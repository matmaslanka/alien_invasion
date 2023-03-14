import pygame


class Ship:
    """Klasa przeznaczona do zarządzania statkiem kosmicznym."""

    def __init__(self, ai_game):
        """Inicjalizacja statku kosmicznego i jego położenie początkowe"""

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Wczytanie obrazu statku kosmicznego i pobranie jego prostokąta.
        self.image = pygame.image.load('images/rocket1.bmp')

        # Ustawienie rozmiaru dla statku
        DEFAULT_IMAGE_SIZE = (411/12, 720/12)

        # Skalowanie obrazu do odpowiedniej wielkości
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)

        self.rect = self.image.get_rect()

        # Każdy statek pojawia się na dole ekranu
        self.rect.midbottom = self.screen_rect.midbottom

        # Położenie poziome statku jest przechowywane w postaci liczb zmiennoprzecinkowej.
        self.x = float(self.rect.x)

        # Opcja wskazująca na poruszanie się statku
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Uaktualnienie położenia statku na podstawie opcji wskazującej na jego ruch"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.x >= 4:
            self.x -= self.settings.ship_speed

        # Uaktualnienie obiektu rect na podstawie wartości self.x

        self.rect.x = self.x

    def blitme(self):
        """Wyświetlanie statku kosmicznego w jego aktualnym położeniu."""
        self.screen.blit(self.image, self.rect)
