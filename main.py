import asyncio
# from GUI import GUI
import pygame
import pygame_gui
# from screeninfo import get_monitors
from menus import Menus

running = {}
manager = None
window_surface = None
background = None
game = None

def setup():
    global running, manager, window_surface, background, game
    pygame.init()

    gamesize = (1400,900) #implement dropdown resolution
    gamesize = (list(gamesize)[0],list(gamesize)[1]-50) #reduce height
    pygame.display.set_caption('Grungy Kitty Play Center')
    window_surface = pygame.display.set_mode(gamesize)

    background = pygame.Surface(gamesize)
    background.fill(pygame.Color('#000000'))

    manager = pygame_gui.UIManager(gamesize)
    # game = GUI(manager=manager,size=gamesize)
    game = Menus()
    game.setdesktop(manager,gamesize)

async def main():
    setup()
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        events = []
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                events.append('button:' + event.ui_object_id)
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                events.append("dropdown:" + event.text + ":" + event.ui_object_id)
            if event.type == pygame_gui.UI_WINDOW_MOVED_TO_FRONT:
                pass
                # if event.ui_element not in running.keys():
                #     running[event.ui_element] # = 
                
                #create game if it doesn't exist else set run to true
                #create a button that can make the screen continue to run when you log out
                #auto off for games and auto on for regular games
                
            manager.process_events(event)

        # game.update(time_delta,events) # only play games that are

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))

        manager.draw_ui(window_surface)

        pygame.display.update() 
        await asyncio.sleep(0)
    
    return

asyncio.run(main())
