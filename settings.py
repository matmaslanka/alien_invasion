class Settings:
    """Klasa przechowująca wszystkie ustawienia gry."""

    def __init__(self):
        """inicjalizacja ustawień gry"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 50, 0)  # bylo 230, 230, 230
        self.ship_speed = 1.5
        self.ship_limit = 3
        self.bullet_speed = 3  # było 3
        self.bullet_width = 3  # było 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)  # było 60, 60, 60
        self.bullet_allowed = 3
        self.ufo_speed = 2.0  # było 1.0
        self.fleet_drop_speed = 10
        # Wartość fleet_direction wynosząca 1 oznacza w prawo natomiast -1 oznacza lewo
        self.fleet_direction = 1
