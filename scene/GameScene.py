from typing import Tuple, Optional, Dict, Any

import pygame
from pygame.surface import Surface
from pygame.event import Event

from Settings import ColorSettings
from Resources import Images, Fonts
from board.Board import Board, BoardState, PlayerId
from scene.Scene import Scene, SceneId
from scene.SceneHandler import SceneSignals
from ui.Constants import UI_BUTTON_COLORS
from ui.Button import ButtonColors
from ui.IconButton import Button, IconButton
from ui.BoardUI import BoardUI
from ui.GameOverPopup import GameOverPopup
from ui.Colors import Colors
import ui.GraphicUtils as GraphicUtils
                        
class GameScene(Scene):
    def __init__(self, screen: Surface, board: Board, flipped: bool = False):
        self.id = SceneId.GAME
        self.options = {}
        self.screen = screen
        self.width, self.height = screen.get_rect().size
        self.board = board
        self.board_ui = BoardUI(self.screen, board, (600, 600), (100, 50))
        self.flipped = flipped
        self.create_buttons()

        # Popup
        self.popup_game_over = GameOverPopup(self.screen, self)

        # Signals
        self.home_clicked = False

    def create_buttons(self) -> None:
        button_colors = ButtonColors(
            background=Colors.UI_BLACK.value,
            foreground=Colors.WHITE.value,
            highlight=Colors.BLACK.value,
            border=Colors.WHITE.value
        )
        home_button = IconButton(self.screen, (15, self.height - 125), (70, 70), Images.HOME.value, button_colors, self.handle_home_button, border_radius=50)
        surrender_button = IconButton(self.screen, (15, 50), (70, 70), Images.FLAG.value, button_colors, self.handle_surrender_button, border_radius=50)
        play_again_button = IconButton(self.screen, (15, 50), (70, 70), Images.REFRESH.value, button_colors, self.handle_play_again_button, border_radius=50, visible=False)
        self.buttons = [home_button, surrender_button, play_again_button]

    def handle_home_button(self) -> None:
        self.home_clicked = True

    def handle_surrender_button(self) -> None:
        # TODO: need to handle when online
        self.board.surrender(self.board.turn)

    def handle_play_again_button(self) -> None:
        # TODO: need to handle when online
        self.board.setup()

    # @override
    def handle_event(self, event: Event) -> Tuple[int, Optional[Dict[Any, Any]]]:
        if self.home_clicked:
            self.home_clicked = False
            return SceneSignals.HOME, None
        if self.popup_game_over.visible:
            self.popup_game_over.handle_event(event)
        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.hover(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button.click(mouse_x, mouse_y)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.handle_home_button()
            if self.board.state() == BoardState.NEUTRAL:
                return self.board_ui.handle_event(event)
        return SceneSignals.NONE, None

    def draw(self) -> None:
        GraphicUtils.draw_background(self.screen)
        self.board_ui.draw()
        self.draw_status()
        self.draw_players_num_pieces()

        _, surrender_button, play_again_button = self.buttons
        if self.board.state() == BoardState.IDLE:
            surrender_button.hide()
            play_again_button.show()
        else:
            surrender_button.show()
            play_again_button.hide()
        for button in self.buttons:
            button.draw()
        self.popup_game_over.draw()

    def draw_status(self) -> None:
        status_width = 175
        status_height = 45
        x = (self.width - status_width)
        top_y = 0
        bottom_y = self.height - status_height

        border_radius=20
        border = 8
        status_y = bottom_y if not self.flipped else top_y
        player_color = ColorSettings.player_one
        if self.board.turn == PlayerId.TWO:
            status_y = top_y if not self.flipped else bottom_y
            player_color = ColorSettings.player_two
        pygame.draw.rect(self.screen, Colors.WHITE.value, (x, status_y, status_width, status_height), border_top_left_radius=border_radius, border_bottom_left_radius=border_radius)
        pygame.draw.rect(self.screen, player_color, (x + (border / 2), status_y + (border / 2), status_width - border, status_height - border), border_top_left_radius=border_radius, border_bottom_left_radius=border_radius)
        self.draw_players_text(status_width, status_height, top_y, bottom_y)

    def draw_players_text(self, status_width: float, status_height: float, top_y: float, bottom_y: float) -> None:
        for player in self.board.players.values():
            draw_text = f"{player.id + 1}"
            if self.board.blitz_mode:
                time_remaining_s = self.board.player_loss_timeout_s - player.time_elapsed_s
                if time_remaining_s < 0:
                    time_remaining_s = 0
                draw_text = "%.2f" % round(time_remaining_s, 2)
            font_size = int(status_height / 2.5)
            text_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
            text_color = (128, 128, 128)
            if self.board.turn == player.id:
                if player.id == PlayerId.ONE:
                    text_color = ColorSettings.get_contrast_color(ColorSettings.player_one)
                else:
                    text_color = ColorSettings.get_contrast_color(ColorSettings.player_two)  
            text_render = text_font.render(draw_text, False, text_color)
            text_width, text_height = text_render.get_rect().size
            text_x = (self.width - (status_width / 2) - (text_width / 2.5))
            player_one_y = bottom_y if not self.flipped else top_y
            player_two_y = top_y if not self.flipped else bottom_y
            if player.id == PlayerId.ONE:
                text_y = player_one_y + (text_height / 2)
                self.screen.blit(text_render, (text_x, text_y))
            else:
                text_y = player_two_y + (text_height / 2)
                self.screen.blit(text_render, (text_x, text_y))

    def draw_players_num_pieces(self) -> None:
        piece_width, piece_height = (75, 75)
        y = self.height / 3
        player_id = PlayerId.TWO if not self.flipped else PlayerId.ONE
        self.draw_player_num_pieces(player_id, y)
        player_id = PlayerId.ONE if not self.flipped else PlayerId.TWO
        y += piece_height + 10
        self.draw_player_num_pieces(player_id, y)

    def draw_player_num_pieces(self, player_id: PlayerId, y: float) -> None:
        piece_width, piece_height = (75, 75)
        player_color = ColorSettings.player_one
        if player_id == PlayerId.TWO:
            player_color = ColorSettings.player_two
        GraphicUtils.draw_piece(self.screen, (10, y), (piece_width, piece_height), player_color, outline_color=Colors.WHITE.value, bg_size=10, outline_size=5)
        
        font_size = int(piece_width / 2)
        text_font = pygame.font.Font(Fonts.STAR_BORN.value, font_size)
        text_color = ColorSettings.get_contrast_color(player_color)

        if player_id == PlayerId.ONE:
            opp_player_id = PlayerId.TWO
        else:
            opp_player_id = PlayerId.ONE
            
        player = self.board.players[opp_player_id]
        text_render = text_font.render(str(len(player.pieces) - player.captured), False, text_color)
        text_width, text_height = text_render.get_rect().size
        self.screen.blit(text_render, (10 + ((piece_width - text_width) / 2), y + ((piece_height - text_height) / 2), text_width, text_height))
                
    def update(self) -> None:
        self.draw()
        self.board.update()
        if self.board.state() != BoardState.NEUTRAL and self.board.state() != BoardState.IDLE:
            if self.board.state() == BoardState.RED_WIN:
                self.popup_game_over.set_player_win(PlayerId.ONE)
            else:
                self.popup_game_over.set_player_win(PlayerId.TWO)
            self.popup_game_over.show()
