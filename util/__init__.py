import connexion


class RequestBody:
    def __init__(self, body):
        self.body = body

    def get(self, property_name):
        if property_name in self.body:
            return self.body[property_name]
        else:
            return None


class Auth:
    def get_user_id(self):
        return 2


def get_paginated_query(query):
    limit = connexion.request.args["limit"]
    offset = connexion.request.args["offset"]

    return query.limit(limit).offset(offset)
