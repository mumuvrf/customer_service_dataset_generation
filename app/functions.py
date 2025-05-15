from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import random

from schemas import *

import getpass
import os

from dotenv import load_dotenv, find_dotenv
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
_ = load_dotenv(find_dotenv()) # read local .env file

def get_model_name(model_name, temperature=0):
    if model_name == "gemini": # https://ai.google.dev/gemini-api/docs/rate-limits?hl=pt-br
        if "GOOGLE_API_KEY" not in os.environ: # https://ai.google.dev/gemini-api/docs/api-key
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")
        llm = ChatGoogleGenerativeAI(
            # model="gemini-1.5-pro", # max 50 / dia
            model="gemini-1.5-flash", # max 1500 / dia
            temperature=temperature,
        )
    elif model_name == "openai":
        if "OPENAI_API_KEY" not in os.environ: # https://platform.openai.com
            os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=temperature,
        )
    return llm

def generate_service_representative(llm, departments):
    prompt = f"""
    Generate information about a representative in a service company. \
    The representative must have a believable and creatively chosen American name. \
    They also must belong to one of the following departments: Support, Sales or Finance.

    There must be at least one representative per department. \
    The following departments already have a representative: {departments}
    """
    llm_with_structured_output = llm.with_structured_output(ServiceRepresentative)

    try:
        response = llm_with_structured_output.invoke(prompt)
        return response
    except Exception as e:
        print(f"An unexpected error occurred in generate_service_representative: {e}")
        raise

async def generate_customer_info(llm):
    gender = random.choice(['Male', 'Female'])
    customer_type = gender+"Individual" if random.randrange(1, 10) < 7 else "Business"
    prompt = f"""
    Generate a detailed and imaginative profile for a fictional customer in the United States.

    ### Required information

    1. Customer Type: {customer_type}
    2. Customer Name: A believable and creatively chosen American name (coherent with Customer Type);
    3. Phone Number: A plausible U.S. phone number with a valid area code (format: (XXX) XXX-XXXX or XXX-XXX-XXXX);
    4. Address: A realistic and specific U.S. address, including street, number, city, state, and ZIP code;
    5. Customer ID: A unique, randomly generated 6- to 8-digit number;

    ### Examples

    - 482736; Wellington Rodriguez; 312-555-1234; 457 Lake Shore Drive, Chicago, IL, 60614; Individual;
    - 784512; Thompson Technologies; (646) 555-0198; 1245 Biltmore Avenue, Asheville, NC 28803; Business;
    - 752134; Evelyn Marie Johnson; (202) 555-0197; 1425 Maplewood Ave, Washington, DC 20001; Individual;
    """
    llm_with_structured_output = llm.with_structured_output(CustomerInfo)

    try:
        response = await llm_with_structured_output.ainvoke(prompt)
        return response
    except Exception as e:
        print(f"An unexpected error occurred in generate_customer_info: {e}")
        raise

async def generate_service_details(llm, customer_info):
    category = random.choice(['Financial', 'Technical', 'Commercial'])
    channel = random.choice(['Email', 'Chatbot', 'WhatsApp', 'Phone'])
    service_type = random.choice(['Technical Support', 'Complaint', 'Inquiry', 'Quote Request'])
    status = random.choice(['Open', 'In progress', 'Resolved', 'Pending', 'Cancelled'])
    prompt = f""" 
    Given customer data, generate a detailed, realistic scenario involving a customer service interaction.

    ### Customer Data

    - Customer Type: {customer_info.customer_type}
    - Customer Name: {customer_info.customer_name}
    - Phone Number: {customer_info.phone_number}
    - Address: {customer_info.address};
    - Customer ID: {customer_info.customer_id};

    ### Instructions

    1. Create a fictional yet plausible situation in which a company or individual contacts a third-party service provider regarding a {category} issue.
        - The contact must be made through {channel}.
        - The request must fall on the service type: {service_type}.
    2. Based on the scenario, provide a structured response with the following required information:


    ### Required information

    - Service ID: A unique, randomly generated 3-digit number;
    - Date and time: Date and time of the service;
    - Service Channel: {channel};
    - Service Type: {service_type};
    - Service Category: {category};
    - Problem description: A technical, employee-style explanation of the issue encountered (300 characters max.);
    - Service Status: {status};

    ### Examples

    - 382; 2023-10-10T14:30:00Z; WhatsApp; Complaint; Commercial; Customer reported a pricing issue via WhatsApp where a 25% promotional discount wasn’t applied at checkout for a product bundle. Investigation confirmed a backend error excluding bundles. A partial refund was processed, and the promotion system was corrected; Resolved;
    - 117; 2024-08-23T17:22:00Z; Chatbot; Inquiry; Technical; User inquired via chatbot about recurring connectivity issues in remote monitoring software. Devices intermittently disconnect despite stable internet. Technical team is investigating potential server latency or firmware bugs. User has been updated, and the case remains in progress; In progress;
    """
    llm_with_structured_output = llm.with_structured_output(ServiceDetails)

    try:
        response = await llm_with_structured_output.ainvoke(prompt)
        return response
    except Exception as e:
        print(f"An unexpected error occurred in generate_service_details: {e}")
        raise

async def pick_service_representatives(llm, representatives, service_details):
    prompt = f"""
    Given a list of service representatives of a company and the details of a service, pick the most adequade representative for the matter.

    ### Representatives

    {representatives}

    ### Service Details

    - Service ID: {service_details.service_id};
    - Service Date and time: {service_details.date_and_time};
    - Service Channel: {service_details.service_channel.value};
    - Service Type: {service_details.service_type.value};
    - Service Category: {service_details.service_category.value};
    - Problem description: {service_details.problem_description};
    - Service Status: {service_details.service_status.value};
    """
    llm_with_structured_output = llm.with_structured_output(ServiceRepresentative)

    try:
        response = await llm_with_structured_output.ainvoke(prompt)
        return response
    except Exception as e:
        print(f"An unexpected error occurred in pick_service_representatives: {e}")
        raise

async def generate_feedback(llm, customer_info, service_details, representative):
    rating = random.choice([1, 2, 3, 4, 5])
    prompt = f"""
    You will receive data about a customer service interaction at a service company. \
    Use that data to generate information about the solution applied and customer feedback.

    ### Required information

    - Applied solution: If the Service Status is 'Resolved', write an employee-style summary of the applied solution. Else leave it blank.
    - Completion Date: If the Service Status is 'Resolved', write the date and time of when the issue was solved - it must always happen after the Service Date. Else, leave it blank.
    - Satisfaction Rating: {rating} out of 5.
    - Customer Comment: A detailed customer feedback. It must be consistent with the Satisfaction Rating.

    ### Customer Service Data

    - Customer Type: {customer_info.customer_type.value}
    - Customer Name: {customer_info.customer_name}
    - Phone Number: {customer_info.phone_number}
    - Address: {customer_info.address};
    - Customer ID: {customer_info.customer_id};
    - Service ID: {service_details.service_id};
    - Service Date and time: {service_details.date_and_time};
    - Service Channel: {service_details.service_channel.value};
    - Service Type: {service_details.service_type.value};
    - Service Category: {service_details.service_category.value};
    - Problem description: {service_details.problem_description};
    - Service Status: {service_details.service_status.value};
    - Representative name: {representative.representative_name};
    - Representative department : {representative.department.value}
    """
    llm_with_structured_output = llm.with_structured_output(SolutionAndFeedback)

    try:
        response = await llm_with_structured_output.ainvoke(prompt)
        return response
    except Exception as e:
        print(f"An unexpected error occurred in generate_feedback: {e}")
        raise