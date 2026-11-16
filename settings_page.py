import pygame
import styles as st
import ui_slider as us
import ui_helpers as uh
import ui_button as ub
import settings as stt
import profile_loader as pl

class SettingsPage:
    def __init__(self, profile, font, small_font):
        self.profile = profile
        self.font = font
        self.small_font = small_font

        self.volume_slider = us.Slider(
            400,300, 300,
            min_value= 0, max_value= 100,
            value=profile.settings.get("volume", stt.DEFAULT_VOLUME), step=5
        )
        
        self.ai_turn_speed = us.Slider(
           400,400, 300,
            min_value=10, max_value=1000,
            value=profile.settings.get("ai_turn_speed", stt.DEFAULT_AI_TURN_SPEED), step=50 
        )
        self.ai_difficulty =  profile.settings.get("ai_difficulty", stt.DEFAULT_AI_DIFFICULTY)
        self.use_ai_full_names = profile.settings.get("use_ai_full_names", stt.DEFAULT_USE_AI_FULL_NAMES)

        self.full_name_button = ub.Button(
                "ON" if self.use_ai_full_names else "OFF",
                400, 470, 300, 50,
                st.GREEN if self.use_ai_full_names else st.RED, st.WHITE)        
        self.back_button = ub.Button(
            "Back",
            275, 600, 200, 50,
            st.DARK_BLUE, st.WHITE
        )
        self.save_button = ub.Button(
            "Save",
            525, 600,200,50,
            st.GREEN, st.WHITE
        )
            
        
        
    def draw(self, screen):
        screen.fill(st.MENU_BACKGROUND)

        uh.draw_text(
            screen, "Settings",
            400, 100, self.font, st.WHITE)
        
        uh.draw_text(
            screen, f"{self.volume_slider.value}",
            720, 285, self.font, st.WHITE)
        
        uh.draw_text(
            screen, f"{self.ai_turn_speed.value} ms",
            720, 385,self.small_font, st.WHITE)
        
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

        uh.draw_text(
            screen, "Use AI Full Names",
            200, 490, self.small_font, st.WHITE)
        
        self.ai_turn_speed.draw(screen)
        self.save_button.draw(screen, self.small_font)
        self.back_button.draw(screen, self.small_font)
        self.full_name_button.draw(screen, self.small_font)
        

    def handle_event(self, event):
        self.volume_slider.handle_event(event)
        self.ai_turn_speed.handle_event(event)

        if self.back_button.is_clicked(event):
            return "back"

        if self.save_button.is_clicked(event):
            self.save_settings()
            return "back"

        if self.full_name_button.is_clicked(event):
            self.use_ai_full_names = not self.use_ai_full_names

            if self.use_ai_full_names:
                self.full_name_button.text = "ON"
                self.full_name_button.base_color = st.GREEN
            else:
                self.full_name_button.text = "OFF"
                self.full_name_button.base_color = st.RED

            return None


    def save_settings(self):
        self.profile.settings["volume"] = self.volume_slider.value
        self.profile.settings["ai_turn_speed"] = self.ai_turn_speed.value
        self.profile.settings["ai_difficulty"] = self.ai_difficulty
        self.profile.settings["use_ai_full_names"] = self.use_ai_full_names
        pl.save_profile(self.profile)
