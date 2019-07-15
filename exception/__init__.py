from connexion import ProblemException


def UnauthorizedException(message=""):
    raise ProblemException(401, "Unauthorized", message, "Unauthorized")


def ForbiddenException(message=""):
    raise ProblemException(403, "Unauthorized", message, "Unauthorized")


def NotFoundException(message=""):
    raise ProblemException(404, "Unauthorized", message, "Unauthorized")


def MethodNotAllowedException(message=""):
    raise ProblemException(405, "Unauthorized", message, "Unauthorized")


def InternalServerErrorException(message=""):
    raise ProblemException(500, "Unauthorized", message, "Unauthorized")


def NotImplementedException(message=""):
    raise ProblemException(501, "Unauthorized", message, "Unauthorized")
