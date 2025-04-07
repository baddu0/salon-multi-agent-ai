
import zmq
import threading
import time
import json

class SalonOptimizationAgent:
    def __init__(self, pub_address="tcp://*:5556", analysis_interval=3600):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(pub_address)
        self.analysis_interval = analysis_interval
        self.inventory_data = {}
        self.staff_schedule = {}
        self.running = False
        self.thread = None

    def update_data(self, inventory_data, staff_schedule):
        self.inventory_data = inventory_data
        self.staff_schedule = staff_schedule

    def analyze_inventory(self):
        suggestions = []
        for item, usage in self.inventory_data.items():
            avg_use = usage.get('average_daily_use', 0)
            stock = usage.get('current_stock', 0)
            reorder_point = usage.get('reorder_point', 0)
            if stock > avg_use * 30:
                suggestions.append(f"Reduce order of {item}, overstocked.")
            elif stock < reorder_point:
                suggestions.append(f"Reorder {item}, stock below reorder point.")
        return suggestions

    def analyze_staff(self):
        suggestions = []
        for day, shifts in self.staff_schedule.items():
            for shift, staff_count in shifts.items():
                demand = shifts.get('expected_clients', {}).get(shift, 0)
                if staff_count > demand / 2 + 1:
                    suggestions.append(f"Reduce staff on {day} during {shift} shift.")
                elif staff_count < max(1, demand / 4):
                    suggestions.append(f"Add staff on {day} during {shift} shift.")
        return suggestions

    def generate_recommendations(self):
        recs = {}
        recs['inventory'] = self.analyze_inventory()
        recs['staffing'] = self.analyze_staff()
        return recs

    def publish_recommendations(self):
        recs = self.generate_recommendations()
        message = json.dumps(recs)
        self.socket.send_string(message)

    def start_periodic_analysis(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _run(self):
        while self.running:
            self.publish_recommendations()
            time.sleep(self.analysis_interval)

if __name__ == "__main__":
    agent = SalonOptimizationAgent()
    # Example data
    inventory = {
        "Shampoo": {"average_daily_use": 2, "current_stock": 100, "reorder_point": 20},
        "Conditioner": {"average_daily_use": 1, "current_stock": 10, "reorder_point": 5}
    }
    staff = {
        "Monday": {"morning": 3, "afternoon": 4, "expected_clients": {"morning": 4, "afternoon": 6}},
        "Tuesday": {"morning": 2, "afternoon": 2, "expected_clients": {"morning": 8, "afternoon": 10}}
    }
    agent.update_data(inventory, staff)
    agent.publish_recommendations()
