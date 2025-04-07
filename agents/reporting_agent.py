
import zmq
import threading
import time
import json
import requests

class ReportingAgent:
    def __init__(self, zmq_url='tcp://localhost:5556', llm_api_url='http://localhost:8000/summarize'):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(zmq_url)
        topics = ['sales', 'appointments', 'inventory', 'staff']
        for topic in topics:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)
        self.data = {topic: [] for topic in topics}
        self.llm_api_url = llm_api_url
        self.running = True

    def listen(self):
        while self.running:
            try:
                message = self.socket.recv_string(flags=zmq.NOBLOCK)
                topic, content = message.split(' ', 1)
                event = json.loads(content)
                self.data[topic].append(event)
            except zmq.Again:
                time.sleep(0.1)

    def generate_report(self):
        report = ''
        for topic, events in self.data.items():
            report += f"
=== {topic.capitalize()} Report ===
"
            report += f"Total events: {len(events)}
"
            # Add more detailed aggregation here as needed
            for event in events[-5:]:  # show last 5 events
                report += json.dumps(event) + '
'
        return report

    def summarize_report(self, report_text):
        try:
            response = requests.post(self.llm_api_url, json={'text': report_text})
            if response.status_code == 200:
                return response.json().get('summary', '')
            else:
                return 'LLM API error'
        except Exception as e:
            return f'LLM API exception: {e}'

    def start(self):
        listener_thread = threading.Thread(target=self.listen)
        listener_thread.daemon = True
        listener_thread.start()
        print('ReportingAgent started. Listening for events...')
        try:
            while True:
                time.sleep(60)  # generate report every 60 seconds
                report = self.generate_report()
                summary = self.summarize_report(report)
                print('--- Generated Report ---')
                print(report)
                print('--- Summary ---')
                print(summary)
        except KeyboardInterrupt:
            self.running = False
            print('ReportingAgent stopped.')

if __name__ == '__main__':
    agent = ReportingAgent()
    agent.start()
