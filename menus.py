from pygame_gui.core import ObjectID
import pygame, pygame_gui
from os.path import abspath
import sys

class Menus():
    def __init__(self):
        self.register = {}

    def getbutton(self,manager,position,text,object_id):
        return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((position[0], position[1]), (position[2], position[3])),
                                            text=text,
                                            manager=manager,
                                            object_id=ObjectID(object_id=object_id,class_id='@friendly_buttons'))

    def getddm(self,manager,position,optionlist,startstr):
        return pygame_gui.elements.UIDropDownMenu(
                                            options_list= [startstr] + list(optionlist.keys()), 
                                            starting_option=startstr,
                                            object_id=startstr,
                                            manager=manager,
                                            relative_rect=pygame.Rect((position[0], position[1]), (position[2], position[3])),
                                            expand_on_option_click=True)

    def openprogram(self,manager,position,relpath):
        window =  pygame_gui.elements.UIButton(relative_rect=pygame.Rect((position[0], position[1]), (position[2], position[3])),
                                            manager=manager)
        
        sys.path.insert(0, abspath(relpath))
        import main
        sys.path.pop(0)

    def setdesktop(self,manager,size,applist):
        buttons = []
        if open('config.dev') != None:
            object_id = "dev"
            self.getddm(manager,[5,5,200,20],applist,object_id)
        object_id = "play"
        buttons += [self.getddm(manager,[5,35,200,20],applist,object_id)]
        self.regelm(object_id,self.getapps)
        object_id = "observe"
        buttons += [self.getddm(manager,[5,65,200,20],applist,object_id)]
        self.regelm(object_id,self.getobvs)
        object_id = "chat"
        buttons += [self.getddm(manager,[size[0]-205,size[1]-25,200,20],applist,object_id)]
        self.regelm(object_id,self.getchat)
        return buttons
    
    def setwindow(self,manager):
        pass

    def regelm(self, id, function):
        self.register[id] = function

    def getapps(self):
        pass

    def getobvs(self):
        pass

    def getchat(self):
        pass