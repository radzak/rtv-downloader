class RTVException(Exception):
    pass


class VideoIdNotMatchedError(RTVException):
    pass


class WrongUrlError(RTVException):
    pass


class WrongQualityError(RTVException):
    pass


class NoTemplateFoundError(RTVException):
    pass
