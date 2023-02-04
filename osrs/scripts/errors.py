class RequestFailed(Exception):
    """ Raised when an HTTP request to the hiscores API fails. """

    def __init__(self, message, code=None):
        self.code = code
        super().__init__(message)

class BadHiScoresPage(Exception):

    def __init__(self, message, code=None):
        self.code = code
        super().__init__(message)

class UserNotFound(Exception):
    def __init__(self, message, code=None):
        self.code = code
        super().__init__(message)
