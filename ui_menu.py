import styles as st
import ui_helpers as uh
import ui_button as ub


class MainMenu:
    def __init__(self, profile, font, small_font):
        self.profile = profile

        self.font = font
        self.small_font = small_font

        self.play_button = ub.Button(
            "Play",
            325, 300, 300, 50,
            st.DARK_BLUE, st.WHITE
        )

        self.settings_button = ub.Button(
            "Settings",
            325, 380, 300, 50,
            st.DARK_BLUE, st.WHITE
        )

        self.change_profile_button = ub.Button(
            "Change Profile",
            325, 460, 300, 50,
            st.GRAY, st.WHITE
        )

        self.quit_button = ub.Button(
            "Quit",
            325, 540, 300, 50,
            st.RED, st.WHITE
        )

    def handle_event(self, event):
        if self.play_button.is_clicked(event):
            return "play"

        if self.settings_button.is_clicked(event):
            return "settings"

        if self.change_profile_button.is_clicked(event):
            return "profile"

        if self.quit_button.is_clicked(event):
            return "quit"

        return None

    def draw(self, screen):
        screen.fill(st.MENU_BACKGROUND)

        uh.draw_text(screen,
                "SABACC",
                400, 100,
                self.font, st.WHITE)

        uh.draw_text(screen,
                     f"Welcome, {self.profile.name}",
                     400, 180,
                     self.small_font, st.WHITE
        )
        uh.draw_text(
            screen,
            f"Credits: {self.profile.credits}",
            400, 215,
            self.small_font,
            st.LIGHT_YELLOW
        )

        uh.draw_text(
            screen,
            f"Wins: {self.profile.wins}",
            350, 250,
            self.small_font,
            st.WHITE
        )
        uh.draw_text(
            screen,
            f"Losses: {self.profile.losses}",
            450, 250,
            self.small_font,
            st.WHITE
        )

        self.play_button.draw(screen, self.small_font)
        self.settings_button.draw(screen, self.small_font)
        self.change_profile_button.draw(screen, self.small_font)
        self.quit_button.draw(screen, self.small_font)