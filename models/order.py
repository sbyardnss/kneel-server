class Order():
    """class for creating new order"""
    def __init__(self, id, style, size, metal):
        self.id = id
        self.style_id = style
        self.size_id = size
        self.metal_id = metal
        self.metal = None
        self.size = None
        self.style = None
