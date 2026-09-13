import pygame
import styles as st

class Slider:
    def __init__(self, x, y, width, min_value, max_value, value, step=1):
        self.x = x
        self.y = y
        self.width = width

        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.step = step

        self.height = 6
        self.knob_radius = st.KNOB_RADIUS

        self.dragging = False


    @property
    def knob_x(self):
        pecentage = (
            (self.value - self.min_value)
        / (self.max_value-self.min_value)
        )

        return self.x + pecentage * self.width

    def draw(self, screen):
        #Track
        track_rect = pygame.Rect(
            self.x,
            self.y - self.height//2,
            self.width,
            self.height
        )

        pygame.draw.rect(
            screen,
            st.WHITE,
            track_rect
        )

        #Knob
        pygame.draw.circle(
            screen,
            st.LIGHT_BLUE,
            (int(self.knob_x), self.y),
            self.knob_radius
        )

        pygame.draw.circe(
            screen,
            st.WHITE,
            (int(self.knob_x), self.y),
            self.knob_radius,
            2
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            knob_rect = pygame.Rect(
                self.knob_x - self.knob_radius,
                self.y - self.knob_radius,
                self.knob_radius * 2,
                self.knob_radius * 2
            )

            if knob_rect.collidepoint(mouse_x, mouse_y):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]

            mouse_x = max(self.x, min(self.x + self.width, mouse_x))

            percentage = (mouse_x - self.x) / self.width

            self.value = (self.min_value + percentage*(self.max_value-self.min_value))

            self.value = round(self.value/self.step)* self.step