Has all the solutions for 2022, some for 2021.

Some earlier days don't have a clear answer
for part 1 as well as part 2 -- I might refactor
some of them.

'common' includes a small library for running
a graph search algorithm in parallel and a function for
fetching the input from a local file, downloading
it from the website if the file isn't there.

To use, make a file containing the browser session*, and
a folder to download the inputs into. Add a .env
file in the root directory containing the paths to these,
under the environment variables `INPUT_DIR`, `SESSION_FILE`.

The .env file is read at compile time, and I think it's
preferable to put absolute paths there.

For example, to run the solution to day 7 from 2022,
cd into the a2022 directory and run

```cargo run -r --bin 07```

Which should print out the answer for both parts.

I feel like I spent a bit too much time thinking about the project
structure and came up with something worse than anything I could have
come up with in the beginning. It's awkward to have binaries with the
same names. You can't build everything from the root directory (without
warnings) and since the executables are in the root target directory,
it's hard to tell what 'target/release/01' actually is.

However, I
like that when I'm working on a solution in an a20xx directory, I don't
have to rewrite the year when running the binary or starting a new solution.
It's also nice to start a completely new project every 25 problems, while
being able to share some code if I need to. I'm really happy with how all the
inputs from all the years are in a single folder that's automatically
managed.

* I also made a chrome extension for getting this. Add the extension in the
'extension' folder, click the icon on the chrome top bar, and click 'copy
command'. Paste the command to replace the closest file named 'session.txt' in
the ancestors of the current directory.
