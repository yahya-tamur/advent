document.getElementById("submit").onclick = async () => {
    //Only gets the advent of code ones because of permissions
    const cs = await chrome.cookies.getAll({});
    let session = cs.find((c) => c.name == "session").value;
    let command = await (await fetch("./set-session.py")).text();

    command = 'python -c "' + command.replace("#session#", session) + '\n"\n';
    await navigator.clipboard
        .writeText(command)
        .then(() => alert("copied!"))
        .catch((_e) => alert(command));
};
