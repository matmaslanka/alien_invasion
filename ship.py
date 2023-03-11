import pygame

class Ship:
    """Klasa przeznaczona do zarządzania statkiem kosmicznym."""

    def __init__(self, ai_game):
        """Inicjalizacja statku kosmicznego i jego położenie początkowe"""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #Wczytanie obrazu statku kosmicznego i pobranie jego prostokąta.
        self.image = pygame.image.load('images/rocket1.bmp')

        #Ustawienie rozmiaru dla statku
        DEFAULT_IMAGE_SIZE = (411/12, 720/12)

        #Skalowanie obrazu do odpowiedniej wielkości
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)

        self.rect = self.image.get_rect()

        #Każdy statek pojawia się na dole ekranu
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Wyświetlanie statku kosmicznego w jego aktualnym położeniu."""
        self.screen.blit(self.image,self.rect)