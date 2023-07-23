from random import choice
import direct.fsm.FSM as FSM
from GUI import GUI
from GameObject import Actor
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
        GameObject.__init__(self,
                            Vec3(0, 0, 0),
                            "dot",
                              {
                                  "stand" : "dot",
                                  "walk" : "dot",
                                  'jump' : "dot"
                              },
                            5,
                            10,
                            "player")
        
        self.actor.getChild(0).setH(180)

        mask = BitMask32()
        mask.setBit(1)

        self.collider.node().setIntoCollideMask(mask)

        mask = BitMask32()
        mask.setBit(1)

        self.collider.node().setFromCollideMask(mask)

        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.lastMousePos = Vec2(0, 0)

        self.magicstate = MagicFSM(self)
        self.weaponstate = WeaponFSM(self)
    
    def enterStanding(self):
        standControl = self.actor.getAnimControl("stand")
        if not standControl.isPlaying():
            self.actor.stop("walk")
            self.actor.loop("stand")

    def enterWalking(self):
        standControl = self.actor.getAnimControl("stand")
        if standControl.isPlaying():
                standControl.stop()

        walkControl = self.actor.getAnimControl("walk")
        if not walkControl.isPlaying():
            self.actor.loop("walk")

    def enterJump(self):
        self.request("Jump")

    def enterWeapon(self): #be sure to allow for both hand fighting
        self.weaponstate.request("Strike")
    
    def enterMagic(self):
        self.magicstate.request("Charging")

    def enterHit(self):
        pass

    def enterDead(self):
        pass

    def enterExit(self):
        Actor.cleanup()

class WeaponFSM(FSM):
    def __init__(self):
        FSM.__init__(self, 'WeaponState')
        self.defaultTransitions = {
                'Draw' : [ 'Idle' ],
                'Idle' : [ 'Strike', 'Block', 'Away' ],
                'Strike' : [ 'Idle'],
                'Block' : [ 'Idle', 'Strike' ],
                'Away' : [ '' ]
        }

        self.beamModel = loader.loadModel("dot")
        self.beamModel.reparentTo(self.actor)
        self.beamModel.setZ(1.5)
        self.beamModel.setLightOff()
        self.beamModel.hide()

        self.beamHitModel = loader.loadModel("dot")
        self.beamHitModel.reparentTo(render)
        self.beamHitModel.setZ(1.5)
        self.beamHitModel.setLightOff()
        self.beamHitModel.hide()
        self.beamHitPulseRate = 0.15
        self.beamHitTimer = 0

        self.damagePerSecond = -5.0
    
    def enterIdle(self):
        if render.hasLight(self.beamHitLightNodePath):
            render.clearLight(self.beamHitLightNodePath)

        self.beamModel.hide()
        self.beamHitModel.hide()

        if self.laserSoundNoHit.status() == AudioSound.PLAYING:
            self.laserSoundNoHit.stop()
        if self.laserSoundHit.status() == AudioSound.PLAYING:
            self.laserSoundHit.stop()

    def enterStrike(self):
        scoredHit = False

        self.rayQueue.sortEntries()
        rayHit = self.rayQueue.getEntry(0)
        hitPos = rayHit.getSurfacePoint(render)

        hitNodePath = rayHit.getIntoNodePath()
        if hitNodePath.hasPythonTag("owner"):
            hitObject = hitNodePath.getPythonTag("owner")
            if not isinstance(hitObject, TrapEnemy):
                hitObject.alterHealth(self.damagePerSecond*dt)
                scoredHit = True


        beamLength = (hitPos - self.actor.getPos()).length()
        self.beamModel.setSy(beamLength)

        self.beamModel.show()
        
        if scoredHit:
            if self.laserSoundNoHit.status() == AudioSound.PLAYING:
                self.laserSoundNoHit.stop()
            if self.laserSoundHit.status() != AudioSound.PLAYING:
                self.laserSoundHit.play()

            self.beamHitModel.show()

            self.beamHitModel.setPos(hitPos)
            self.beamHitLightNodePath.setPos(hitPos + Vec3(0, 0, 0.5))

            if not render.hasLight(self.beamHitLightNodePath):
                render.setLight(self.beamHitLightNodePath)
        else:
            if self.laserSoundHit.status() == AudioSound.PLAYING:
                self.laserSoundHit.stop()
            if self.laserSoundNoHit.status() != AudioSound.PLAYING:
                self.laserSoundNoHit.play()

            if render.hasLight(self.beamHitLightNodePath):
                render.clearLight(self.beamHitLightNodePath)

            self.beamHitModel.hide()
        
        self.request('Idle')
    
    def exitStrike(self):
        pass

    def enterBlock(self):
        pass

    def enterAway(self):
        self.gameobject.cleanup()

class MagicFSM(FSM):
    def __init__(self):
        FSM.__init__(self, 'MagicState')
        self.defaultTransitions = {
                'Idle' : [ 'Charging', 'Away' ],
                'Charging' : [ 'Firing' ],
                'Firing' : [ 'Hit' ],
                'Hit' : [ 'Idle' ],
                'Away' : [ '' ]
        }

    def enterIdle(self):
        pass

    def enterCharging(self):
        #hold off until the button is released
        self.game
        self.request("Firing")

    def enterFiring(self):
        self.request("Hit")

    def enterHit(self):
        self.request('Idle')

    def enterAway(self):
        pass #destroy object