import subprocess

cd = "~/"

def exec(command):
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    return output

async def ls(msg, content):
    await msg.reply(exec(["ls", cd+content]))
