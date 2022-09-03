# On Coding Applications in Python

I remember how I used to write programs
and I know how I try to write them now.
Now I have 45 years of experience
and I've read Georg Polya's "How to Solve It".

Experience counts.
It always helps if you've solved a similar problem in the past.
But I think more importantly, experience gives you the confidence
to defer the actual coding until you understand the problem.
So it doesn't take experience to do this, just confidence.

There is a difference between "prototype" coding and "production" coding.
When you prototype the goal is knowledge, not a usable program.
None of the prototype code will survive into the production version.
You prototype to learn how to use a resource,
to convince yourself you know the code
necessary to utilize the resource
to solve the problem at hand.

New programmers, lacking the confidence that comes from experience,
focus on coding up a usable program as fast as possible.
The resulting program will embody some useful piece of functionality
and all is well until it is actually used, or used in a different context,
and then the real world sets in
and the input domain is larger or different,
or the output requirements have changed.

What happens then, as the code gets patched to handle changes,
is its complexity grows.
Then the code acquires complexity
because of its implementation,
and not because of the complexity inherent in the problem it is trying to solve.
It just gets harder and harder to debug, maintain, and adapt.

To get the program to embody some piece of functionality is the easy part.
What takes finesse is to package that functionality
so the program is resilient to change.
A program is resilient when small changes to the requirements
require small changes to the implementation.
"Coupling" between components is the obstacle to resilience.
The tighter the coupling the harder it is to make changes.

A strategy is required to develop code with minimal coupling.
Consider the prototyping experiments as "bottom-up" research,
and write the program "top-down".
Start with the mainline.

**_Understand the problem._**

0. Typically, you are presented with a "User story".\
  It describes the context and what is desired
  in the end user's terms.
  Also typically, only the "happy" path is described in any detail.
  The end user is usually unconcerned with possible "error" paths
  because they don't occur often enough in the existing situation.

1. You must firm up the response to errors.\
  On bad input or network or other errors,
  do you log and ignore it?
  Abort?
  Can the program pick up from where it left off?
  Must you undo what's been done in order to try again?
  All of this takes precedence over any of the details in the "happy" path.

2. Then state the task at hand.\
  Be as brief as possible.
  What is the desired outcome?
  What is the input?
  Use the appropriate terms from the domain at hand unambiguously.
  Avoid aliases and synonyms.
  Be rigorous.

**_Find the connection between the input and the output._**

3. Devise a plan.\
  First make a model.
  Map the user's objects onto programmable objects
  so that the desired outcome can be obtained
  by a series of definite operations on those objects.
  Appropriate classes will emerge from this analysis.
  Each class will define an object
  and implement the operations on it.
  It will provide a layer of abstraction
  so operations can be referenced by name
  (perhaps qualified with arguments),
  and knowledge of the details is not required.

4. State the solution.\
  Derive the desired result from operations on the objects.

**_Carry out the plan._**

5. Now write the code. \
  Partition the task at hand into independent sub-tasks.
  This is a "breadth-first" recursive technique
  applicable at each stage of the partition.
  Each sub-task requires a plan as in 3.
  and a solution as in 4.
  The goal is a collection of loosely coupled
  and highly cohesive components.

**_Examine the solution obtained._**

6. Is there a simpler implementation?\
  Are the names correct?
  Is the code fully factored?
  Can the classes encapsulate more details?
  Are the classes too complex?


## Partitioning the task.

For each task there is the code that does the work,
and there is the code that provides the context for the work to be done.
Focus on the latter
and delegate the former to a sub-task.
Decide on what the sub-task needs and what it does or returns,
not on how it works.
The code that actually does the work will eventually be written,
but defer this coding as long as possible.

The decomposition into independent sub-tasks is aided by the viewpoint
that every piece of code that does something,
is a particular instance of a more general piece of code.
As you proceed away from the root of the tree of tasks,
the code becomes more general.
Each task understands its situation
and employs sub-tasks with the particulars from its current context.
The sub-tasks process their input independently of their caller's context.
In this way, the leaves of the task tree will have no knowledge
of the particulars of the application they are embedded in.

As the decomposition proceeds,
each sub-task must do,
or accomplish,
or be responsible for
exactly one thing <sup id="a1">[1](#f1)</sup>.
Its implementation must fit on one screen.

Isolate the external interfaces.
Encapsulate the knowledge required to use an external resource.
That knowledge should be centralized
and not sprinkled throughout the implementation <sup id="a2">[2](#f2)</sup>.

Keep the code factored as you go.
When you have to do the same thing again only slightly differently,
do not copy-paste-tweak.
Instead, parameterize the operation
and call it with different arguments.

Factoring the code will generally consolidate the implementation,
however,
the need for factorization may reveal
the need for a higher order object
not yet considered by the previous analysis.
It is precisely at this juncture,
as well as when the input domain or the output requirements change,
that the choice of loosely coupled,
highly cohesive (and necessarily small),
components pays off:
some components may be altered (it won't take long),
others may be scrapped (so what!),
and new ones may be written (it won't take too long),
but everything else remains unchanged!

<a name="f1"><sup>1</sup></a>
<sup>
: The goal is highly cohesive components.
If a component does two things, it is half as cohesive as if it did one thing.
Its cohesion deteriorates exponentially
because the number of possible interactions
between the things it does grows exponentially.
</sup>
[*](#a1)

```python
component.cohesion = 2 ** (1 - component.number_of_things_it_does)
```

<a name="f2"><sup>2</sup></a>
<sup>
: Your knowledge of the resource may grow,
or patterns of error handling may be required
for errors which did not appear
during the prototyping of the resource
but do appear during actual use.
In any case, if the usage is isolated,
the isolate can be fixed or improved
independently of its users.
</sup>
[*](#a2)

## A filter example.

As network admin, I need to send log files to a 3rd party auditor.
These files are text files with one log entry per line.
They contain IP addresses as well as passwords
and these must be redacted for security.
The files are huge and must be processed in a pipeline.
A program is required which reads the logs on stdin,
and writes the redacted logs to stdout.

The redaction is straightforward.
* All IP addresses must have their digits replaced with "X".\
  IP addresses are 4 8-bit numbers (0-255) separated by ".".
* All passwords must be replaced with "REDACTED".\
  The passwords are encoded in a JSON dict
  as the value of the "password" key (using a case-insensitive match).

This example is simple because there is no error handling.
The opening and management of the files will be handled by the pipeline
of which this program will be a part.

The mainline needs to process stdin and stdout
so it calls a `LineRedactor` instantiated with `sys.stdin` and `sys.stdout`.

```python
    if __name__ == '__main__':
        import sys

        LineRedactor(sys.stdin, sys.stdout)()
```

`LineRedactor` does not know about stdin and stdout,
it is more general and takes infile and outfile arguments.
This generalization is useful because now `LineRedactor`
can be run independently of `sys`
as for example
in a [test suite][test_redact_py] using `io.StringIO` instances as files.

`LineRedactor.__call__` will redact the input file a line at a time.
`LineRedactor` is an instance of a more general program,
`LineFilter`, which filters its input a line at a time.

```python
    class LineFilter:
        def __init__(self, infile, outfile):
            self.infile = infile
            self.outfile = outfile

        def __call__(self):
            for line in self.infile:
                self.outfile.write(self.filter(line))

        def filter(self, line):
            # return the filtered line
            raise NotImplementedError


    class LineRedactor(LineFilter):
        def filter(self, line):
            ...
```

There is no point in deriving `LineFilter`
from a more general class, perhaps `Filter`,
as we've already achieved our purpose
in that `LineFilter` only does one thing
and it frees `LineRedactor` to only implement the redaction.

We'll use the regular expression substitution method `re.sub`
to replace the passwords and IP addresses.
We'll replace the passwords first in case they happen to match an IP.

`repl`, the replacement string or function,
may reference groups in the `pattern_string`.
This coupling is unavoidable
so ideally both arguments should be declared in the same place.
The problem with calling `re.sub` directly, as in

```python
    def filter(self, line):
        filtered = re.sub(pattern_string, repl, line)
        ...
        return filtered
```

is that compilation of a pattern string into a pattern is costly
and ought to take place during initialization,
not inside a loop.
A solution is the `Replacer` class
which is initialized with `pattern_string`, and `repl`,
and invokes `re.sub` when called.
Additionally, it isolates and encapsulates the use of `re`.

```python
    import re

    class Replacer:
        def __init__(self, pattern_string, repl):
            self.pattern = re.compile(pattern_string)
            self.repl = repl

        def __call__(self, string):
            return self.pattern.sub(self.repl, string)


    class LineRedactor(LineFilter):
        replace_ip = Replacer(
                # With an abundance of caution,
                # the word delimiter "\b" which might normally
                # delimit a regex for an IP address, is omitted here.
                pattern_string=(
                        r'('
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
                        r'('
                        r'\.'
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
                        r'){3}'
                        r')'),
                repl=lambda match: ''.join(
                        '.' if c == '.' else 'X'
                                for c in match.group(1)))
        replace_password = Replacer(
                pattern_string=r'(?i)("password": )"(.*?)"',
                repl=r'\1"REDACTED"')

        def filter(self, line):
            return self.replace_ip(self.replace_password(line))
```

Functionally we are done, but there is an unintended "coupling"
that can be easily reduced
by factoring executable code into data.

Note that `LineRedactor.filter` "knows" a lot about what the program does.
It "knows" `replace_ip`, `replace_password`,
and to use `replace_password` first.
The coupling
(between `LineRedactor.filter` and `LineRedactor` class variables)
would only grow if we added another `Replacer` instance.
We'd have to add a call to it in `filter`.

We can reduce this coupling by noting that `filter`
does not need to know what each `Replacer` does.
It just needs to reduce `line` by a list of `Replacer`.
The author of the list cares about the order of the replacements,
but `filter` does not need to.

While we could put the `Replacer` instances in a `list`,
it would then be unclear what each instance does.
Instead we'll use `replacers`, a `dict` of `Replacer`
indexed by an informative replacer name,
so `filter` can reduce `self.replacers.values()`.

```python
        def filter(self, line):
            for replacer in self.replacers.values():
                line = replacer(line)
            return line
```

Here is the complete program: [redact.py][redact_py]

## A `requests` example

The `requests` module provides a clean interface
to send and receive data to and from web APIs.

You send requests by calling `requests.request(...)`
with a list of keyword arguments.
Either a `requests.exception.RequestException` is raised
when the data exchange did not complete
or a `requests.Response` object is returned.

A `RequestException` can be raised for a variety of reasons.
The url could be wrong, the request might be blocked by a firewall,
the site could be down, the request could have timed out, or some other error.
Some applications might catch `RequestException` or specific sub-classes of it
and attempt to handle these errors,
however for many applications,
there is no need to handle these exceptions,
as they are due to configuration errors
or events beyond the control of the program.

On the other hand, when a `Response` object is returned,
it is the responsibility of the application
to handle it correctly, no matter what it is.

Many web APIs respond with JSON strings which encode nested objects.
Applications can expect the response to have a particular structure
and will be coded accordingly.
However, if the response has an unexpected structure,
perhaps because the site is still under development,
or the API documentation was misunderstood or is incomplete or faulty,
then the code may crash with a `KeyError` or `TypeError`, or some such `Exception`.

Even if the implementation always checks the viability of a reference beforehand:
```python
    if isinstance(data, dict):
        if 'fuzzle' not in data:
            raise MyAppError('Missing key "fuzzle"')
        fuzzle = data['fuzzle']
    else:
        raise MyAppError(f'Expected a dict, got "{data}"')
```
instead of:
```python
    fuzzle = data['fuzzle']
```
then aside from obscuring the code,
the further downstream from the receipt of the response that this sort of error occurs,
the more cryptic the error will appear,
and the more time it will take to understand what happened.

What is needed is the ability for the application to declare what is expected
and then to check the validity of the response as soon as it arrives.

Since the format of the returned data can often depend upon the status code,
and the number of reasonable status codes will be small,
the application's response template will be a dict,
indexed by status code,
whose values are types or objects that the response object must match.

Suppose for example,
when the status code is 200,
the response object is expected to be a dict with a "customers" key
whose value is a list of dicts with keys "name" and "number",
whose values are of types "str" and "int" respectively,
and when the status code is 403 we don't care what the response object is,
and when the status code is 404 the response is expected to be a list of strings,
then the response template would be:
```python
    response_template = {
            200: {'customers': [{'name': str, 'number': int}]},
            403: Any,
            404: [str]}
```
If the response matches the template, the application can navigate it with impunity.
If not, the error message should be sufficient for a developer
to understand the root cause of the error.
It should show:
* what is wrong with the response (from the program's point of view)
* `response.status_code` and `response.reason`
* what was sent
* what was expected
* what was received

This information will enable the developer to either fix the program
or provide proof to the web API that something is amiss.

The implementation falls neatly into two components.
1. A Requestor
   * Its `request` method sends the request and handles errors. \
     It returns (the JSON decoded response object, status code) \
     or it raises `RuntimeError`.
   * Its `send` method isolates and encapsulates the use of `requests`.
   * Its `error` method returns a formatted error string.
   * It need not know what a valid response is, as it delegates that to the Validator.
2. A Validator which validates the `Response` object
   to ensure it matches the `response_template`.

[requestor.py][requestor_py]
```python
import json

import requests

import nested_validator

class Requestor:
    class_validator = nested_validator.NestedValidator

    def __init__(self):
        self.validator = self.class_validator()

    @staticmethod
    def error(
            error: str,
            response: requests.Response,
            request_args: dict,
            response_template: dict) -> str:
        try:
            obj = json.loads(response.text)
            prettytext = json.dumps(obj, indent=4)
        except json.decoder.JSONDecodeError:
            prettytext = response.text
        return (
                f'{error}\n'
                f'{response.status_code} {response.reason}\n'
                f'{json.dumps(request_args, indent=4)}\n'
                f'{json.dumps(response_template, indent=4)}\n'
                f'{prettytext}')

    def request(self, request_args: dict, response_template: dict):
        response = self.send(request_args)
        try:
            if response.status_code in response_template:
                obj = json.loads(response.text) if response.text else None
                error = self.validator(obj, response_template)
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

    @staticmethod
    def send(request_args: dict) -> requests.Response:
        response = requests.request(**request_args)
        return response
```
`NestedValidator.__call__` must traverse the `template` recursively,
comparing it to the `obj`,
and validating as it goes.
* If the template is Any, the obj is valid.
* If the template is a type, the obj must be an instance of that type,
  otherwise the type of the obj must equal the type of the template.
* If the template is a dict, every key must be in the obj
  and their values must match.
* If the template is a list, every element in obj must match template[0].

It returns the first error it finds
or it returns an empty string if it completes the traversal.

As it traverses, it must keep track of its location in case there is an error.

The error should be self-explanatory in the context in which it appears.
`{location of error in the nested object}: {error message}` is sufficient.

A stack of locations is needed to keep track of the nested location,
and a list of locations is needed to print them as a dot-delimited string.
So a list will suffice for the implementation.

`nested_validator.py`
```python
Any = type('Any', (), {})


class NestedLocation(list):
    def __str__(self):
        return '.'.join(str(location) for location in self)

    def push(self, location):
        self.append(location)


class NestedValidator:
    def __init__(self):
        self.nested_location = None
        self.error = None

    def __call__(self, obj, template):
        self.nested_location = NestedLocation()
        self.error = ''
        self.validate(obj, template)
        return self.error

    def load_error(self, error: str):
        nested_location = (
                f'{self.nested_location}: ' if self.nested_location
                else '')
        self.error = f'{nested_location}{error}'

    def validate(self, obj, template):
        if not self.error and not template == Any:
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
        for index, element in enumerate(obj):
            self.nested_location.push(index)
            self.validate(element, template[0])
            self.nested_location.pop()
            if self.error:
                break
```
As it happens, some API's may return a variety of responses for the same request.
For example instead of a list of strings, a single string may be returned.

We can take advantage of the fact that JSON has no tuple type
and use Python's tuple as metadata to request a choice of templates.

Of course if the application's `response_template` allows multiple templates
for the same `status_code`,
then the application must determine what object was actually returned
before it can navigate that object with impunity.

Here is an example of a template which accepts a dict or a list of dicts
which have a "customers" key, or a dict with no "customers" key:
```python
    response_template = {
            200: (
                    {'customers': Any},
                    [{'customers': Any}],
                    dict)}
```
We need only change `validate` to check for a `tuple`, and add `validate_tuple`:
```python
    def validate(self, obj, template):
        if not self.error and not template == Any:
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

    def validate_tuple(self, obj, template_tuple: tuple):
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
```
Here is the complete program: [nested_validator.py][nested_validator_py]

[nested_validator_py]: ./nested_validator.py
[redact_py]: ./redact.py
[requestor_py]: ./requestor.py
[test_redact_py]: ./test/test_redact.py
