import zmq
import threading
import requests
import json
import time

class PersonalizedMarketingAgent:
    def __init__(self, llm_url='http://localhost:8000/generate', pub_port=5556, sub_port=5557):
        self.llm_url = llm_url
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(f'tcp://*:{pub_port}')
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(f'tcp://127.0.0.1:{sub_port}')
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, 'customer_updates')
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _listen_loop(self):
        while self.running:
            try:
                topic, message = self.sub_socket.recv_multipart()
                topic = topic.decode('utf-8')
                message = message.decode('utf-8')
                data = json.loads(message)
                customer_id = data.get('customer_id')
                customer_data = data.get('customer_data', {})
                booking_history = data.get('booking_history', [])
                self.process_customer(customer_id, customer_data, booking_history)
            except zmq.Again:
                time.sleep(0.1)
            except Exception as e:
                print(f"Error: {e}")

    def generate_prompt(self, customer_data, booking_history):
        prompt = f"""You are a marketing AI for a salon.
Analyze the following customer data and booking history.
Generate a personalized promotion and upsell suggestion.

Customer Data:
{json.dumps(customer_data, indent=2)}

Booking History:
{json.dumps(booking_history, indent=2)}

Respond with a JSON object with 'promotion' and 'upsell' fields."""
        return prompt

    def query_llm(self, prompt):
        response = requests.post(self.llm_url, json={'prompt': prompt})
        response.raise_for_status()
        return response.json()

    def publish_message(self, customer_id, message):
        payload = {
            'customer_id': customer_id,
            'message': message
        }
        self.pub_socket.send_json(payload)

    def process_customer(self, customer_id, customer_data, booking_history):
        prompt = self.generate_prompt(customer_data, booking_history)
        llm_response = self.query_llm(prompt)
        marketing_message = {
            'promotion': llm_response.get('promotion', ''),
            'upsell': llm_response.get('upsell', '')
        }
        self.publish_message(customer_id, marketing_message)

if __name__ == '__main__':
    agent = PersonalizedMarketingAgent()
    agent.start()
    print('Personalized Marketing Agent started. Press Ctrl+C to stop.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        agent.stop()
        print('Agent stopped.')
