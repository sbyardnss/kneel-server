DATABASE = {
    "metals": [
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
    ],
    "sizes": [
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
    ],
    "styles": [
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
    ],
    "orders": [
        {
            "id": 1,
            "metalId": 3,
            "sizeId": 2,
            "styleId": 1
        }
    ]
}


def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]


def retrieve(resource, id):
    """For GET requests to a single resource"""
    requested_asset = None
    for asset in DATABASE[resource]:
        if asset["id"] == id:
            requested_asset = asset
    return requested_asset


def create(resource, resource_obj):
    """For POST requests to a collection"""
    max_id = DATABASE[resource][-1]["id"]
    new_id = max_id + 1
    resource_obj["id"] = new_id
    DATABASE[resource].append(resource_obj)
    return resource_obj


def update():
    """For PUT requests to a single resource"""
    pass


def delete():
    """For DELETE requests to a single resource"""
    pass
