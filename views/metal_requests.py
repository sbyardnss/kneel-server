import json
import sqlite3
from models import Metal
"""metal requests module"""
METALS = [
    {
        "id": 1,
        "metal": "Sterling Silver",
        "price": 12.42
    },
    {
        "id": 2,
        "metal": "14K Gold",
        "price": 736.4
    },
    {
        "id": 3,
        "metal": "24K Gold",
        "price": 1258.9
    },
    {
        "id": 4,
        "metal": "Platinum",
        "price": 795.45
    },
    {
        "id": 5,
        "metal": "Palladium",
        "price": 1241
    }
]


def get_all_metals(query_params):
    """sql function for getting all metals"""
    with sqlite3.connect("./kneel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        sortBy = ""
        if len(query_params) != 0:
            if query_params['_sortBy']:
                print(query_params['_sortBy'])
                if query_params['_sortBy'][0] == 'price':
                    sortBy = "ORDER BY m.price"
        sql_to_execute = f"""
            SELECT
                m.id,
                m.metal,
                m.price
            FROM metals m
            {sortBy}
            """
        db_cursor.execute(sql_to_execute)
        metals = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            metal = Metal(row['id'], row['metal'], row['price'])
            metals.append(metal.__dict__)
    return metals


def get_single_metal(id):
    """function for getting single metal"""
    requested_metal = None
    for metal in METALS:
        if metal["id"] == id:
            requested_metal = metal
    return requested_metal

def update_metal(id, new_metal):
    """sql function for updating metal price"""
    with sqlite3.connect("./kneel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Metals
            SET
                price = ?
        WHERE id = ?
        """, (new_metal['price'], id,))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    return True
