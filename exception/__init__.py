class ApiException(Exception):
    def __init__(self, title, message, code):
        super()

        self.title = title
        self.message = message
        self.code = code

    def to_json_response(self):
        return {
            "type": self.title,
            "message": self.message,
            "code": self.code
        }, self.code


class UnauthorizedException(ApiException):
    def __init__(self, message=""):
        super(UnauthorizedException, self).__init__("Unauthorized", message, 401)


class ForbiddenException(ApiException):
    def __init__(self, message=""):
        super(ForbiddenException, self).__init__("Forbidden", message, 403)


class NotFoundException(ApiException):
    def __init__(self, message=""):
        super(NotFoundException, self).__init__("Not Found", message, 404)


class MethodNotAllowedException(ApiException):
    def __init__(self, message=""):
        super(MethodNotAllowedException, self).__init__("Method Not Allowed", message, 405)


class InternalServerErrorException(ApiException):
    def __init__(self, message=""):
        super(InternalServerErrorException, self).__init__("Internal Server Error", message, 500)


class NotImplementedException(ApiException):
    def __init__(self, message=""):
        super(NotImplementedException, self).__init__("Not Implemented", message, 501)
