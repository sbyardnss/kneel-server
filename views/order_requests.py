import json
import sqlite3
from models import Order, Metal, Size, Style
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
            o.style_id,
            m.metal metal_metal,
            m.price metal_price,
            s.carets size_carets,
            s.price size_price,
            t.style style_style,
            t.price style_price
        FROM orders o
        JOIN Metals m
            ON o.metal_id = m.id
        JOIN Sizes s
            ON o.size_id = s.id
        JOIN Styles t
            ON o.style_id = t.id
        """)
        orders = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            order = Order(row['id'], row['metal_id'],
                          row['size_id'], row['style_id'])
            metal_exp = Metal(
                row['metal_id'], row['metal_metal'], row['metal_price'])
            order.metal = metal_exp.__dict__
            size_exp = Size(
                row['size_id'], row['size_carets'], row['size_price'])
            order.size = size_exp.__dict__
            style_exp = Style(
                row['style_id'], row['style_style'], row['style_price'])
            order.style = style_exp.__dict__
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
