import json
import sqlite3
from models import Style
"""styles requests module"""
STYLES = [
    {
        "id": 1,
        "style": "Classic",
        "price": 500
    },
    {
        "id": 2,
        "style": "Modern",
        "price": 710
    },
    {
        "id": 3,
        "style": "Vintage",
        "price": 965
    }
]

# def get_all_styles():
#     """function for getting all styles"""
#     return STYLES

def get_all_styles(query_params):
    """sql get all styles"""
    with sqlite3.connect("./kneel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        sortBy = ""
        if len(query_params) != 0:
            if query_params['_sortBy']:
                if query_params['_sortBy'][0] == "price":
                    sortBy = "ORDER BY st.price"
        sql_to_execute = f"""
            SELECT
                st.id,
                st.style,
                st.price
            FROM STYLES st
            {sortBy}
            """
        db_cursor.execute(sql_to_execute)
        styles = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            style = Style(row['id'], row['style'], row['price'])
            styles.append(style.__dict__)
    return styles

def get_single_style(id):
    """function for getting single style"""
    requested_style = None
    for style in STYLES:
        if style["id"] == id:
            requested_style = style
    return requested_style
