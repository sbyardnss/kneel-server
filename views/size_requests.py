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

def get_all_sizes():
    """function for getting all sizes"""
    return SIZES

def get_single_size(id):
    """function for getting single size"""
    requested_size = None
    for size in SIZES:
        if size["id"] == id:
            requested_size = size
    return requested_size
