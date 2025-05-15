from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum

__all__ = ["CustomerInfo", "ServiceDetails", "ServiceRepresentative", "SolutionAndFeedback"]

class CustomerType(Enum):
    INDIVIDUAL = "Individual"
    BUSINESS = "Business"

class CustomerInfo(BaseModel):
    customer_id : Annotated[int, Field(..., description = "Customer ID Number")]
    customer_name : Annotated[str, Field(..., description = "Customer Name")]
    phone_number : Annotated[str, Field(..., description = "Customer Phone Number")]
    address : Annotated[str, Field(..., description = "Customer Address")]
    customer_type : Annotated[CustomerType, Field(..., description = "Customer type, either individual or business")]

class ServiceChannel(Enum):
    EMAIL = "Email"
    CHATBOT = "Chatbot"
    WHATSAPP = "WhatsApp"
    PHONE = "Phone"
    OTHER = "Others"

class ServiceType(Enum):
    TECHNCAL_SUPPORT = "Technical Support"
    COMPLAINT = "Complaint"
    INQUIRY = "Inquiry"
    QUOTE_REQUEST = "Quote Request"

class ServiceCategory(Enum):
    FINANCIAL = "Financial"
    TECHNICAL = "Technical"
    COMMERCIAL = "Commercial"

class ServiceStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    PENDING = "Pending"
    CANCELED = "Cancelled"

class ServiceDetails(BaseModel):
    service_id : Annotated[int, Field(..., description = "Service ID")]
    date_and_time : Annotated[str, Field(..., description = "Date and time of the service")]
    service_channel : Annotated[ServiceChannel, Field(..., description = "Service Channel. Either Email, Chatbot, WhatsApp, Phone or Others")]
    service_type : Annotated[ServiceType, Field(..., description = "Service Type. Either Technical Support, Complaint, Inquiry or Quote Request")]
    problem_description : Annotated[str, Field(..., descrition = "Problem/Request description")]
    service_category : Annotated[ServiceCategory, Field(..., description = "Service Category. Either Financial, Technical or Commercial")]
    service_status : Annotated[ServiceStatus, Field(..., description = "Service Status. Open, In progress, Resolved, Pending or Cancelled")]

class Department(Enum):
    SUPPORT = "Support"
    SALES = "Sales"
    FINANCE = "Finance"

class ServiceRepresentative(BaseModel):
    representative_name : Annotated[str, Field(..., description = "Representative name.")]
    department : Annotated[Department, Field(..., description = "Department. Either Support, Sales or Finance.")]

class SolutionAndFeedback(BaseModel):
    applied_solution : Annotated[str | None, Field(..., description = "Summary of resolution.")]
    completion_date : Annotated[str | None, Field(..., description = "Completion date (leave blank if the service is not yet completed).")]
    satisfaction_rating : Annotated[int, Field(..., description = "Customer Satisfaction Rating (scale from 0 to 5)")]
    customer_comment : Annotated[str, Field(..., description = "Customer Comment (descriptive text)")]