'''
Send request, validate response.
'''

import json

import requests

import nested_validator

class Requestor:
    '''
    Validate request response against a request template
    '''
    class_validator = nested_validator.NestedValidator

    def __init__(self):
        self.validator = self.class_validator()

    @staticmethod
    def error(
            error: str,
            response: requests.Response,
            request_args: dict,
            response_template: dict) -> str:
        '''
        return formatted error messsage.
        '''
        try:
            obj = json.loads(response.text)
            prettytext = json.dumps(obj, indent=4)
        except json.decoder.JSONDecodeError:
            prettytext = response.text
        return (
                f'{error}\n'
                f'{response.status_code} {response.reason}\n'
                f'{json.dumps(request_args, indent=4)}\n'
                f'{response_template}\n'
                #f'{json.dumps(response_template, indent=4)}\n'
                f'{prettytext}')

    @staticmethod
    def request(request_args: dict) -> requests.Response:
        '''
        send `request_args` using requests.request
        return response (requests.Response instance)
        '''
        response = requests.request(**request_args)
        return response

    def send(self, request_args: dict, response_template: dict):
        '''
        Send request, validate response
        return obj, status_code or raise RuntimeError
        obj - object decoded from JSON response.
        status_code - HTTP status code
        '''
        response = self.request(request_args)
        try:
            if response.status_code in response_template:
                obj = json.loads(response.text) if response.text else None
                error = self.validator(
                        obj,
                        response_template[response.status_code])
            else:
                error = f'Unexpected status code {response.status_code}'
        except json.decoder.JSONDecodeError as exc:
            error = f'Unable to JSON decode: {exc}'
        if error:
            raise RuntimeError(self.error(
                    error,
                    response,
                    request_args,
                    response_template))
        return obj, response.status_code
