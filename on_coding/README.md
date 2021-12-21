# On Coding Applications in Python

I remember how I used to write programs
and I know how I try to write them now.

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

3. Devise a plan.\
  First make a model.
  Map the user's objects onto programmable objects
  so that the desired outcome can be obtained
  by a series of definite operations on those objects.

4. State the solution.\
  Derive the desired result from operations on the object.

5. Now write the code. \
  Partition the task at hand into independent sub-tasks.
  This is a "breadth-first" recursive technique
  applicable at each stage of the partition.

  For each task there is the code that does the work,
  and there is the code that provides the context for the work to be done.
  Focus on the latter.
  Decide on what is needed, not on how to do it.
  The code that actually does the work will have to be written,
  but its ultimate accessibility and utility
  depends on how it is wrapped up.
  Defer this coding until the end.

  The decomposition into sub-tasks is aided by the viewpoint
  that every piece of code that does something,
  is a particular instance of a more general piece of code.

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
