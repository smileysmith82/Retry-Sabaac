import pygame
import styles as st
import ui_helpers as uh
import ui_button as ub
from profile import Profile
import profile_loader as pl
MAX_PROFILE_NAME_LENGTH = 15

class ProfileScreen:
    def __init__(self, font, small_font):
        self.profiles = pl.get_profiles()
        self.profile_buttons = []
        self.profile_data = []

        self.font = font
        self.small_font = small_font

        self.scroll_offset = 0
        self.scroll_speed = 40
        
        self.load_profiles()
        self.create_buttons()

        self.guest_button = ub.Button(
            "Guest",
            270, 650, 140, 50,
            st.GRAY, st.WHITE
        )
        self.new_profile_button = ub.Button(
            "New Profile",
            430, 650, 140, 50,
            st.DARK_BLUE, st.WHITE
        )
        self.delete_profile_button = ub.Button(
            "Delete Profile",
            590, 650, 140, 50,
            st.RED, st.WHITE
        )
        
        self.confirm_delete_button = ub.Button(
            "Delete",
            350, 450, 140, 50,
            st.RED, st.WHITE
        )
        self.cancel_delete_button = ub.Button(
            "Cancel",
            510, 450, 140, 50,
            st.GRAY, st.WHITE
        )
        
        self.selected_profile = None
        self.creating_profile = False
        self.profile_name = ""
        self.profile_message = ""
        self.deleting_profile = False
        self.confirming_delete = False

        self.confirm_profile_button = ub.Button(
            "Confirm",
            350, 450, 140, 50,
            st.GREEN, st.WHITE
        )
        self.cancel_profile_button = ub.Button(
            "Cancel",
            510, 450, 140, 50,
            st.GRAY, st.WHITE
        )
        
    def load_profiles(self):
        for name in self.profiles:
            profile = pl.load_profile(name)

            if profile is not None:
                self.profile_data.append(profile)    

    def refresh_profiles(self):
        self.profiles = pl.get_profiles()
        self.profile_data = []
        self.load_profiles()
        self.create_buttons()
    def reset(self):
        self.selected_profile = None
        self.deleting_profile = False
        self.confirming_delete = False
        self.creating_profile = False
        self.profile_name = ""
        self.profile_message = ""
        self.scroll_offset = 0

    def finish_profile_creation(self):
        name = self.profile_name.strip().title()

        if name == "":
            self.profile_message = "Please enter a profile name."
            return None

        if len(name) > MAX_PROFILE_NAME_LENGTH:
            self.profile_message = "Profile name is too long"
            return None

        if name.lower() in [profile_name.lower() for profile_name in self.profiles]:
            self.profile_message = "That profile name already exists."
            return None

        profile = pl.create_profile(name)
        self.refresh_profiles()
        self.cancel_profile_creation()
        self.profile_message = ""
        self.selected_profile = profile

        return profile

    def cancel_profile_creation(self):
        self.creating_profile = False
        self.profile_name = ""

    def create_buttons(self):
        self.profile_buttons = []
        profiles_per_row = 3
        button_width = 280
        button_height = 120

        spacing_x = 20
        spacing_y = 20

        total_width = (profiles_per_row * button_width 
                       + (profiles_per_row - 1) * spacing_x)

        start_x = (st.WIDTH - total_width) // 2
        start_y = 200        

        for i, profile in enumerate(self.profile_data):
            row = i//profiles_per_row
            column = i % profiles_per_row
            x = start_x + column * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)

            button = ub.Button(
                "",
                x, y,
                button_width, button_height,
                st.LIGHT_BLUE, st.BLACK
            )
            self.profile_buttons.append(button)

    def get_max_scroll(self):
        profiles_per_row = 3
        button_height = 120

        spacing_y = 20

        start_y = 200

        rows = (len(self.profile_data)
                + profiles_per_row -1
                ) // profiles_per_row

        if rows == 0:
            return 0

        content_height = (
            rows * button_height
            + (rows -1) * spacing_y
        )

        visible_height = 400

        max_scroll = max(0, content_height - visible_height)

        return max_scroll

    def delete_selected_profile(self):
        pl.delete_profile(self.selected_profile.name)

        self.refresh_profiles()

        self.selected_profile = None
        self.deleting_profile = False
        self.confirming_delete = False
        self.profile_message = ""
        self.scroll_offset = 0

    def handle_event(self, event):

        if self.confirming_delete:            
            if self.confirm_delete_button.is_clicked(event):
                self.delete_selected_profile()
                return None

            if self.cancel_delete_button.is_clicked(event):
                self.deleting_profile = False
                self.confirming_delete = False
                self.selected_profile = None
                self.profile_message = ""
                return None

            return None
        if self.new_profile_button.is_clicked(event):
            self.deleting_profile = False
            self.profile_message = ""
            self.selected_profile = None
            
            self.creating_profile = True
            self.profile_name = ""
            return None

        if self.delete_profile_button.is_clicked(event):
            self.creating_profile = False
            self.profile_name = ""
                
            if self.deleting_profile:
                self.deleting_profile = False
                self.profile_message = ""
                self.selected_profile = None
                return None

            if self.selected_profile is None:
                self.profile_message = "Please select a profile to delete"
            else:
                self.profile_message = ""

            self.deleting_profile = True
            return None
        
        if self.creating_profile:
            if self.confirm_profile_button.is_clicked(event):
                if self.profile_name.strip() != "":
                    return self.finish_profile_creation()

            if self.cancel_profile_button.is_clicked(event):
                self.cancel_profile_creation()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.profile_name = self.profile_name[:-1]
                    self.profile_message = ""

                elif event.key == pygame.K_RETURN:
                    return self.finish_profile_creation()

                elif event.unicode.isprintable():
                    if len(self.profile_name) < MAX_PROFILE_NAME_LENGTH:
                        self.profile_name += event.unicode
                        self.profile_message = ""

                    else:
                        self.profile_message = "Profile name is too long"

                    
            return None
   
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= (
                event.y * self.scroll_speed
            )

            self.scroll_offset = max(0, min(self.scroll_offset, self.get_max_scroll()))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_offset -= self.scroll_speed

            elif event.key == pygame.K_DOWN:
                self.scroll_offset += self.scroll_speed

            self.scroll_offset = max(
                0, min(self.scroll_offset, self.get_max_scroll())
            )           
        
        if self.guest_button.is_clicked(event):
            self.selected_profile = Profile(
                "Guest",
                is_guest = True
            )
            return self.selected_profile

        if event.type == pygame.MOUSEBUTTONUP:
            profile_area = pygame.Rect(0, 180, st.WIDTH, 430)
            if profile_area.collidepoint(event.pos):
                for i, button in enumerate(self.profile_buttons):           
                    if button.is_clicked(event):
                        self.selected_profile = self.profile_data[i]
                        
                        if self.deleting_profile:
                            self.confirming_delete = True
                            return None
                        return self.selected_profile
            
    def draw(self, screen):
        screen.fill(st.MENU_BACKGROUND)

        #Title
        uh.draw_text(
            screen,
            "Select Profile",
            (st.WIDTH//2) -50, 100,
            self.font, st.WHITE
        )
        profile_area = pygame.Rect(
            0, 180, st.WIDTH, 430
        )
        screen.set_clip(profile_area)
        profiles_per_row = 3
        button_height = 120
        spacing_y = 20
        start_y = 200

        for i,button in enumerate(self.profile_buttons):
            profile = self.profile_data[i]

            row = i // profiles_per_row
            normal_y = (start_y + row * (button_height + spacing_y))

            button.rect.y = (normal_y - self.scroll_offset)    

            button.draw(screen, self.font)
            #Profile Name
            name_surface = self.font.render(
                profile.name, True, st.WHITE)
            name_rect = name_surface.get_rect(
                center = (button.rect.centerx, button.rect.y + 25)
            )
            screen.blit(name_surface, name_rect)
            
            #Wins
            wins_surface = self.small_font.render(f"Wins: {profile.wins}",
            True,
            st.WHITE)
            wins_rect = wins_surface.get_rect(
                center=(button.rect.centerx - 70, button.rect.y + 65)
            )
            screen.blit(wins_surface, wins_rect)

            # Losses
            losses_surface = self.small_font.render(
                f"Losses: {profile.losses}",
                True,
                st.WHITE
            )
            losses_rect = losses_surface.get_rect(
                center=(button.rect.centerx + 70, button.rect.y + 65)
            )
            screen.blit(losses_surface, losses_rect)

            # Credits
            credits_surface = self.small_font.render(
                f"Credits: {profile.credits}",
                True,
                st.LIGHT_YELLOW)
            credits_rect = credits_surface.get_rect(
                center=(button.rect.centerx, button.rect.y + 100)
            )
            screen.blit(credits_surface, credits_rect)
        screen.set_clip(None)

        self.guest_button.draw(screen, self.small_font)
        self.new_profile_button.draw(screen, self.small_font)
        self.delete_profile_button.draw(screen, self.small_font)

        if self.profile_message:
            uh.draw_text(screen,
                self.profile_message, 
                400, 620,
                self.small_font, st.RED)
            
        if self.creating_profile:
            panel = pygame.Rect(
                250, 150, 500, 450
            )

            pygame.draw.rect(
                screen, st.GRAY, panel
            )
            
            pygame.draw.rect(
                screen,
                st.WHITE, panel, 2
            )

            uh.draw_text(
                screen,
                "Create Profile",
                350, 190,
                self.font, st.WHITE
            )

            uh.draw_text(
                screen,
                "Enter your name:",
                350, 250,
                self.small_font, st.WHITE
            )

            uh.draw_text(
                screen,
                self.profile_name,
                350, 300,
                self.font, st.WHITE
            )
            
            if self.profile_message != "":
                uh.draw_text(
                    screen, self.profile_message,
                    350,350, self.small_font, st.RED
                )

            self.confirm_profile_button.draw(
                screen,
                self.small_font
            )

            self.cancel_profile_button.draw(
                screen,
                self.small_font
            )

            return

        if self.confirming_delete:
            panel = pygame.Rect(
                            250, 150, 500, 450
                        )
            pygame.draw.rect(
                screen, st.GRAY, panel
            )
            pygame.draw.rect(
                screen, st.WHITE, panel, 2
            )

            uh.draw_text( screen,
                f"Delete {self.selected_profile.name}'s Profile?",
                350, 190, self.font, st.WHITE                
            )
            uh.draw_text(screen,
            "WARNING: This cannot be undone.",
            350, 300, self.small_font, st.RED
            )
            self.confirm_delete_button.draw(
                screen,self.small_font
            )
            self.cancel_delete_button.draw(
                screen,self.small_font
            )
            return

        