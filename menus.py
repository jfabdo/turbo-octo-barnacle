import pygame, pygame_gui

class Menus():
    def __init__(self):
        self.register = {}

    def getbutton(self,manager,position,text,object_id):
        return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((position[0], position[1]), (position[2], position[3])),
                                            text=text,
                                            manager=manager,object_id=object_id)

    def getwindow(self,manager,offset,position):
        return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((position[0], position[1]), (position[2], position[3])),
                                            manager=manager)

    def setdesktop(self,manager,size):
        if open('config.dev') != None:
            object_id = "dev"
            self.getbutton(manager,[5,5,100,20],text=object_id,object_id=object_id)
        object_id = "play"
        button = self.getbutton(manager,[5,35,100,20],text=object_id,object_id=object_id)
        self.regelm(object_id,self.getapps)
        object_id = "obsv"
        button = self.getbutton(manager,[5,65,100,20],text=object_id,object_id=object_id)
        self.regelm(object_id,self.getobvs)
        object_id = "chat"
        button = self.getbutton(manager,[size[0]-105,size[1]-25,100,20],text=object_id,object_id=object_id)
        self.regelm(object_id,self.getchat)

    def regelm(self, id, function):
        self.register[id] = function

    def getapps(self):
        pass

    def getobvs(self):
        pass

    def getchat(self):
        pass