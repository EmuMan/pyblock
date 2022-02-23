from typing import Any
from requests import Response

__all__ = (
    'PyblockException',
    'HTTPInvalidResponse',
    'SkyblockAPIException',
    'MissingRequestData',
    'ForbiddenAccess',
    'InvalidRequestData',
    'RequestLimitReached',
    'DataNotPopulated'
)

class PyblockException(Exception):
    """Base exception class for pyblock"""
    pass

class HTTPInvalidResponse(PyblockException):
    """Exception class for when an HTTP request fails"""
    
    response: Response

    def __init__(self, response: Response):
        self.response = response
        super().__init__(str(response.status_code))

class SkyblockAPIException(PyblockException):
    """Base exception class for any invalid Hypixel API responses"""

    response_data: dict[str, Any]
    
    def __init__(self, response_data: dict[str, Any]):
        self.response_data = response_data
        super().__init__(response_data['cause'])

class MissingRequestData(SkyblockAPIException):
    pass

class ForbiddenAccess(SkyblockAPIException):
    pass

class InvalidRequestData(SkyblockAPIException):
    pass

class RequestLimitReached(SkyblockAPIException):

    global_throttle: bool

    def __init__(self, response_data: dict[str, Any]):
        self.global_throttle = response_data.get('global', False)
        super().__init__(response_data)

class DataNotPopulated(SkyblockAPIException):
    pass

def _get_response_exception(response: Response) -> PyblockException | None:
    data = response.json()
    if response.status_code == 400:
        return MissingRequestData(data)
    elif response.status_code == 403:
        return ForbiddenAccess(data)
    elif response.status_code == 422:
        return InvalidRequestData(data)
    elif response.status_code == 429:
        return RequestLimitReached(data)
    elif response.status_code == 503:
        return DataNotPopulated(data)
    return None
