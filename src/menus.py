from pygame_gui.core import ObjectID
import pygame, pygame_gui
from os.path import abspath, isfile
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
        window =  GameWindow(position,manager,relpath)
        return window

    def setdesktop(self,manager,size,applist):
        buttons = []

        if isfile('config.dev'):
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

    def regelm(self, id, function):
        self.register[id] = function

    def getapps(self):
        pass

    def getobvs(self):
        pass

    def getchat(self):
        pass

class GameWindow(pygame_gui.elements.ui_window.UIWindow):
    def __init__(self,position,manager,relpath) -> None:
        # super.__init__(self,rect=pygame.rect((position[0], position[1]), (position[2], position[3])),
            # manager=manager)
        self.setup(manager,position,relpath)

    def on_moved_to_front(self):
        pass
    
    # pulls in the game from the path given in applist.
    # TODO: Load from web addresses
    def setup(self,manager,position,relpath):
        sys.path.insert(0, abspath(relpath))
        from Game import Game
        # 
        self.game = Game(manager,position,sys.path[0])
        self.game.run()
        
    def update(self):
        pass