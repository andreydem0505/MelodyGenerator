def sub(a, b):
    if a <= b:
        return a - b + 12
    return a - b

def add(a, b):
    return (a + b - 1) % 12 + 1