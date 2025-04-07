
import zmq
import threading
import requests
import time

class CustomerServiceAgent:
    def __init__(self, zmq_pub_url="tcp://127.0.0.1:5556", zmq_sub_url="tcp://127.0.0.1:5557", llm_api_url="http://localhost:8000/generate"):
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.connect(zmq_pub_url)
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(zmq_sub_url)
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "customer_queries")
        self.llm_api_url = llm_api_url
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
                response = self.handle_query(message)
                self.pub_socket.send_multipart([
                    b"customer_responses",
                    response.encode('utf-8')
                ])
            except zmq.Again:
                time.sleep(0.1)
            except Exception as e:
                print(f"Error: {e}")

    def handle_query(self, query):
        try:
            payload = {"prompt": query}
            r = requests.post(self.llm_api_url, json=payload, timeout=10)
            if r.status_code == 200:
                data = r.json()
                return data.get("response", "I'm sorry, I couldn't understand your question.")
            else:
                return "I'm sorry, there was an error processing your request."
        except Exception as e:
            return f"Error contacting LLM API: {e}"

if __name__ == "__main__":
    agent = CustomerServiceAgent()
    agent.start()
    print("Customer Service Agent started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        agent.stop()
        print("Agent stopped.")
