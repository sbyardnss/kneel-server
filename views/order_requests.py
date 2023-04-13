import json
import sqlite3
from models import Order
"""order requests module"""
ORDERS = [
    {
        "id": 1,
        "metal": "Sterling Silver",
        "size": "carets: 0.5",
        "style": "Classic"
    }
]


def get_all_orders():
    """function for getting all orders"""
    with sqlite3.connect("./kneel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id
        FROM orders o
        """)
        orders = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            order = Order(row['id'], row['metal_id'],
                          row['size_id'], row['style_id'])
            orders.append(order.__dict__)
    return orders


def get_single_order(id):
    """sql function for getting single order"""
    with sqlite3.connect("./kneel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id
        FROM orders o
        WHERE o.id = ?
        """, (id, ))
        data = db_cursor.fetchone()
        order = Order(data['id'], data['metal_id'],
                      data['size_id'], data['style_id'])
    return order.__dict__


def create_order(order):
    """sql function for creating a new order"""
    with sqlite3.connect("./kneel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Orders
            ( metal_id, size_id, style_id)
        VALUES
            (?, ?, ?);
        """, (order['metal_id'], order['size_id'], order['style_id']))
        id = db_cursor.lastrowid
        order['id'] = id
    return order


def delete_order(id):
    """sql function for deleting order"""
    with sqlite3.connect("./kneel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Orders
        WHERE id = ?
        """, (id, ))


def update_order(id, new_order):
    """function for updating an existing order"""
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            ORDERS[index] = new_order
            break
