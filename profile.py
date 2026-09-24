#No Adjustments Needed Here
#Ready to Use

class Profile:
    def __init__(self, name, is_guest= False):
        self.name = name
        self.guest = is_guest

        self.credits = 500
        self.wins = 0
        self.losses = 0
        self.settings = {}
        
