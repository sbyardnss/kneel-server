import json
import sqlite3
from models import Size
"""size requests module"""
SIZES = [
    {
        "id": 1,
        "carets": 0.5,
        "price": 405
    },
    {
        "id": 2,
        "carets": 0.75,
        "price": 782
    },
    {
        "id": 3,
        "carets": 1,
        "price": 1470
    },
    {
        "id": 4,
        "carets": 1.5,
        "price": 1997
    },
    {
        "id": 5,
        "carets": 2,
        "price": 3638
    }
]


def get_all_sizes(query_params):
    """sql function for getting all sizes"""
    with sqlite3.connect("./kneel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        sortBy = ""
        if len(query_params) != 0:
            if query_params['_sortBy']:
                print(query_params['_sortBy'])
                if query_params['_sortBy'][0] == 'price':
                    sortBy = "ORDER BY s.price"
        sql_to_execute = f"""
            SELECT
                s.id,
                s.carets,
                s.price
            FROM SIZES s
            {sortBy}
            """
        db_cursor.execute(sql_to_execute)
        sizes = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            size = Size(row['id'], row['carets'], row['price'])
            sizes.append(size.__dict__)
    return sizes

# def get_all_sizes():
#     """function for getting all sizes"""
#     return SIZES


def get_single_size(id):
    """function for getting single size"""
    requested_size = None
    for size in SIZES:
        if size["id"] == id:
            requested_size = size
    return requested_size
