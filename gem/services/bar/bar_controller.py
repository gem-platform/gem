from uuid import uuid4


class BarController:
    """Bar controller"""
    def __init__(self):
        self.__orders = []

    @property
    def orders(self):
        """Return list of orders"""
        return self.__orders

    def add(self, user, items):
        """Add new order"""
        new_order = {
            "id": str(uuid4()),
            "name": user,
            "items": items
        }
        self.__orders.append(new_order)
        return new_order

    def done(self, order_id):
        """Complete order"""
        self.__orders = list(filter(lambda x: x["id"] != order_id, self.__orders))
