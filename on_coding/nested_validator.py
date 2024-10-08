'''
Nested Validator
Compares an object to a template and ensures they match.
'''
import collections


class NestedLocation(collections.deque):
    '''
    >>> loc = NestedLocation()
    >>> loc.push(location)
    >>> loc.pop()
    '''
    delimiter = '.'
    push = collections.deque.append

    def __str__(self):
        return self.delimiter.join(str(location) for location in self)


class NestedValidator:
    '''
    >>> validator = NestedValidator()
    >>> error = validator(obj, template)
    >>> assert isinstance(error, str)
    >>> if error:
    '''
    class_nested_location = NestedLocation

    def __init__(self):
        self.nested_location = None
        self.error = None

    def __call__(self, obj, template):
        self.nested_location = self.class_nested_location()
        self.error = ''
        self.validate(obj, template)
        return self.error

    def load_error(self, error: str):
        '''
        prepend location to error and load into self.error
        '''
        nested_location = (
                f'{self.nested_location}: ' if self.nested_location
                else '')
        self.error = f'{nested_location}{error}'

    def validate(self, obj, template):
        '''
        depth-first traversal of obj,
        load self.error on first error and stop.
        '''
        if not self.error:
            template_type = (
                    template if isinstance(template, type)
                    else type(template))
            if not isinstance(obj, template_type):
                self.load_error(f'Not a {template_type}: {obj}')
            elif isinstance(template, dict):
                self.validate_dict(obj, template)
            elif isinstance(template, list):
                self.validate_list(obj, template)

    def validate_dict(self, obj: dict, template: dict):
        '''
        validate_dict
        '''
        for key in template:
            if key in obj:
                self.nested_location.push(key)
                self.validate(obj[key], template[key])
                self.nested_location.pop()
                if self.error:
                    break
            else:
                self.load_error(f'Missing key "{key}"')
                break

    def validate_list(self, obj: list, template: list):
        '''
        validate_list
        '''
        for index, element in enumerate(obj):
            self.nested_location.push(index)
            self.validate(element, template[0])
            self.nested_location.pop()
            if self.error:
                break
