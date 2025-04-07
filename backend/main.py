import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from pydantic import BaseModel
from agents.scheduler_agent import SchedulerAgent
from agents.customer_service_agent import CustomerServiceAgent

app = FastAPI()
scheduler = SchedulerAgent()
customer_service = CustomerServiceAgent()

class AppointmentRequest(BaseModel):
    customer_name: str
    time_slot: str

class CustomerQuery(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Salon backend running"}

@app.post("/book")
def book_appointment(req: AppointmentRequest):
    return scheduler.book_appointment(req.customer_name, req.time_slot)

@app.get("/appointments")
def list_appointments():
    return scheduler.list_appointments()

@app.post("/customer_query")
def handle_customer_query(req: CustomerQuery):
    return customer_service.handle_query(req.message)

