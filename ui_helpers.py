import pygame
import styles as st

def draw_text(screen, text, x, y, font, color=st.WHITE):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_fitting_text(screen, text, x, y, font, max_width):
 #   original_size = font.get_height()
  #  current_size = original_size

#    while current_size >= 8:
 #       text_width = pygame.font.Font(None, current_size).size(text)[0]
#
 #       if text_width <= max_width-5:
  #          break
   #     current_size -=1

    #fitting_font = pygame.font.Font(None, current_size)
    pass
    #draw_text(screen, text, x, y, fitting_font)
