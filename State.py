from random import choice
import direct.fsm.FSM as FSM
from GUI import GUI
from direct.gui.DirectGui import taskMgr

welcomescreen = [
    "Welcome, fool",
    "Welcome to the dungeons"
]

class MenuFSM(FSM):
    def __init__(self):
        FSM.__init__(self, 'MenuState')
        self.defaultTransitions = {
            'Intro' : [ 'Exited', 'Playing' ],
            'Playing' : [ 'Escaped', 'Paused' ],
            'Escaped' : [ 'Exited', 'Intro', 'Playing' ],
            'Paused' : [ 'Escaped', 'Playing' ],
            'Exited' : [ ],
        }
        self.GUI = GUI(self)
        self.GUI.run()

    def enterIntro(self):
        self.GUI.introscreen.show()

    def exitIntro(self):
        self.GUI.introscreen.hide()

    def enterPlaying(self):
        self.GUI.updateTask = taskMgr.add(self.update, "update")

class ActorFSM(FSM):
    def __init__(self):
        FSM.__init__(self, 'ActorState')
        # self.defaultTransitions = {
        #     'Standing' :
        # }
    
    def enterStanding(self):
        pass

    def enterWalking(self):
        pass

    def enterWeapon(self): #be sure to allow for both hand fighting
        pass
    
    def enterMagic(self):
        pass

    def enterHit(self):
        pass

    def enterDead(self):
        pass

class WeaponFSM(FSM):
    def __init__(self):
        FSM.__init__(self, 'WeaponState')
        self.defaultTransitions = {
                'Draw' : [ 'Idle' ],
                'Idle' : [ 'Strike', 'Block', 'Away' ],
                'Strike' : [ 'Idle', ],
                'Block' : [ 'Idle', 'Strike' ],
                'Away' : [ '' ]
        }
    
    def enterIdle(self):
        pass

    def enterStrike(self):
        self.request('Idle')

    def enterBlock(self):
        pass

class MagicFSM(FSM):
    def __init__(self):
        FSM.__init__(self, 'MagicState')
        self.defaultTransitions = {
                'Idle' : [ 'Charging', 'Exit' ],
                'Charging' : [ 'Firing' ],
                'Firing' : [ 'Hit' ],
                'Hit' : [ 'Idle' ],
                'Exit' : [ '' ]
        }

    def enterIdle(self):
        pass

    def enterCharging(self):
        #hold off until 
        self.request('Firing')

    def enterFiring(self):
        self.request('Hit')

    def enterHit(self):
        self.request('Idle')

    def enterExit(self):
        pass #destroy object