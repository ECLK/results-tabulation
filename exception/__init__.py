from connexion import ProblemException


def UnauthorizedException(message="", code=None):
    raise ProblemException(401, "Unauthorized", message, "Unauthorized")


def ForbiddenException(message="", code=None):
    raise ProblemException(403, "Forbidden", message, "Forbidden")


def NotFoundException(message="", code=None):
    raise ProblemException(404, "Not Found", message, "NotFound")


def MethodNotAllowedException(message="", code=None):
    raise ProblemException(405, "Method Not Allowed", message, "MethodNotAllowed")


def InternalServerErrorException(message="", code=None):
    raise ProblemException(500, "Internal Server Error", message, "InternalServerError")


def NotImplementedException(message="", code=None):
    raise ProblemException(501, "Not Implemented", message, "NotImplemented")
