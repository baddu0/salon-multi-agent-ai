import sys
import zmq
import threading
import time
import json
from datetime import datetime

sys.path.append("/root/salon_app/agents")
try:
    from scheduler_agent import SchedulerAgent
except ImportError:
    SchedulerAgent = None

class SalonOrchestratorAgent:
    def __init__(self, sub_port=5557, pub_port=5558):
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(f"tcp://localhost:{sub_port}")
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(f"tcp://*:{pub_port}")
        self.scheduler = SchedulerAgent() if SchedulerAgent else None
        self.thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.thread.start()

    def listen_loop(self):
        while True:
            try:
                msg = self.sub_socket.recv_json()
                self.process_event(msg)
            except Exception as e:
                print(f"Error processing message: {e}")
            time.sleep(0.1)

    def process_event(self, event):
        event_type = event.get("type")
        data = event.get("data", {})
        print(f"Received event: {event_type}")
        if event_type == "optimization_suggestions":
            self.handle_optimization(data)

    def handle_optimization(self, data):
        idle_slots = data.get("idle_slots", [])
        promotions = data.get("promotions", [])
        if len(idle_slots) >= 4:
            self.trigger_marketing(promotions)
        self.adjust_schedule(idle_slots)

    def trigger_marketing(self, promotions):
        campaign = {
            "timestamp": datetime.now().isoformat(),
            "promotions": promotions
        }
        print(f"Triggering marketing campaign: {campaign}")
        self.pub_socket.send_json({"type": "marketing_campaign", "data": campaign})

    def adjust_schedule(self, idle_slots):
        if not self.scheduler:
            print("SchedulerAgent not available, skipping schedule adjustment")
            return
        for slot in idle_slots[:3]:
            print(f"Considering adjustment for slot: {slot}")

if __name__ == "__main__":
    agent = SalonOrchestratorAgent()
    print("Salon Orchestrator Agent running...")
    while True:
        time.sleep(10)

