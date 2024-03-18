# On Coding Applications in Python

Georg Polya’s brilliant book “How to Solve It”
provides a set of techniques for how to solve mathematical problems
that you have never encountered.
It’s a way of thinking about problems,
not an exploration of particular mathematical topics.

This write up is my effort
to apply Polya’s method to application programming.
It is also a distillation of my 45 years of experience
writing and debugging applications.
My intention is to provide a generalist, step-by-step,
yet recursive approach
for implementing resilient solutions to problems.
I have provided examples in Python to illustrate key concepts.

Programming is different from mathematics.
There is a difference between "prototype" coding and "production" coding.
When you prototype the goal is knowledge, not a usable program.
None of the prototype code will survive into the production version.
You prototype to learn how to use a resource,
to convince yourself you know the code necessary to utilize the resource
to solve the problem at hand.

New programmers, lacking the confidence that comes from experience,
focus on coding up a usable program as fast as possible.
They produce a "prototype" version
which embodies some useful piece of functionality,
and runs to completion,
and all is well until it is actually used,
or used in a different context,
and then the real world sets in
and the input domain is different than expected,
or the output requirements have changed.

What happens then, as the code gets patched to handle changes,
is its complexity grows.
Then the code acquires complexity because of its implementation,
and not because of the complexity inherent
in the problem it is trying to solve.
It just gets increasingly harder to debug, maintain, and adapt.

To get the program to embody some piece of functionality
is the easy part.
What takes finesse is to package that functionality
so the program is resilient to change.
A program is resilient when small changes to the requirements
require small changes to the implementation.
"Coupling" between components is the obstacle to resilience.
The tighter the coupling the harder it is to make changes.

A strategy is required to develop resilient code.
Consider the prototyping experiments as "bottom-up" research,
and write the program "top-down".
Start with the mainline.
It will contain all of the particulars
and all of the assumptions required
to use the components it employs.
Develop cohesive components
and strive always to reduce their coupling.

**_Understand the problem._**

0. Typically, you are presented with a "User story".\
  It describes the context and what is desired
  in the end user's terms.
  Also typically, only the "happy" path is described in any detail.
  The end user is usually unconcerned with possible "error" paths
  because they don't occur often enough in the existing situation.

1. You must be aware of the context the program will run in.\
  In particular you must firm up the response to errors.
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
  Each sub-task requires a statement as in 2.,
  a plan as in 3.,
  and a solution as in 4.
  The goal is a collection of loosely coupled
  and highly cohesive components.

**_Examine the solution obtained._**

6. Is there a simpler implementation?\
  Can the coupling be reduced?
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

At each stage the problem is either solved or transformed into finding
an effective axis of generalization.
Edsgar Dijkstra considers finding
the greatest common divisor of 111 and 259
in _Chapter 0 Executional Abstraction_ of _"A Discipline of Programming"_
published by Prentice-Hall.
He chooses a GCD-computer over a 111-and-259-processor
and discusses
'what characteristics make a generalization "helpful for our purpose"'.

For me personally, the axes appear spontaneously
as a creative act driven by the desire to generalize
and at this time I am unable to say more about it.

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

## doc strings

As a programming habit,
I always write the doc strings first,
then I implement what was described.
Writing the doc string is actually step 4. during the recursive partitioning.

`pylint` requires doc strings so I use them.
And I always lint my code before testing it.
So I try to write code
so that it passes the linter the first time.

How do you know what to put in a doc string?
You can be sure you completely understand a piece of code
when you know what it does, how it does it, and why it is needed.

What, how, why.

Of these, "why" is the most important, and "how" the least.
In a language as expressive as Python, the "how" is the code itself.
It is rare to need in-line comments in Python.
In other words you seldom need a "how" for the "how".
The doc string should be the "what".
This almost always includes a description of the input and output.
As for the "why",
it derives from the context of the caller's "what",
and it should be completely transparent to the component's "what".
The "why" comes from your imagination
and it constitutes your understanding
of the component's relation to the implementation.

Remember that Python's `help` apparatus displays the doc strings.
Start the interpreter, import your module, run `help`
and make sure what you see explains what the module does
and how to use it.
```python
    >>> import some_module
    >>> help(some_module)
    ...
    >>> help(some_module.some_component)
    ...
```
## Debugging

I started writing programs in "assembler".
In those days a debugger was indispensable.
In the first place it could display information on the teletype.
In those days you could crash the operating system
by running a program with a mis-spelled label.
A program could run fine when linked with the debugger,
and fail miserably without it;
then it took some ingenuity
to locate the cause of the memory leak.

When "C" arrived, a lot of the memory management was automated,
but the program still had to manage memory
and could still mysteriously crash.
Debuggers were useful because
you could effectively add dynamic print statements
without recompiling.
But for the most part,
I found that well placed `printf` statements
could eliminate the need for a debugger.

With "Python",
I have never used a debugger.

When the program crashes, a stack trace is output.
Since my programs are constructed
out of cohesive components with loose coupling,
it is easy to discover the root cause of the crash.
The trace lists the error, file, method, and line number which crashed.
When I look there,
if there is still any mystery,
I can put an output statement at the start of the method
to show its input arguments
and then run the program again.
If the input is correct, the error is in the method;
if not, the trace shows the line number of the caller,
so I can continue this search technique from there.

The point is that the stack trace directs the search,
and since each method is cohesive and loosely coupled,
it can be understood in isolation.
You'll know if its input is valid or not,
and you'll know what it is supposed to do
because that information is in the doc string.
So the search for the cause of the error can proceed
without having to understand the entire program.

If the program was not component based,
the stack trace might point you to a line number
in a `while` in a `for` in a `for` in a `while`,
and then you might wish you had a debugger
so you could continue from breakpoint to breakpoint
hunting for the bug with the wrong end of the telescope.

## Error Handling

All too often application development proceeds by implementing the "happy" path first
with no regard to error handling.
And when the error handling is finally added, no thought is given to the content of the message
besides indicating that an error happened.
These are errors which probably never happened during development,
or perhaps only appeared during the initial prototyping of the resource,
so an "it doesn't matter, ain't never gonna happen" attitude often prevails.

Not handling errors is almost the essence of prototyping:
you are the error handler in real-time
as you learn how to use the resource.

But deferring or omitting the error handling in application code is always short-sighted.
The extra time it takes to code proper error handling
will be paid back multiple times in the time saved during debugging.
Error handling is not a nice extra "bell" or "whistle";
it's foundational and offers the quickest path to completion!

Good error handling is always required
because even though it seems to be working now,
in time, things will go wrong.
A configuration file gets corrupted, a disk fills up, permissions change, ...
You want the application to not simply be a victim,
but to actually aid in discovering the path to recovery.

Compare

* `FAILED :(`
* `Unable to read configuration.`
* `init: read /some/path/config.cfg -> "Permission denied"`

If you want the application to be robust,
then whenever the application calls an external resource
the return status should be checked.
If it is a failure, the error message should include at a minimum

1. The caller's view of what was attempted.
2. The resource that was called (including all arguments if any).
3. What the resource returned.

Put another way,
the message should include whatever you would display
if you were in a debugger at a breakpoint where the error occurred.

This information will serve several purposes.
First, it will enable the developer to rapidly fix the code
when the error is due to an improper call to the resource.
Second, it will help operators diagnose the root of the problem
should this error suddenly appear in production.
Finally, if the error is actually in the resource,
then the message will serve as a starting point
for developers of the resource to begin debugging it.

## Examples

My intent is to illustrate the concepts of coupling and cohesion
and the advantages of loose coupling and high cohesion.
The examples given are small and I suppose it could be argued
that it does not matter how they were constructed
as long as they work.
But the advantages of managing coupling and cohesion
increase with the size of the project.
More importantly, after time,
a collection of components will emerge
which can "cover" the problem space, or nearly so.
Then new problems can be solved
by using the existing components
and almost no new code needs to be developed.

The examples shown have gone through several iterations
(steps 2 through 6)
and do not reflect the growing pains that transpired
to arrive in their present form,
however they do demonstrate implementations constructed with
highly cohesive and loosely coupled components.

The actual code includes doc strings throughout
and scores 10.00/10 with pylint,
but the following examples omit the doc strings
because the code is annotated.

### A filter example.

As network admin, I need to send log files to a 3rd party auditor.
These files are text files with one log entry per line.
They include IP addresses as well as passwords
and these must be redacted for security.
The files are huge and must be processed in a pipeline.
A program is required which reads the logs from stdin,
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
                pattern_string=r'(?i)("password": ?)"(.*?)"',
                repl=r'\1"REDACTED"')

        def filter(self, line):
            return self.replace_ip(self.replace_password(line))
```

Functionally we are done, but there is an unintended "coupling"
that can be easily reduced
by the technique of factoring executable code into data.

Note that `LineRedactor.filter` "knows" a lot about what the program does.
It "knows" `replace_ip`, `replace_password`,
and to use `replace_password` first.
This coupling
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
Instead we'll use `replacer`, a `dict` of `Replacer`
indexed by replacer name,
so `filter` can reduce `line` by `self.replacer.values()`.

```python
        replacer = dict(
                replace_password=Replacer(
                        pattern_string=r'(?i)("password": ?)"(.*?)"',
                        repl=r'\1"REDACTED"'),
                replace_ip=Replacer(
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
                                    for c in match.group(1))))

        def filter(self, line):
            for replacer in self.replacer.values():
                line = replacer(line)
            return line
```

Finally,
`LineRedactor.filter` expects `replacer` to be a `dict` of callables
which take one string argument and return a string.
That's a lot of coupling best managed with a class

```python
    class Redaction(dict):
        '''
        A dict of Replacer that reduces a given line with them
        when called.
        '''
        def __call__(self, line):
            for replacer in self.values():
                line = replacer(line)
            return line

        def __setitem__(self, key, value):
            assert isinstance(value, Replacer)
            super().__setitem__(key, value)


    class LineRedactor(LineFilter):
        redaction = Redaction(
                ...

        def filter(self, line):
            return self.redaction(line)

```

Here is the complete program: [redact.py][redact_py]

Please note that
the redaction details are encapsulated in `LineRedactor.redaction`.
So even though `LineRedactor` as implemented
contains a specific redaction,
it is in a real sense just the "default" redaction
which can be overwritten by sub-classing:

```python
    class MyLineRedactor(LineRedactor):
        redaction = Redaction( ... )
```

### A `requests` example

The `requests` module provides a clean interface
to send and receive data to and from web APIs.

You send requests by calling `requests.request(...)`
with keyword arguments.
Either a `requests.exception.RequestException` is raised
when the data exchange did not complete
or a `requests.Response` object is returned.

A `RequestException` can be raised for a variety of reasons.
The url could be wrong, the request might be blocked by a firewall,
the site could be down, the request could have timed out, or some other error.
Some applications might catch `RequestException` or specific subclasses of it
and attempt to handle these errors,
however for many applications,
there is no need to handle these exceptions,
as they are due to configuration errors
or events beyond the control of the program
and the stack trace which shows the `RequestException`
is entirely sufficient.

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
            403: object,
            404: [str]}
```
If the response matches the template,
the application can dispatch on the status code
and navigate with impunity.
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

The application code which interprets the status code
is necessarily tightly coupled to the response template.
It must know what the acceptable status codes are
and what to do in each case.
This coupling could be removed
(using the technique of factoring executable code into data)
by modifying the response template
to associate a handler (i.e. a method to call) with each status code.

However, in practice, the application's logic
follows common sense,
and this coupling is entirely manageable.
For example, a GET request may accept a 200
and return the requested object,
or accept a 404 when the object is not found.

Proceeding from the top down, the implementation falls neatly into two components.

1. A Requestor

   * Its `send` method handles any errors from sending the request. \
     It returns (the JSON decoded response object, status code) \
     or it raises `RuntimeError`.
   * Its `request` method isolates and encapsulates the use of `requests`.
   * Its `error` method returns a formatted error string.
   * Besides decoding the JSON response
     it need not know what a valid response is,
     as it delegates that to the Validator.

2. A Validator which validates the `Response` object
   to ensure it matches the `response_template`.

`requestor.py`
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

    @staticmethod
    def request(request_args: dict) -> requests.Response:
        response = requests.request(**request_args)
        return response

    def send(self, request_args: dict, response_template: dict):
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
```
Here is the complete program: [requestor.py][requestor_py]

`NestedValidator.__call__` must traverse the `template` recursively,
comparing it to the `obj`,
and validating as it goes.

* If the `template` is a `type`, the `obj` must be an instance of that `type`,
  otherwise the `type` of the `obj` must equal the `type` of the `template`.
  This implies that if the `template` is `object`, then the `obj` is valid.
* If the `template` is a `dict`, every key must be in the `obj`
  and their values must match.
* If the `template` is a `list`, every element in `obj` must match `template[0]`.

It returns the first error it finds
or it returns an empty string if it completes the traversal.

As it traverses, it must keep track of its location in case there is an error.

The error should be self-explanatory in the context in which it appears.
`{location of error in the nested object}: {error message}` is sufficient.

A stack of locations is needed to keep track of the nested location,
and a list of locations is needed to print them as a dot-delimited string.
So a `list` will suffice for the implementation.

`nested_validator.py`
```python
class NestedLocation(list):
    def __str__(self):
        return '.'.join(str(location) for location in self)

    def push(self, location):
        self.append(location)


class NestedValidator:
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
        nested_location = (
                f'{self.nested_location}: ' if self.nested_location
                else '')
        self.error = f'{nested_location}{error}'

    def validate(self, obj, template):
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
        for index, element in enumerate(obj):
            self.nested_location.push(index)
            self.validate(element, template[0])
            self.nested_location.pop()
            if self.error:
                break
```
Here is the complete program: [nested_validator.py][nested_validator_py]

Here is the test suite for both examples: [test_suite][test_suite]

### A CLI example

This example will contrast two designs.
We can do so without actually writing the code.
It is worth noting that the code that would actually "do the work"
would be essentially the same in either design,
although the design with greater cohesion
will likely require less actual code.

We need a CLI program to put our ducks in a row.
We'll have to manage those ducks.
Receive them, weigh them, feed them,
and ultimately sort them,
and other operations as well.

#### First approach: A Parser and a Master

We'll parse the command line arguments
and then dispatch to the selected command.

We'll create `class DuckParser(argparse.ArgumentParser)` to parse the arguments
and obtain a `namespace`.
It will ensure that `namespace.command` is a valid command
and that all options and required arguments for that command
are validated and present in the `namespace`.

Since the various commands will share the same model of "duck"
they will share some code, so they can be methods of say `class DuckMaster`
with `__init__(self, namespace)`,
and `__call__(self)` which calls the indicated command.
The command will extract its arguments from the namespace
now `self.namespace` and go to work.

The mainline will instantiate the `DuckParser`
with `sys.argv[1:]`
and call it to get the `namespace`.
Then it will instantiate the `DuckMaster` with the `namespace`
and call it.

There are problems with this approach.

* One clue is that both the DuckParser and DuckMaster
  have to dispatch on the indicated command.
  This is a symptom of the tight coupling between them.
* The DuckParser is not cohesive
  as it knows the options and arguments
  of all the supported commands.
* The DuckMaster is not cohesive as it contains
  all of the commands and all the common code.

In order to add a new command
we'd have to understand the entire design
and add the command to both DuckParser and DuckMaster.

This design does not manage the coupling that must exist
between the parser for a command and the code
which operates on the parsed namespace.

#### Second approach: A Command and a Master

`class DuckCommand` will be the base class
and each command (a method of DuckMaster in the first approach),
will now be a subclass.

`class DuckMaster` will be instantiated with
the command line arguments `sys.argv[1:]`.
`DuckMaster.__init__` need only parse its first argument `args[0]`
to ensure it is a valid command name,
and then instantiate the class associated with the command name
with the remaining arguments `args[1:]`.

`DuckMaster.command` will be a class variable,
a `dict` mapping a command name to a subclass of `DuckCommand`.
This `dict` could be hard-coded or, for less coupling,
derived by introspecting
the subclasses of `DuckCommand`.

`DuckMaster.__call__` will call the instantiated class.
While the call to the instantiated class
could be made by `__init__`,
I prefer to separate the (static) "setup"
and the (dynamic) "execution"
with `__init__` and `__call__`.
It makes testing easier,
and it makes calling the same instance twice feasible.
It is worth the time spent deciding
what belongs in `__init__`,
and what belongs in `__call__`.

The mainline now needs only to instantiate and call `DuckMaster`.
```python
    DuckMaster(sys.argv[1:])()
```

`DuckCommand` will contain all the common code
formerly in `DuckMaster`,
as well as two methods each subclass must overwrite:
`get_namespace` and `__call__`.
These methods will be tightly coupled
as the `namespace` will contain exactly the attributes
that `__call__` will act on.
But now they will be in the same subclass,
and they are the only methods each subclass is required to implement.
Now the subclass is cohesive as
it is responsible for implementing a single command
in its entirety.

`DuckCommand.__init__(self, args)` will call `self.get_namespace(args)`
to get the namespace by parsing the args.
`DuckCommand.__call__(self)` will implement the actual duck command.

Now, to add another command,
we'd only have to declare a new subclass of `DuckCommand`
and implement its `get_namespace` and `__call__` methods.

The point worth noting here is that
the difference is in the packaging.
The code that "does the work"
will be essentially the same in both designs.
This is why (after the prototyping experiments have revealed
the light at the end of the tunnel)
this code should be deferred as long as possible.

## Conclusion

Applications are useful when they solve problems in the real world.
The world however, is phenomenon rich;
the simplest things are more complicated than they first appear.

You've written a program to put your ducks in a row.
You thought back at Step 0
that you understood what a duck was
but then it turns out that while sorting
ducklings must remain with their mothers.
What must change to handle this?
What about the Canadian clients?
(Ducks from Quebec are measured in kilograms,
and from Ontario in Imperial pounds).
What about the Muscovy ducks which are measured in centimeters?

The world is complicated
and it is immensely difficult to anticipate all the complexities
which may arise
(seemingly out of nothing)
in any given domain.

This is why striving for resilience in the implementation is so important.

[nested_validator_py]: ./nested_validator.py
[redact_py]: ./redact.py
[requestor_py]: ./requestor.py
[test_redact_py]: ./test/test_redact.py
[test_suite]: ./test
