# Outputs from running main.py

## Description

Command used to run: `python3 main.py`

So basically, I am sorting newtryingToCompute.json, which already has the pre-calculated ratio (coverage/time). This process helps us work more efficiently. By sorting the file, I can organize the data and obtain the output with the smallest coverage value. The smaller the number, the better it is, as it indicates that we achieved more coverage in less time. And, a higher number indicates poorer performance, as it means we covered less in more time.

- The test case `tests/test_checks.py::test_integers` has the highest coverage in less time, indicating it is the most efficient test case in the dataset.

```shell
rosaruiz@Rosas-Laptop Rosa % python3 main.py

🌟 Results 🌟

Sorting by coverage took 0.00039887428283691406 seconds.

🚀 Test Case with Highest Coverage:
Test Name: tests/test_checks.py::test_integers
Coverage: 0.24619199000000663
rosaruiz@Rosas-Laptop Rosa %
```
