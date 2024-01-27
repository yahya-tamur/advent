document.getElementById("submit").onclick = async () => {
    //Only gets the advent of code ones because of permissions
    const cs = await chrome.cookies.getAll({});
    let session = cs.find((c) => c.name == "session").value;
    let command = `python -c "
import os
while 'session.txt' not in os.listdir():
    os.chdir('..')
open('session.txt', 'w').write('#session#')
"

`.replace("#session#", session)
    await navigator.clipboard
        .writeText(command)
        .then(() => alert("copied!"))
        .catch((_e) => alert(command));
};

