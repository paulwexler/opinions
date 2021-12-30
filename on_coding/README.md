# On Coding Applications in Python

I remember how I used to write programs
and I know how I try to write them now.
Now I have 45 years of experience
and I've read Georg Polya's "How to Solve It".

Understand the problem.

0. Typically, you are presented with a "User story".\
  It describes the context and what is desired;
  entirely in the end-user's terms.
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

Find the connection between the input and the output.

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

Carry out the plan.

5. Now write the code. \
  Partition the task at hand into independent sub-tasks.
  This is a "breadth-first" recursive technique
  applicable at each stage of the partition.

Examine the solution obtained.

6. Is there a simpler implementation?\
  Are the names correct?
  Is the code fully factored?
  Can the classes encapsulate more details?


## Partitioning the task.

For each task there is the code that does the work,
and there is the code that provides the context for the work to be done.
Focus on the latter
and delegate the former to a sub-task.
Decide on what the sub-task needs and what it returns,
not on how it works.
The code that actually does the work will have to be written,
but its ultimate accessibility and utility
depends on how it is wrapped up.
Defer this coding as long as possible.

The decomposition into sub-tasks is aided by the viewpoint
that every piece of code that does something,
is a particular instance of a more general piece of code.
As you proceed away from the root of the tree of tasks,
the code becomes more general.
Each task understands its situation
and employs sub-tasks with the particulars from the current context.
The sub-tasks process their arguments independently of the caller's context.
In this way, the leaves of the task tree will have no knowledge
of the particulars of the application they are embedded in.

As the decomposition proceeds,
each sub-task must do,
or accomplish,
or be responsible for
exactly one thing.
Its implementation must fit on one screen.

Isolate the external interfaces.
Encapsulate the knowledge required to use the external resource.
That knowledge should be centralized
and not sprinkled throughout the implementation.

Keep the code factored as you go.
When you have to do the same thing again only slightly differently,
do not cut-paste-tweak.
Instead, parameterize the operation
and call it with different arguments.


## Simple example.

As network admin, I need to send log files to a 3rd party auditor.
These files are text files with one log entry per line.
They contain IP addresses as well as passwords
and these must be redacted for security.
The files are huge and must be processed in a pipeline.
A program is required which reads the logs on stdin,
and writes the redacted logs to stdout.

The redaction is straight forward.
* All IP addresses must have their digits replaced with "X".\
  IP addresses are 4 8-bit numbers (0-255) separated by ".".
* All passwords must be replaced with "REDACTED".\
  The passwords are encoded in a JSON dict
  as the value of the "password" key (using a case-insensitive match).

This example is simple because there is no error handling.
The opening and management of the files will be handled by the pipeline
of which this program will be a part.

    if __name__ == '__main__':
        import sys

        LineRedactor(sys.stdin, sys.stdout)()

The mainline needs to process stdin and stdout
so it instantiates `LineRedactor` with `sys.stdin` and `sys.stdout`
and then calls it.

`LineRedactor` does not know about stdin and stdout,
it is more general and takes infile and outfile arguments.
This generalization is useful because now `LineRedactor`
can be run independently of `sys` 
as for example
in a test suite using StringIO instances as files.

`LineRedactor.__call__` will redact the input file a line at a time.
`LineRedactor` is an instance of a more general program,
`LineFilter`, which filters its input a line at a time.

    class LineFilter:
        def __init__(self, infile, outfile):
            self.infile = infile
            self.outfile = outfile

        def __call__(self):
            for line in self.infile:
                self.outfile.write(self.filter(line))

        def filter(self, line):
            raise NotImplementedError


    class LineRedactor(LineFilter):
        ...
        def filter(self, line):
            ...


There is no point in deriving LineFilter
from a more general class, perhaps Filter,
as we've already achieved our purpose
in that LineFilter only does one thing
and it frees LineRedactor to only implement the redaction.

We'll use the regular expression substitution method re.sub
to replace the passwords and IP addresses.
We'll replace the passwords first in case they happen to match an IP.

`repl`, the replacement string or function,
may reference groups in the `pattern_string`,
so ideally both should be defined in the same place.
The problem with using

    def filter(self, line):
        re.sub(pattern_string, repl, line)

is that compilation of a pattern string into a pattern is costly
and ought to take place during initialization,
not inside a loop.
The solution is a `Replacer` class
which is initialized with both
and invokes `re.sub` when called.
Additionally, it isolates and encapsulates the use of `re`.

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
                        '.' if c == '.' else 'X' for c in match.group(1)))
        replace_password = Replacer(
                pattern_string=r'(?i)("password": )"(.*?)"',
                repl=r'\1"REDACTED"')

        def filter(self, line):
            return self.replace_ip(self.replace_password(line))
