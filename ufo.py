import pygame
from pygame.sprite import Sprite


class Ufo(Sprite):
    """Klasa do zarządzania ufo"""

    def __init__(self, ai_game):
        """Inicjalizacja UFO i jego położenie początkowe"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Wczytanie obrazu UFO i pobranie jego prostokąta.
        self.image = pygame.image.load('images/ufo1.bmp')

        # Ustawienie rozmiaru obrazu.
        DEFAULT_IMAGE_SIZE = (640/12, 324/12)

        # Skalowanie obrazu do odpowiedniej wielkości
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)

        self.rect = self.image.get_rect()

        # Każde ufo pojawia się z lewej strony na górze ekranu
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Przechowywanie dokładnego poziomu położenia statku
        self.x = float(self.rect.x)
        # Przechowywanie dokładnego pionu położenia statku
        self.y = float(self.rect.y)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Przesunięcie obcych w prawo lub w lewp"""
        self.x += (self.settings.ufo_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Wyświetlanie statku kosmicznego w jego aktualnym położeniu."""
        self.screen.blit(self.image, self.rect)
