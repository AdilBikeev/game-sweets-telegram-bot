storage = dict()

def init(user_id):
    storage[user_id] = dict(attempt=None, random_digit=None)

def set(user_id, key, value):
    storage[user_id][key] = value

def get(user_id):
    return storage[user_id]