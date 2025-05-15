import jsonlines
import pandas as pd
import asyncio
from tqdm import tqdm
import tqdm.asyncio
from functions import *

jsonl_filename = "../data/output.jsonl"
xlsx_filename = "../data/output.xlsx"

async def store_in_json(filename, customer_info, service_details, representative, feedback):
    data = {
        "customer_id" : customer_info.customer_id,
        "customer_name" : customer_info.customer_name,
        "customer_type" : customer_info.customer_type.value,
        "customer_phone_number" : customer_info.phone_number,
        "customer_address" : customer_info.address,
        "service_id" : service_details.service_id,
        "service_date" : service_details.date_and_time,
        "service_channel" : service_details.service_channel.value,
        "service_type" : service_details.service_type.value,
        "service_category" : service_details.service_category.value,
        "problem_description" : service_details.problem_description,
        "service_status" : service_details.service_status.value,
        "representative_name" : representative.representative_name,
        "representative_department" : representative.department.value,
        "applied_solution" : feedback.applied_solution,
        "completion_date" : feedback.completion_date,
        "satisfaction_rating" : feedback.satisfaction_rating,
        "customer_comment" : feedback.customer_comment
    }
    
    with jsonlines.open(filename, mode='a') as writer:
        writer.write(data)
    pass

def representative_to_string(representative):
    return f"\nRepresentative name: {representative.representative_name}\nRepresentative department: {representative.department.value}\n"

async def generate_entry(llm, representatives):
    customer_info = await generate_customer_info(llm)

    service_details = await generate_service_details(llm, customer_info)

    representatives_txt = ''.join(map(representative_to_string, representatives))
    representative = await pick_service_representatives(llm, representatives_txt, service_details)
    
    feedback = await generate_feedback(llm, customer_info, service_details, representative)

    await store_in_json(jsonl_filename, customer_info, service_details, representative, feedback)

async def run_generate_entry_wrapper(semaphore, llm, representatives):
    async with semaphore: # Acquire semaphore before running
        await generate_entry(llm, representatives)

async def main():
    llm = get_model_name('openai', temperature=0.7)

    representatives = []
    departments = set([])
    for i in range(4):
        departments_txt = ' '.join(departments)
        curr = generate_service_representative(llm, departments_txt)
        departments.add(curr.department.value)
        representatives.append(curr)

    semaphore = asyncio.Semaphore(5) # Limit to 5 concurrent tasks
    tasks = []
    for i in range(10): # Create 10 tasks
        tasks.append(run_generate_entry_wrapper(semaphore, llm, representatives))

    await tqdm.asyncio.tqdm.gather(*tasks) # Run all tasks concurrently

    # Read JSONL into a list of dictionaries
    records = []
    with jsonlines.open(jsonl_filename) as reader:
        for obj in reader:
            records.append(obj)

    # Convert to DataFrame
    df = pd.DataFrame(records)

    # Save to Excel
    df.to_excel(xlsx_filename, index=False)

if __name__ == "__main__":
    asyncio.run(main())