from typing import Tuple

import pygame

MENU_SCALE_FACTOR = 4


class Character:
    def __select_elemental_portrait(self, element: str):
        if element == "fire":
            self._portrait = pygame.transform.scale2x(
                pygame.image.load(
                    "./images/characters/fire_knight/fire_knight.png"
                )
            )
            self._label = pygame.image.load(
                "./images/characters/fire_knight/fire_label.png"
            )
        elif element == "crystal":
            self._portrait = pygame.transform.scale2x(
                pygame.image.load(
                    "./images/characters/crystal_mauler/crystal_mauler.png"
                )
            )
            self._label = pygame.image.load(
                "./images/characters/crystal_mauler/crystal_label.png"
            )
        elif element == "water":
            self._portrait = pygame.transform.scale2x(
                pygame.image.load(
                    "./images/characters/water_priestess/water_priestess.png"
                )
            )
            self._label = pygame.image.load(
                "./images/characters/water_priestess/water_label.png"
            )
        elif element == "wind":
            self._portrait = pygame.transform.scale2x(
                pygame.image.load(
                    "./images/characters/wind_hashashin/wind_hashashin.png"
                )
            )
            self._label = pygame.image.load(
                "./images/characters/wind_hashashin/wind_label.png"
            )
        else:
            self._portrait = pygame.transform.scale2x(
                pygame.image.load(
                    "./images/characters/leaf_ranger/leaf_ranger.png"
                )
            )
            self._label = pygame.image.load(
                "./images/characters/leaf_ranger/leaf_label.png"
            )

    def __init__(self, position: Tuple[int, int], element: str):
        self.position = position
        self.portrait_position = position[0] + 12, position[1] + 24
        self._label_position = position[0], position[1] + 196
        self._port_holder = pygame.transform.scale_by(
            pygame.image.load("./images/main_menu/introcomp_menu.png"),
            MENU_SCALE_FACTOR,
        )
        self._selected = False
        self.__select_elemental_portrait(element)

    def select(self):
        self._selected = True

    def render(self, display_surface: pygame.Surface):
        if self._selected:
            self._port_holder.set_alpha(128)
            self._portrait.set_alpha(128)
        display_surface.blit(self._port_holder, self.position)
        display_surface.blit(self._portrait, self.portrait_position)
        display_surface.blit(self._label, self._label_position)
