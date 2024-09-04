import sys
from typing import Tuple
from time import sleep

import pygame

from arrow import Arrow
from character import Character
from enemy import Enemy

NUM_CHARACTERS = 5
MENU_SCALE_FACTOR = 4


def drop_shadow_text(
    screen: pygame.Surface,
    text: str,
    size: int,
    position: Tuple[int, int],
):
    dropshadow_offset = 1 + (size // 15)
    text_font = pygame.font.Font("./fonts/ARCADE_N.TTF", size)

    text_bitmap = text_font.render(text, True, (0, 0, 0))
    screen.blit(
        text_bitmap,
        (position[0] + dropshadow_offset, position[1] + dropshadow_offset),
    )

    text_bitmap = text_font.render(text, True, (255, 255, 255))
    screen.blit(text_bitmap, position)


class Game:
    background = pygame.transform.scale_by(
        pygame.image.load("./images/main_menu/background.png"),
        MENU_SCALE_FACTOR,
    )
    characters = [
        Character((142, 230), "crystal"),
        Character((436, 230), "wind"),
        Character((730, 230), "fire"),
        Character((289, 510), "water"),
        Character((583, 510), "leaf"),
    ]
    selected_characters = []
    battle_array: list
    title = pygame.image.load("./images/main_menu/introbattle_title.png")
    turn: str

    def __init__(self, width: int, height: int) -> None:
        self._running = True
        self._display_surf: pygame.Surface
        self.window_size = self.width, self.height = width, height
        self._selection_arrow = Arrow()
        self._idx = 0
        self._selected_chars = 0
        self._actual_turn = 0

    def on_init(self) -> None:
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.window_size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._running = True

    def event_handler(self, event):
        pressed_keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            self._running = False
        if pressed_keys[pygame.K_ESCAPE]:
            self._running = False
        if pressed_keys[pygame.K_RIGHT]:
            self._selection_arrow.move_right()
            if self._selection_arrow.stage == 1:
                if self._idx >= 3:
                    self._idx = -1
            else:
                if self._idx >= 4:
                    self._idx = -1
            self._idx += 1
        if pressed_keys[pygame.K_LEFT]:
            self._selection_arrow.move_left()
            if self._selection_arrow.stage == 1:
                if self._idx <= 0:
                    self._idx = 4
            else:
                if self._idx <= 0:
                    self._idx = 5
            self._idx -= 1
        if pressed_keys[pygame.K_z]:
            if not self.characters[self._idx].selected:
                self._selected_chars += 1
                self.selected_characters.append(self.characters[self._idx])
            self.characters[self._idx].select()
            if self._selection_arrow.stage == 1:
                self.on_turn(self._actions[self._idx])

    def cleanup(self):
        pygame.quit()
        sys.exit()

    def on_main_menu(self):
        self._display_surf.blit(self.title, (218, 71))

        for i in range(NUM_CHARACTERS):
            self.characters[i].render(self._display_surf)

        self._selection_arrow.render(self._display_surf)

    def on_battle(self):
        if self._selection_arrow.stage == 0:
            self._idx = 0
            self._actions = ["ATTACK", "DEFENSE", "INSIGHT", "SKILL"]
            self._selection_arrow.on_battle()
            for i in range(3):
                self.selected_characters[i].on_battle = True
                self.selected_characters[i].portrait = (
                    pygame.transform.scale_by(  # noqa: E501
                        pygame.image.load(
                            f"./images/characters/{self.selected_characters[i].element}/{self.selected_characters[i].element}_idle.png"  # noqa: E501
                        ),
                        3,
                    )
                )
                self.selected_characters[i].position = (
                    20 + i * 321,
                    602,
                )

            self.selected_characters[0].portrait_position = (-197, -109)
            self.selected_characters[1].portrait_position = (-326, 0)
            self.selected_characters[2].portrait_position = (-197, 91)
            self.enemies = [
                Enemy(1, (889, 179), "SKELETON"),
                Enemy(2, (889, 342), "VEIGAR"),
            ]  # noqa: E501
            self.battle_array = self.selected_characters + self.enemies
            self.battle_array.sort(key=lambda x: x.speed, reverse=True)
            self.turn = self.battle_array[self._actual_turn].name
            self._selection_arrow.stage = 1

        pygame.draw.rect(
            self._display_surf, (180, 180, 180), (20, 504, 678, 245)
        )  # noqa: E501
        pygame.draw.rect(
            self._display_surf, (180, 180, 180), (721, 504, 278, 245)
        )  # noqa: E501
        drop_shadow_text(
            self._display_surf, f"{self.turn.upper()}'S TURN", 34, (71, 529)
        )
        drop_shadow_text(self._display_surf, "ATTACK", 32, (71, 602))
        drop_shadow_text(self._display_surf, "DEFENSE", 32, (392, 602))
        # drop_shadow_text(self._display_surf, "INSIGHT", 32, (71, 675))
        # drop_shadow_text(self._display_surf, "SKILL", 32, (392, 675))
        for i in range(3):
            self.selected_characters[i].render(self._display_surf)
            drop_shadow_text(
                self._display_surf,
                self.selected_characters[i].name,
                18,
                (734, 528 + i * 79),
            )
            drop_shadow_text(
                self._display_surf,
                f"{self.selected_characters[i].health}/{self.selected_characters[i].max_health}",  # noqa: E501
                18,
                (868, 528 + i * 79),
            )
        for i in range(2):
            self.enemies[i].render(self._display_surf)
        self._selection_arrow.render(self._display_surf)

    def select_target(self, command: str, self_char):
        if command == "ATTACK":
            if type(self_char) is Character:
                if self.enemies[0].health > 0:
                    return self.enemies[0]
                elif self.enemies[1].health > 0:
                    return self.enemies[1]
            elif type(self_char) is Enemy:
                if self.selected_characters[0].health > 0:
                    return self.selected_characters[0]
                elif self.selected_characters[1].health > 0:
                    return self.selected_characters[1]
                elif self.selected_characters[2].health > 0:
                    return self.selected_characters[2]
        elif command == "DEFENSE":
            return None
        elif command == "INSIGHT":
            return None
        elif command == "SKILL":
            return None

    def on_turn(self, command: str):
        if self.battle_array[self._actual_turn].health <= 0:
            self.battle_array[self._actual_turn].health = 0
            if self._actual_turn >= 4:
                self._actual_turn = -1
            self._actual_turn += 1
            return
        self.turn = self.battle_array[self._actual_turn].name
        self.battle_array[self._actual_turn].action(
            command,
            self.select_target(
                command, self.battle_array[self._actual_turn]
            ),  # noqa: E501
        )  # noqa: E501
        if self.enemies[0].health <= 0 and self.enemies[1].health <= 0:
            pygame.draw.rect(
                self._display_surf, (180, 180, 180), (20, 504, 678, 245)
            )  # noqa: E501
            drop_shadow_text(self._display_surf, "YOU WIN", 64, (71, 529))
            pygame.display.flip()
            sleep(5)
            self._running = False
        if self._actual_turn >= 4:
            self._actual_turn = -1
        self._actual_turn += 1

    def execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.event_handler(event)

            self._display_surf.blit(self.background, (0, 0))

            if self._selected_chars >= 3:
                self.on_battle()
                for c in self.battle_array:
                    print(c.name, c.health)
            else:
                self.on_main_menu()

            pygame.display.flip()

        self.cleanup()


if __name__ == "__main__":
    game = Game(1024, 768)
    game.execute()
