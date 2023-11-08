import os
while 'session.txt' not in os.listdir():
    os.chdir('..')
os.system(r'''echo '#session#' > session.txt''');
