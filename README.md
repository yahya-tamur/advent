Contents, Organization
---------
This repository contains solutions to problems on adventofcode.com.

Right now, it contains almost all to solutions for 2021, all the solutions for
2022, and solutions for all the released problems for 2023.

Each user on the webiste gets a different input for each problem, and a
'solution' consists of finding an solution for that input and submitting
it to the website.

This repository contains some code to help organize the inputs:

Both python and rust folders contain code for downloading the inputs from the
website to access them locally from the code. You can run `python setup-downloads.py` to
set this up. It will create an 'inputs' folder for the inputs to get downloaded
into and a 'session.txt' file to put the user session cookie from the website into.

The `extension` folder contains an unpacked chrome extension. With this installed,
you can click a button to copy a command that populates the nearest session.txt
file with the session cookie of the website.

You can then go the the python folder and run the `common.py` script to make
sure it works correctly.

The `rust` and `python` folders contain solutions in rust and python respectively.

The `common` module from both folders have a function called `get_problem`. This
will download the input to the problem to `/inputs/a<year>/<day>.txt` if it's not
already there, and return the contents of that file.

All the solutions, in both rust and python, should print something like
```
part 1: <solution to part 1>
part 2: <solution to part 2>
```
when run.

The python folder also contains a `post.py` script which will find the problem
file with the most recent changes, change the code to post the solution to
the latest part to the website instead of just printing it, and run the changed
code.

I did the problems for 2022 and then the start of 2021 in rust, then switched
over to python. There might also be a few more recent solutions in rust if I
thought it was an interesting problem to try to optimize further.

Notes for the rust folder:
-----
This is a workspace, with different crates for each year and a crate
for common functions.

The crates for each year contain binaries named after the day they're for.
To run the solution to day 7 from 2022, cd into the a2022 directory and run

```cargo run -r --bin 07```

In addition to the code for getting the inputs, the 'common' crate includes
a library for running a graph search algorithm in parallel.

-----
Notes for the python folder:
-----
The way I included `common` and `post` in the code is by having symlinks in the folder
for each year.

You can cd into `a<year>` and run
```python <day>.py```
to print the answers to that day from that year.

You can run `python post.py` from a year folder to find the most recently updated day file,
change the code to post the latest part instead of just printing it, and run the changed code.
Run `python post.py print` to print the changed code if you'd like to look at it before running it.

You can run `common.py` standalone to print the input for a given day or post a solution
to a given day and part. Run `python common.py` to see the correct command line inputs.
