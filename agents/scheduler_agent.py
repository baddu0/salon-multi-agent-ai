class SchedulerAgent:
    def __init__(self):
        self.appointments = []

    def book_appointment(self, customer_name, time_slot):
        self.appointments.append({"customer": customer_name, "time": time_slot})
        return {"status": "booked", "customer": customer_name, "time": time_slot}

    def list_appointments(self):
        return self.appointments

