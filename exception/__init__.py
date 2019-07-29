from connexion import ProblemException


def UnauthorizedException(message=""):
    raise ProblemException(401, "Unauthorized", message, "Unauthorized")


def ForbiddenException(message=""):
    raise ProblemException(403, "Forbidden", message, "Forbidden")


def NotFoundException(message=""):
    raise ProblemException(404, "Not Found", message, "NotFound")


def MethodNotAllowedException(message=""):
    raise ProblemException(405, "Method Not Allowed", message, "MethodNotAllowed")


def InternalServerErrorException(message=""):
    raise ProblemException(500, "Internal Server Error", message, "InternalServerError")


def NotImplementedException(message=""):
    raise ProblemException(501, "Not Implemented", message, "NotImplemented")
