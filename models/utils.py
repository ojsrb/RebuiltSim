class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)


def wait(field, seconds):
    start = field.timestamp
    while True:
        elapsed = field.timestamp - start

        if elapsed > seconds * 30:
            break