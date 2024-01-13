Contents, Organization
---------
This repository contains solutions to problems on adventofcode.com.

Right now, it contains all of the solutions for 2019, 2020, 2021, 2022, and 2023.

Each user on the website gets a different input for each problem, and a
'solution' consists of finding an solution for that input and submitting to the
website.

This repository contains some code to help organize the inputs:

Both python and rust folders contain code for downloading the inputs from the
website to access them locally from the code. You can run `python
setup-downloads.py` to set this up. It will create an 'inputs' folder for the
inputs to get downloaded into and a 'session.txt' file to put the user session
cookie from the website into.

The `extension` folder contains an unpacked chrome extension. With this
installed, you can click a button to copy a command that populates the nearest
session.txt file with the session cookie of the website.

You can then go to `python/common` and run the `problem.py` script to make
sure it works correctly.

The `rust` and `python` folders contain solutions in rust and python
respectively.

The `common` module from both folders have a function called `get_problem`.
This will download the input to the problem to `/inputs/a<year>/<day>.txt` if
it's not already there, and return the contents of that file.

All the solutions, in both rust and python, should print something like
```
part 1: <solution to part 1>
part 2: <solution to part 2>
```

The python folder also contains a `post.py` script which will find the problem
file with the most recent changes, change the code to post the solution to the
latest part to the website instead of just printing it, and run the changed
code.

I did 2022 first, then 2021 and 2023 together, then 2020. I switched to python
a little bit after I started 2021, though I did some problems in rust if I
thought they were interesting to try to optimize.

Notes for the rust folder:
-----
This is a workspace, with different crates for each year and a crate for common
functions.

The crates for each year contain binaries named after the day they're for. To
run the solution to day 7 from 2022, cd into the a2022 directory and run

```cargo run -r --bin 07```

In addition to the code for getting the inputs, the 'common' crate includes a
library for running a graph search algorithm in parallel. See days 16 and 19
from 2022 for examples of how it's used.

Notes for the python folder:
-----
The way I included `problem` in the code is by having symlinks in the folder for
each year.

You can cd into `a<year>` and run ```python <day>.py``` to print the answers to
that day from that year.

You can run `python ../post.py` from a year folder to find the most recently
updated day file, inject some code to post the answer instead of just printing
it, and run the injected code. Run `python post.py print` to print the injected
code instead of running it.

To run the code on a test input rather than the real input, you can run `python
../input.py` from a year folder. This will run the code with the input from the
file named `input` in the current directory. This modifies the code, similar to
post.py. Run `python ../input.py print` to take a look at the modified code.

You can run `common/problem.py` standalone to print the input for a given day
or post a solution to a given day and part. Run `python problem.py` to see the
correct command line inputs.

You can run the `make_year.py` script to set up a folder for a new year.
Currently, this just makes the folder and creates the problem.py symlink.
