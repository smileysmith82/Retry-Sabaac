class Player:
    def __init__(self, profile, is_ai=False):
        self.profile = profile
        
        self.name = profile.name
        self.credits = profile.credits

        self.is_ai = is_ai
        
        self.hand = []
        self.hand_hidden = False
        self.folded = False

