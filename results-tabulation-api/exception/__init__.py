from connexion import ProblemException


def UnauthorizedException(message="", code=None):
    raise ProblemException(401, "Unauthorized", message, "Unauthorized", code)


def ForbiddenException(message="", code=None):
    raise ProblemException(403, "Forbidden", message, "Forbidden", code)


def NotFoundException(message="", code=None):
    raise ProblemException(404, "Not Found", message, "NotFound", code)


def MethodNotAllowedException(message="", code=None):
    raise ProblemException(405, "Method Not Allowed", message, "MethodNotAllowed", code)


def InternalServerErrorException(message="", code=None):
    raise ProblemException(500, "Internal Server Error", message, "InternalServerError", code)


def NotImplementedException(message="", code=None):
    raise ProblemException(501, "Not Implemented", message, "NotImplemented", code)


def InvalidInputException(message="", code=None):
    raise ProblemException(400, "Invalid Input", message, "Forbidden", code)
