import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from ufo import Ufo


class AlienInvasion:
    """Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry"""

    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobów"""
        pygame.init()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Inwazja obcych")

        # Utworzenie egzemplarza przechowującego dane statystyczne dotyczące gry

        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()

        self._create_fleet()

        # Utworzenie przycisku gra
        self.play_button = Button(self, "NEW GAME")

    def run_game(self):
        """Rozpoczęcie pętli głównej gry"""
        while True:
            # Oczekiwanie na naciśnięcie klawisza lub przycisku myszy
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_ufos()

            self._update_screen()

    def _check_events(self):
        """Reakcja na zdarzenia generowane przez klawiature i mysz."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_evens(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Rozpoczęcie nowej gry po kliknięciu przycisku przez użytkownika"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Wyzerowanie ustawień dotyczących gry.
            self.settings.initialize_dynamic_settings()
            # Wyzerowanie danych statystycznych gry.
            self.stats.reset_stats()
            self.stats.game_active = True
            # Ukrycie kursora myszy.
            pygame.mouse.set_visible(False)

            # Usunięcie zawartości list ufos i bullets
            self.ufos.empty()
            self.bullets.empty()

            #Utworzenie nowej floty i wyśrodkowanie statku
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_evens(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Utworzenie nowego pocisku i dodanie go do grupy pocisków"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Uaktualnienie położenia pocisków i usunięcie tych, które są poza ekranem"""
        # Uaktualnienie położenia
        self.bullets.update()

        # Usunięcie pocisków, które znajdują się poza ekranem
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_ufos_collisions()

    def _check_bullet_ufos_collisions(self):
        """Reakcja na kolizję między pociskiem a obcym"""
        # Sprawdzanie czy, którykolwiek pocisk trafił obcego.
        # Jeżeli tak to usuwamy pocisk i obcego
        collision = pygame.sprite.groupcollide(self.bullets, self.ufos, True, True)

        if not self.ufos:
            # pozbycie się istniejących pocisków i utworzenie nowej floty
            self.bullets.empty()
            self._create_fleet()
            # Gra przyspiesz
            self.settings.increase_speed()

    def _update_ufos(self):
        """Sprawdzenia czy flota znajduje się przy krawiędzi a następnie uaktualnienie położenia wszystkich obcych
        we flocie"""
        self._check_fleet_edges()
        self.ufos.update()

        # Wykrywanie kolizji między obcym a statkiem
        if pygame.sprite.spritecollideany(self.ship, self.ufos):
            self._ship_hit()

        # Wyszukanie czy obcy dotarł do dolnej krawędzi ekranu.
        self._check_ufos_bottom()

    def _ship_hit(self):
        """Reakcja na uderzenie obcego w statek"""
        if self.stats.ships_left > 0:
            # Zmniejszenie wartości przechowywanej w ships_left.
            self.stats.ships_left -= 1

            # Usunięcie zawartości listy ufos i byllets.
            self.ufos.empty()
            self.bullets.empty()

            # Utworzenie nowej floty i wypośrodkowanie statku.
            self._create_fleet()
            self.ship.center_ship()

            # Pauza
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_ufos_bottom(self):
        """Sprawdzanie, czy jakikolwiek obcy dotarł do dolnej krawędzi ekranu."""
        screen_rect = self.screen.get_rect()
        for ufo in self.ufos.sprites():
            if ufo.rect.bottom >= screen_rect.bottom:
                # Tak samo jak w przypadku zderzenia statku z obcym
                self._ship_hit()
                break

    def _create_fleet(self):
        """Utworzenie pełnej floty obcych"""
        # Utworzeniae obcego i ustalenie liczby obcych, którzy mieszczą się w rzędzie.
        # Odległość między poszczególnymi obcymi jest równa szerokości obcego.
        ufo = Ufo(self)
        ship = Ship(self)
        ufo_width, ufo_height = ufo.rect.size
        available_space_x = self.settings.screen_width - (2 * ufo_width)
        number_ufos_x = available_space_x // (ufo_width * 2)

        # Ustalenie ilości rzędów na ekranie
        ship_height = ship.rect.height
        available_space_y = self.settings.screen_height - ((20 * ufo_height) - ship_height)
        number_rows = available_space_y // (ufo_height * 2)

        # Utworzenie pełnej floty obcych
        for row_numbers in range(number_rows):
            for ufo_number in range(number_ufos_x):
                self._create_ufo(ufo_number, row_numbers)

    def _create_ufo(self, ufo_number, row_number):
        """Utworzenie obcego, umieszczenie go w rzędzie oraz dodanie kolejnych rzędów"""
        ufo = Ufo(self)
        ufo_width, ufo_height = ufo.rect.size
        ufo.x = ufo_width + 2 * ufo_width * ufo_number
        ufo.rect.x = ufo.x
        ufo.y = ufo.rect.height + 2 * ufo.rect.height * row_number
        ufo.rect.y = ufo.y
        self.ufos.add(ufo)

    def _check_fleet_edges(self):
        """Odpowiednia reakcja, gdy obcy dotrze do krawiędzi ekranu."""
        for ufo in self.ufos.sprites():
            if ufo.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Przesunięcie całej floty w dół i zmiana kierunku, w którym się ona porusza."""
        for ufo in self.ufos.sprites():
            ufo.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Uaktualnienie obrazów na ekranie i przejście do nowego ekranu"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ufos.draw(self.screen)

        #Wyświetlanie przycisku tylko wtedy gdy gra jest nieaktywna
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Utworzenie ezamplarza gry i jej uruchomienie.

    ai = AlienInvasion()
    ai.run_game()
