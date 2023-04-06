"""order requests module"""
ORDERS = []

def get_all_orders():
    """function for getting all orders"""
    return ORDERS

def get_single_order(id):
    """function for getting single order"""
    requested_order = None
    for order in ORDERS:
        if order["id"] == id:
            requested_order = order
    return requested_order
