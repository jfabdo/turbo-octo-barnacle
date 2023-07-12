from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from screeninfo import get_monitors

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        for m in get_monitors():
            if m.is_primary:
                primarymonitor = m

        properties = WindowProperties()
        properties.setSize(primarymonitor.width, primarymonitor.height)
        self.win.requestProperties(properties)