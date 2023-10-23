import pytest


class HTTPRequest:
    def __init__(self, request_type, resource_path, protocol_type):
        self.request_type = request_type
        self.resource_path = resource_path
        self.protocol_type = protocol_type

    def __str__(self):
        return f"Request Type: {self.request_type}\nResource Path: {self.resource_path}\nProtocol Type: {self.protocol_type}"


class BadRequestTypeError(Exception):
    pass


class BadHTTPVersion(Exception):
    pass


def reqstr2obj(request_string):
    request_types = ['GET', 'POST']
    protocol_types = ['HTTP1.0', 'HTTP1.1', 'HTTP2.0']

    if not isinstance(request_string, str):
        raise TypeError("Request_string is not of a type string")

    split_request = request_string.split()
    if len(split_request) != 3:
        return None

    request_type = split_request[0]
    resource_path = split_request[1]
    protocol_type = split_request[2]

    if request_type not in request_types:
        raise BadRequestTypeError("Illegal request type")

    if not resource_path.startswith("/"):
        raise ValueError("Path must start with /")

    if protocol_type not in protocol_types:
        raise BadHTTPVersion("Illegal HTTP Version")

    return HTTPRequest(request_type, resource_path, protocol_type)


def test1():
    with pytest.raises(TypeError):
        reqstr2obj(1)


def test2():
    request_string = "GET / HTTP1.1"
    http_request = reqstr2obj(request_string)
    assert isinstance(http_request, HTTPRequest)


def test3():
    request_string = "GET / HTTP1.1"
    http_request = reqstr2obj(request_string)
    assert isinstance(http_request, HTTPRequest)
    assert http_request.request_type == "GET"
    assert http_request.resource_path == "/"
    assert http_request.protocol_type == "HTTP1.1"


@pytest.mark.parametrize("request_string, expected_request_type, expected_resource_path, expected_protocol_type", [("GET / HTTP1.1", "GET", "/", "HTTP1.1"), ("POST /register HTTP2.0", "POST", "/register", "HTTP2.0")])
def test4(request_string, expected_request_type, expected_resource_path, expected_protocol_type):
    http_request = reqstr2obj(request_string)
    assert isinstance(http_request, HTTPRequest)
    assert http_request.request_type == expected_request_type
    assert http_request.resource_path == expected_resource_path
    assert http_request.protocol_type == expected_protocol_type


def test5():
    request_string = "GET/HTTP1.1"
    http_request = reqstr2obj(request_string)
    assert http_request is None

    request_string = "POST/ HTTP1.1"
    http_request = reqstr2obj(request_string)
    assert http_request is None

    request_string = "GET / HTTP1.1 AAA"
    http_request = reqstr2obj(request_string)
    assert http_request is None


def test6():
    request_string = "DOWNLOAD /movie.mp4 HTTP1.1"
    with pytest.raises(BadRequestTypeError):
        reqstr2obj(request_string)

    request_string = "CHANGE /movie.mp4 HTTP1.1"
    with pytest.raises(BadRequestTypeError):
        reqstr2obj(request_string)

    request_string = "SET /movie.mp4 HTTP1.1"
    with pytest.raises(BadRequestTypeError):
        reqstr2obj(request_string)


def test7():
    request_string = "POST / HTTP1.4"
    with pytest.raises(BadHTTPVersion):
        reqstr2obj(request_string)

    request_string = "GET / HTTP3"
    with pytest.raises(BadHTTPVersion):
        reqstr2obj(request_string)

    request_string = "POST / HTTP"
    with pytest.raises(BadHTTPVersion):
        reqstr2obj(request_string)


def test8():
    request_string = "GET PATH HTTP1"
    with pytest.raises(ValueError) as error_text:
        reqstr2obj(request_string)
    assert str(error_text.value) == "Path must start with /"


def main():
    pass


if __name__ == '__main__':
    main()
