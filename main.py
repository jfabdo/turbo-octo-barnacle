from GUI import GUI
import pygame
import pygame_gui
# from screeninfo import get_monitors


pygame.init()

gamesize = pygame.display.get_desktop_sizes()[0]
gamesize = (list(gamesize)[0],list(gamesize)[1]-50) #reduce height
pygame.display.set_caption('Grungy Kitty')
window_surface = pygame.display.set_mode(gamesize)

background = pygame.Surface(gamesize)
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager(gamesize)
game = GUI(manager=manager,size=gamesize)

clock = pygame.time.Clock()
is_running = True

while is_running:

    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            pass
        manager.process_events(event)

    game.update(time_delta)

    manager.update(time_delta)
    window_surface.blit(background, (0, 0))

    manager.draw_ui(window_surface)

    pygame.display.update() 