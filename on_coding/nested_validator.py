'''
Nested Validator
Compares an object to a template and ensures they match.
'''


class NestedLocation(list):
    '''
    >>> loc = NestedLocation()
    >>> loc.push(location)
    >>> loc.pop()
    '''
    def __str__(self):
        return '.'.join(str(location) for location in self)

    def push(self, location):
        '''
        push (a.k.a. append)
        '''
        self.append(location)


class NestedValidator:
    '''
    >>> validator = NestedValidator()
    >>> error = validator(obj, template)
    >>> assert isinstance(error, str)
    >>> if error:
    '''
    def __init__(self):
        self.nested_location = None
        self.error = None

    def __call__(self, obj, template):
        self.nested_location = NestedLocation()
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
        if not self.error and not template == object:
            if isinstance(template, tuple):
                self.validate_tuple(obj, template)
            else:
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
        for key in template.keys():
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

    def validate_tuple(self, obj, template_tuple: tuple):
        '''
        validate_tuple
        error only if all templates in the tuple fail.
        '''
        errors = []
        for template in template_tuple:
            self.error = ''
            self.validate(obj, template)
            if self.error:
                errors.append(self.error)
            else:
                break
        else:
            self.load_error('\n'.join(errors))
