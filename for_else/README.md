# for else

Some people do not like Python's `for else` construct because
there is no natural language equivalent.
However, the construct is very compact, useful, and "pythonic".
Guido found no need to introduce another keyword for it
because `else` is entirely appropriate - once you realize
what the implied `if` must be.

A `for` loop either runs to completion,
or it does not because a `break` was executed.
In this context, an empty loop has run to completion
because a `break` was never executed.

Ordinarily, the code immediately following the `for` block
has no way of deciding whether or not a `break` was executed;
while the code immediately preceding the `break` knows that
the break condition is now true
and is about to break out of the loop.
Therefore the only possible use for the `else` clause
in a `for else` block
is to handle the case of when the `for` loop has run to completion.

In other words, the implied `if` is **"if a `break` was executed"**.
And of course that only happens when the break condition was found to be true.
So `else` only runs when the break condition was never found to be true:

```python
    for x in my_iterable:
        if the_break_condition(x) is True:
            handle_the_condition_is_true(x)
            break
        handle_the_condition_is_false(x)
    else:
        handle_the_condition_was_never_found_to_be_true()
```

The interpreter knows whether a `break` was executed
and the `for else` block allows the code to know it as well.
Without this construct the code would have to "manually" keep track:

```python
    break_out = False
    for x in my_iterable:
        if the_break_condition(x) is True:
            handle_the_condition_is_true(x)
            break_out = True
            break
        handle_the_condition_is_false(x)
    if break_out:
        pass
    else:
        handle_the_condition_was_never_found_to_be_true()
```

`for else` is ideal for searching:

```python
    for x in my_iterable:
        ... # search for x and break when found
    else:
        handle_not_found()
```
