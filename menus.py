import pygame, pygame_gui

class Menus():

    def getbutton(self,manager,position,text):
        return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((position[0], position[1]), (position[2], position[3])),
                                            text=text,
                                            manager=manager)

    def getwindow(self,manager,offset,position):
        return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((position[0], position[1]), (position[2], position[3])),
                                            manager=manager)

    def setdesktop(self,manager,size):
        if open('config.dev') != None:
            self.getbutton(manager,[5,5,100,20],"dev")
        self.getbutton(manager,[5,35,100,20],"play")
        self.getbutton(manager,[5,65,100,20],"obsv")
        self.getbutton(manager,[size[0]-105,size[1]-25,100,20],"chat")
