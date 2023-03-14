import sys

import pygame

from settings import Settings
from ship import Ship
from ufo import Ufo


class AlienInvasion:
    """Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry"""

    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobów"""
        pygame.init()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_high))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Inwazja obcych")

        self.ship = Ship(self)
        self.ufo = Ufo(self)

    def run_game(self):
        """Rozpoczęcie pętli głównej gry"""
        while True:
            # Oczekiwanie na naciśnięcie klawisza lub przycisku myszy
            self._check_events()
            self.ship.update()
            self._updete_screen()


    def _check_events(self):
        """Reakcja na zdarzenia generowane przez klawiature i mysz."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_evens(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_evens(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _updete_screen(self):
        """Uaktualnienie obrazów na ekranie i przejście do nowego ekranu"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.ufo.blitme()

        pygame.display.flip()


if __name__ == '__main__':
    # Utworzenie ezamplarza gry i jej uruchomienie.

    ai = AlienInvasion()
    ai.run_game()
