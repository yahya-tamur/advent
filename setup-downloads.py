import os

print()
print("Both python and rust projects have modules called 'problem'")
print('that get the problem inputs.')
print()
print('They try to get the it from a local file, and download')
print("it from the website if that doesn't exist.")
print()
print("This script makes the 'session' file and the 'inputs' directory,")
print("then sets up the environment variables in a .env file.")
print()

if os.getcwd().split("/")[-1] != "advent":
    print("This should be run from the root project folder.")
    print("Are you sure you're there?")
    print("Press Ctrl-C to quit, Enter to proceed.")
    input()

if '_inputs' not in os.listdir():
    os.mkdir('_inputs')

with open('session.txt', 'w'):
    pass

with open('.env', 'w') as f:
    f.write(f'P={os.getcwd()}\n')
    f.write('SESSION_FILE=${P}/session.txt\n')
    f.write('INPUT_DIR=${P}/_inputs\n')

print('Setup complete.')
print()
print('To populate the session file, install the extension,')
print("make sure you're logged in to adventofcode, click the button")
print('in the extension popup, and paste the command you get here.')
print()
print('After that, to test, you can run python/common/problem.py:')
print()
print('python python/common/problem.py get 2021 11')
print()
print("It should be slower in the first run.")
print()

