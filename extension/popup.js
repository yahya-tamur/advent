document.getElementById("submit").onclick = async () => {
    //Only gets the advent of code ones because of permissions
    const cs = await chrome.cookies.getAll({});
    let session = cs.find((c) => c.name == "session").value;
    let command = `python -c "
import os, sys
for _ in range(10):
    if 'session.txt' in os.listdir():
        open('session.txt', 'w').write('#session#')
        sys.exit()
    os.chdir('..')
print('Couldn\\\'t find a session.txt file. Did you run setup-downloads.py?')
"

`.replace("#session#", session)
    await navigator.clipboard
        .writeText(command)
        .then(() => alert("copied!"))
        .catch((_e) => alert(command));
};

