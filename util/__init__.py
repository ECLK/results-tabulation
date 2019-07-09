class RequestBody:
    def __init__(self, body):
        self.body = body

    def get(self, property_name):
        if property_name in self.body:
            return self.body[property_name]
        else:
            return None
