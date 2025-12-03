
let message = (message) => {
    document.getElementById("messageBox").innerText = message;
};

document.getElementById("submit").onclick = async () => {
    //Only gets the advent of code ones because of permissions
    const cs = await chrome.cookies.getAll({});
    if (cs.find((c) => c.name == "session") === undefined) {
        message("Cookie not found. Are you logged in on adventofcode.com?")
    } else {
        let session = cs.find((c) => c.name == "session").value;
        let command = `python -c "
import os, sys
for _ in range(10):
    if 'session.txt' in os.listdir():
        open('session.txt', 'w').write('${session}')
        sys.exit()
    os.chdir('..')
print('Couldn\\\'t find a session.txt file. Did you run setup-downloads.py?')
"

`

        await navigator.clipboard
            .writeText(command)
            .then(() => message("copied!"))
            .catch((_e) => message(`There was an error with clipboard, but you can paste this into your session.txt file:\n${session}`));
    }
};

