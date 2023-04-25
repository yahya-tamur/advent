Has all the solutions for 2022.

Some earlier parts don't have a clear answer
for part 1 as well as part 2 -- I might refactor
some of them.

'common' includes a small library for running
dfs-like algorithms in parallel and a function for
fetching the input from a local file, downloading
if the file isn't there.

To use, add to the root directory a 'session.txt' file
containing the browser session token, and a 'inputs' folder,
which the inputs will be downloaded into.

Then, run the solutions from the a2022 directory with
`cargo run -r --bin {problem number}`.
