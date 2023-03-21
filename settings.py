class Settings:
    """Klasa przechowująca wszystkie ustawienia gry."""

    def __init__(self):
        """inicjalizacja ustawień gry"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 50, 0)  # bylo 230, 230, 230

        self.ship_limit = 3

        self.bullet_width = 3 # było 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)  # było 60, 60, 60
        self.bullet_allowed = 3

        self.fleet_drop_speed = 10

        self.fleet_direction = 1

        # Łatwa zmiana szybkości gry
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inizcjalizacja ustawień, które ulegają zmianie w trakcie gry."""
        self.ship_speed = 1.3
        self.bullet_speed = 3  # było 3
        self.ufo_speed = 1.5  # było 1.0
        # Wartość fleet_direction wynosząca 1 oznacza w prawo natomiast -1 oznacza lewo
        self.fleet_direction = 1

    def increase_speed(self):
        """Zmiana ustawień dotyczących szybkości"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.ufo_speed *= self.speedup_scale

