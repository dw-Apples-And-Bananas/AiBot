import subprocess

cd = "~/"

def exec(command):
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    return str(output)+"\n"+str(err)

async def cmdline(msg, content):
    await msg.reply(exec(content))

async def ls(msg, content):
    await msg.reply(exec(["ls", cd+content]))
