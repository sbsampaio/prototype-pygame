from typing import Tuple

import pygame

MENU_SCALE_FACTOR = 4


class Character:
    max_health: int
    health: int
    attack: int
    defense: int
    speed: int

    def __select_element_attributes(self, element: str):
        if element == "fire":
            self.health = self.max_health = 100
            self.attack = 10
            self.defense = 5
            self.speed = 6
            self.name = "KNIGHT"
        elif element == "crystal":
            self.health = self.max_health = 100
            self.attack = 5
            self.defense = 10
            self.speed = 4
            self.name = "MAULER"
        elif element == "water":
            self.health = self.max_health = 80
            self.attack = 15
            self.defense = 5
            self.speed = 5
            self.name = "MAGE"
        elif element == "wind":
            self.health = self.max_health = 100
            self.attack = 5
            self.defense = 5
            self.speed = 10
            self.name = "ROGUE"
        else:
            self.health = self.max_health = 90
            self.attack = 15
            self.defense = 5
            self.speed = 7
            self.name = "RANGER"

    def __init__(self, position: Tuple[int, int], element: str):
        self.position = position
        self.element = element
        self.portrait_position = position[0] + 12, position[1] + 24
        self._label_position = position[0], position[1] + 196
        self._port_holder = pygame.transform.scale_by(
            pygame.image.load("./images/main_menu/introcomp_menu.png"),
            MENU_SCALE_FACTOR,
        )
        self.selected = False
        self.portrait = pygame.transform.scale2x(
            pygame.image.load(f"./images/characters/{element}/{element}.png")
        )
        self._label = pygame.image.load(
            f"./images/characters/{element}/{element}_label.png"
        )
        self.__select_element_attributes(element)
        self.on_battle = False

    def select(self):
        self.selected = True

    def render(self, display_surface: pygame.Surface):
        if self.selected:
            self._port_holder.set_alpha(128)
            self.portrait.set_alpha(128)

        if not self.on_battle:
            display_surface.blit(self._port_holder, self.position)
            display_surface.blit(self._label, self._label_position)
        else:
            self.portrait.set_alpha(255)

        display_surface.blit(self.portrait, self.portrait_position)
