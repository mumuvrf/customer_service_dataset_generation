# Customer Service Dataset Generator

This is a **customer service dataset generator** developed as a task for the class **LLM: Prompts & Applications** at Insper. It was used LangChain to generate fictional customer information that was then stored in a jsonl file.

Below are the columns of the dataset.

## Dataset description

**1. Customer Information**
- Customer ID (unique code)
- Customer Name
- Phone Number
- Address (if relevant for technical visits)
- Customer Type (Individual or Business)

**2. Service Details**
- Service ID (unique tracking number)
- Date and Time of Service
- Service Channel (email, chatbot, WhatsApp, phone, etc.)
- Service Type (technical support, complaint, inquiry, quote request)
- Problem/Request Description (descriptive text)
- Service Category (financial, technical, commercial)
- Service Status (open, in progress, resolved, pending, canceled)

**3. Service Representative**
- Representative Name (assume a small team with only four agents)
- Department (support, sales, finance)

**4. Solution & Feedback**
- Applied Solution (summary of resolution)
- Completion Date (leave blank if the service is not yet completed)
- Customer Satisfaction Rating (scale from 0 to 5)
- Customer Comment (descriptive text)