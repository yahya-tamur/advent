Contents, Organization
---------
This repository contains solutions to problems on adventofcode.com.

Right now, it contains all of the solutions for 2016, 2017, 2018, 2019, 2020,
2021, 2022, and 2023.

Each user on the website gets a different input for each problem, and a
'solution' consists of finding an solution for that input and submitting to the
website.

This repository contains some code to help organize the inputs. To set up:

1) Run `python setup-downloads.py` to create a folder that the inputs will get
put into, and a file that will contain the browser session cookie to get the
inputs from the website if they're not downloaded.

2) Download the chrome extension in the `extension` folder, make sure you're
logged in to `adventofcode.com`, and click the button to copy a command to
populate the `session.txt` file. Paste the command in a terminal in this
directory.

3) Try running some of the solutions to make sure they work.

To access the inputs from the code, both `rust` and `python` folders contain
modules with functions called `get-problem` or `get-problem-lines`. This will
try to access the input from the folder, and download it if it's not there.

All the solutions, in both rust and python, should print something like

```
part 1: <solution to part 1>
part 2: <solution to part 2>
```

I did 2022 first, then 2021 and 2023 together, then backwards from 2020. I
switched to python a little bit after I started 2021, though there are a few
problems in rust here and there.

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

Note that in order for symlinks to be correctly set up in Windows, you need to
be in 'developer mode', run some git commands, then clone the repository. I
don't use Windows, but everything else in this repository should work without
problems.

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

In more recent years (in the order I did them, not chronologically), I've
commented '🌟🌟🌟' on solutions I thought were especially interesting. Run
```grep -r '🌟🌟🌟' .``` or equivalent from the python folder to see those
solutions.

