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
  On bad input or network errors,
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
  It will provide a layer of abstaction
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
Decide on what is needed, not on how to do it.
The code that actually does the work will have to be written,
but its ultimate accessibility and utility
depends on how it is wrapped up.
Defer this coding as long as possible.

The decomposition into sub-tasks is aided by the viewpoint
that every piece of code that does something,
is a particular instance of a more general piece of code.
As you proceed away from the root of the tree of tasks
the code becomes more general.
The leaves of this tree will have no knowledge
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