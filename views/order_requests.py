from .metal_requests import get_single_metal
from .size_requests import get_single_size
from .style_requests import get_single_style
"""order requests module"""
ORDERS = [
    {
        "id": 1,
        "metalId": 3,
        "sizeId": 2,
        "styleId": 1
    }
]


def get_all_orders():
    """function for getting all orders"""
    return ORDERS


def get_single_order(id):
    """function for getting single order"""
    requested_order = None
    for order in ORDERS:
        if order["id"] == id:
            requested_order = order
            requested_order["metal"] = get_single_metal(order["metalId"])
            requested_order["size"] = get_single_size(order["sizeId"])
            requested_order["style"] = get_single_style(order["styleId"])
            requested_order.pop("styleId", None)
            requested_order.pop("sizeId", None)
            requested_order.pop("metalId", None)
    return requested_order


def create_order(order):
    """function for creating a new order"""
    # max_id = None
    # if ORDERS[-1]["id"] is None:
    #     max_id = 0
    # else:
    #     max_id = ORDERS[-1]["id"]
    max_id = ORDERS[-1]["id"]
    new_id = max_id + 1
    order["id"] = new_id
    ORDERS.append(order)
    return order

def delete_order(id):
    """function for deleting an order obj"""
    order_index = -1
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            order_index = index
    if order_index >= 0:
        ORDERS.pop(order_index)

def update_order(id, new_order):
    """function for updating an existing order"""
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            ORDERS[index] = new_order
            break
