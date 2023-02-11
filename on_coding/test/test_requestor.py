import pytest
import requests
import simcm

import requestor
from requestor import Requestor

class MockResponse:
    """ A requests.request response.
    Just the parts we need.
    """
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text
        self.reason = 'just testing'

def send_request(req: Requestor, request_args=None, response_template=None):
    request_args = request_args or dict(url='test', method='GET')
    response_template = response_template or {200: dict}
    return req.send(request_args, response_template)
    
def test_requestor():
    req = requestor.Requestor()
    with simcm.Simulate(
            target_string='requests.request',
            target_globals=dict(requests=requests),
            response_list=[
                    MockResponse(status_code=200, text='{}'),
                    MockResponse(status_code=400, text='{}'),
                    MockResponse(status_code=200, text='{bad json}')]):
        response_obj, status_code = send_request(req)
        assert response_obj == {}
        assert status_code == 200
        with pytest.raises(RuntimeError) as exc:
            send_request(req)
        result = str(exc.value)
        expect = 'Unexpected status code 400'
        assert result.startswith(expect)
        with pytest.raises(RuntimeError) as exc:
            send_request(req)
        result = str(exc.value)
        expect = 'Unable to JSON decode:'
        assert result.startswith(expect)
