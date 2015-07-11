"""
HTTP API specific exceptions and responses.
"""

from pyramid.httpexceptions import HTTPClientError
from pyramid.response import Response

from ichnaea.exceptions import BaseClientError


class BaseAPIError(HTTPClientError, BaseClientError):
    """
    A base class to represent API errors that all act as HTTP responses
    and have a similar JSON body.
    """

    code = 400  #:
    domain = ''  #:
    reason = ''  #:
    message = ''  #:

    def __init__(self):
        # explicitly avoid calling the HTTPException init magic
        Response.__init__(self, status=self.code, json_body=self.json_body())
        Exception.__init__(self)
        self.detail = self.message

    def __str__(self):
        return '<%s>: %s' % (self.__class__.__name__, self.code)

    @classmethod
    def json_body(cls):
        """A JSON representation of this error."""
        return {
            'error': {
                'errors': [{
                    'domain': cls.domain,
                    'reason': cls.reason,
                    'message': cls.message,
                }],
                'code': cls.code,
                'message': cls.message,
            },
        }


class DailyLimitExceeded(BaseAPIError):

    code = 403  #:
    domain = 'usageLimits'  #:
    reason = 'dailyLimitExceeded'  #:
    message = 'You have exceeded your daily limit.'  #:


class InvalidAPIKey(BaseAPIError):

    code = 400  #:
    domain = 'usageLimits'  #:
    reason = 'keyInvalid'  #:
    message = 'Missing or invalid API key.'  #:


class LocationNotFound(BaseAPIError):

    code = 404  #:
    domain = 'geolocation'  #:
    reason = 'notFound'  #:
    message = 'Not found'  #:


class LocationNotFoundV1(LocationNotFound):
    """
    A variant of :exc:`~ichnaea.api.exceptions.LocationNotFound` used
    in earlier version 1 HTTP APIs.
    """

    code = 200  #:

    @classmethod
    def json_body(cls):
        return {'status': 'not_found'}


class ParseError(BaseAPIError):

    code = 400  #:
    domain = 'global'  #:
    reason = 'parseError'  #:
    message = 'Parse Error'  #: