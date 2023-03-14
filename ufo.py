import pygame


class Ufo:
    """Klasa do zarządzania ufo"""

    def __init__(self, ai_game):
        """Inicjalizacja UFO i jego położenie początkowe"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Wczytanie obrazu UFO i pobranie jego prostokąta.
        self.image = pygame.image.load('images/ufo1.bmp')

        # Ustawienie rozmiaru obrazu.
        DEFAULT_IMAGE_SIZE = (640/12, 324/12)

        # Skalowanie obrazu do odpowiedniej wielkości
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)

        self.rect = self.image.get_rect()

        # Każde ufo pojawia się na środku ekranu
        self.rect.midtop = self.screen_rect.midtop

    def blitme(self):
        """Wyświetlanie statku kosmicznego w jego aktualnym położeniu."""
        self.screen.blit(self.image, self.rect)
