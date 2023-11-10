import os

if 'inputs' not in os.listdir():
    os.mkdir('inputs')

with open('session.txt', 'w'):
    pass

print(f'{os.getcwd()}')

with open('.env', 'w') as f:
    f.write(f'P={os.getcwd()}\n')
    f.write('SESSION_FILE=${P}/session.txt\n')
    f.write('INPUT_DIR=${P}/inputs\n')

print('now just install the extension, log in, click the button,')
print('and paste the command you get here.')

