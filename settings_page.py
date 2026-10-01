import pygame
import styles as st
import ui_slider as us
import ui_helpers as uh
import ui_button as ub

class SettingsPage:
    def __init__(self, profile, font, small_font):
        self.profile = profile
        self.font = font
        self.small_font = small_font

        self.volume_slider = us.Slider(
            x = 400, y = 300,
            width = 300,
            min_value= 0, max_value= 100,
            value= 75, step=5
        )
        
        self.ai_turn_speed = us.Slider(
            x=400, y=400,
            width= 300,
            min_value= 10, max_value=1000,
            value=750, step=50 
        )

        self.back_button = ub.Button(
            "Back",
            350, 600, 300, 50,
            st.DARK_BLUE, st.WHITE
        )
        self.ai_difficulty = 2

    def draw(self, screen):
        screen.fill(st.MENU_BACKGROUND)

        uh.draw_text(
            screen, "Settings",
            400, 100,
            self.font, st.WHITE
        )
        uh.draw_text(
            screen, f"{self.volume_slider.value}",
            720, 285,
            self.font, st.WHITE
        )
        
        uh.draw_text(
            screen, f"{self.ai_turn_speed.value} ms",
            720, 385,
            self.small_font, st.WHITE
        )
        
        uh.draw_text(
            screen, "Volume",
            200, 290,
            self.small_font, st.WHITE
        )

        self.volume_slider.draw(screen)

        uh.draw_text(
            screen, "AI Turn Speed",
            200, 390,
            self.small_font, st.WHITE
        )

        self.ai_turn_speed.draw(screen)

        self.back_button.draw(screen, self.small_font)

    def handle_event(self, event):
        self.volume_slider.handle_event(event)
        self.ai_turn_speed.handle_event(event)

        if self.back_button.is_clicked(event):
            return "back"

        return None


