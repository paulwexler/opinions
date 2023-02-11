# On Readability

Most programmers would agree that "Readability counts" [^1].
What makes code "readable"?
Python made a leap forward in readability
by enforcing the indentation of code blocks.
Why is that more readable?
The answer comes from music notation.

There exists a deep analogy between
reading a program to understand what it does,
and reading music to realize the composer's intent.
While music notation has had centuries to develop,
coding has had only decades.

A good manuscript maintains a consistant redundency
between the formal rules
and the informal style.
For example,
formally, the half note gets two beats
and has a hollow notehead,
and the quarter note gets one beat
and has a solid notehead.
Informally,
the half note receives more horizontal space
between it and the next note
than the quarter note does.
The result is that you do not have to read every note;
you can "see it at a glance" [^2].

Readable code is code you can "see at a glance".
You do not have to read every token,
you can just see it.

Use vertical space strategically.
It is an extension of what makes indentation so powerful.

1. Double indent continuation lines
   so they do not obscure the shape of the block.
2. When there are several arguments to a function call,
   or when they do not fit on a (79 character) line,
   put each argument on its own (doubly-indented) line.
   It is far easier to scan the vertical space a function uses
   than to count its commas.
   ```python
   >>> scanable_code = code(
   ...         which_uses,
   ...         vertical_space,
   ...         strategically_so,
   ...         readable=True)

   >>> message_string = (
   ...         "This string is broken up into"
   ...         " smaller pieces so scrolling is"
   ...         " not necessary to see all of it."
   ...         " Please note the leading spaces.")
   ```
3. When an expression is complicated,
   break it up into one idea per line.
   ```python
   >>> value = do_something_to(
   ...         some_value if some_condition(
   ...                 of,
   ...                 some,
   ...                 args)
   ...         else some_computation(
   ...                 of_some,
   ...                 other_args))
   ```
4. Limit methods to a single screen.
   Break it up into smaller methods if it does not fit.
   "Bugs" creep in between the screens,
   so it is best when you can see the entire method at once.
   Here is a surprisingly accurate heuristic:
   ```python
   number_of_mistakes = 2 ** (number_of_screens - 2)

[^1]: [The Zen of Python.] (https://www.python.org/dev/peps/pep-0020/)

[^2]: G. Polya, "How to Solve It". Princeton University Press ISBN 0-691-02356-5

