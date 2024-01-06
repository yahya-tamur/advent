import sys
from common.init_injection import init_injection

# Go to a year folder and run "python ../input.py" to run the
# most recently changed solution on the input from the file named "input"
# in the current directory instead of the usual input.
# Run "python ../input.py print" to see the changed code instead of running.

_, _, code = init_injection(new_input="file='input'")

if 'print' in sys.argv:
    print(code)
else:
    exec(code)
