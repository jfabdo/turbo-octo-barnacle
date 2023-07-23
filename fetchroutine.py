from direct.showbase.ShowBase import ShowBase
from browser import Object, fetch

async def fetchroutine(url):
    # optional options object
    options = Object()
    options.method = "GET"

    response = await fetch(url, options)
    if response.ok:
        print(await response.text())
    else:
        print("Error", response.status)

base = ShowBase()
base.taskMgr.add(fetchroutine("./test.txt"))
base.taskMgr.add(fetchroutine("./test2.txt"))
base.run()