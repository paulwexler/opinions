# Test Suite

* Run `pylint`.
  ```bash
  $ pylint *.py
  ```
  Ensure the score is 10.00/10
* Run `pytest` using `coverage`.
  ```bash
  $ coverage erase
  $ coverage run --source=. -m pytest -v test
  $ coverage report -m
  ```
  Ensure all tests PASS with 100% coverage (i.e. no missing lines)
