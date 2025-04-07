import zmq

class InventoryAgent:
    def __init__(self, low_stock_threshold=5, zmq_pub_url='tcp://*:5556'):
        self.inventory = {}
        self.low_stock_threshold = low_stock_threshold
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind(zmq_pub_url)

    def add_product(self, product_name, quantity):
        self.inventory[product_name] = self.inventory.get(product_name, 0) + quantity
        self._check_and_alert(product_name)

    def update_stock(self, product_name, quantity):
        self.inventory[product_name] = quantity
        self._check_and_alert(product_name)

    def reduce_stock(self, product_name, quantity):
        if product_name in self.inventory:
            self.inventory[product_name] -= quantity
            if self.inventory[product_name] < 0:
                self.inventory[product_name] = 0
            self._check_and_alert(product_name)

    def get_stock(self, product_name):
        return self.inventory.get(product_name, 0)

    def _check_and_alert(self, product_name):
        qty = self.inventory.get(product_name, 0)
        if qty <= self.low_stock_threshold:
            alert_msg = f'LOW_STOCK:{product_name}:{qty}'
            self.publisher.send_string(alert_msg)

    def close(self):
        self.publisher.close()
        self.context.term()
