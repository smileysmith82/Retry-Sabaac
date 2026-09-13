import pygame
import os
from game import Game
import styles as st
import ui
import ui_button as ub

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "IMAGES")
def main():
    pygame.init()

    pygame.display.set_caption("Sabaac")
    WIN = pygame.display.set_mode((st.WIDTH,st.HEIGHT))
    font = pygame.font.SysFont(st.FONT_NAME, st.FONT_SMALL)
    
    BG = pygame.transform.scale(pygame.image.load(os.path.join(
                                IMAGE_DIR, "Green_background.jpg")), 
                                (st.WIDTH, st.HEIGHT))

    game = Game()
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        ui.draw_background(WIN, BG)
        ui.draw_game(WIN, game, font)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            ub.handle_button_clicks(event, game)

        game.update()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()