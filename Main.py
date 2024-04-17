import kivy
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.metrics import dp

# Configuration des dimensions de la fenêtre pour simuler un appareil mobile
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

# Configuration du backend OpenGL pour éviter des problèmes de compatibilité
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

# Vérification de la version de Kivy
kivy.require('1.11.1')

class TicTacToeApp(App):
    def build(self):
        self.current_player = 'X'
        self.game_over = False
        self.moves = []
        self.grid = GridLayout(cols=3, spacing=dp(10), size_hint=(1, 0.8))
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.status_label = Label(text="Player X's turn", size_hint=(1, 0.1), font_size=dp(18))

        for r in range(3):
            for c in range(3):
                btn = Button(text='', font_size=dp(24), background_normal='', background_color=[0.88, 0.88, 0.88, 1])
                btn.bind(on_press=lambda btn, r=r, c=c: self.on_button_click(btn, r, c))
                self.buttons[r][c] = btn
                self.grid.add_widget(btn)

        self.reset_button = Button(text='Reset Game', size_hint=(1, 0.1), font_size=dp(18))
        self.reset_button.bind(on_press=self.reset_game)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.status_label)
        layout.add_widget(self.grid)
        layout.add_widget(self.reset_button)

        return layout

    def on_button_click(self, btn, r, c):
        if btn.text == "" and not self.game_over:
            btn.text = self.current_player
            btn.background_color = [0.97, 0.97, 0.81, 1] if self.current_player == 'X' else [0.71, 0.85, 0.95, 1]
            self.moves.append((r, c, self.current_player))

            if len(self.moves) > 6:
                oldest_move = self.moves.pop(0)
                old_btn = self.buttons[oldest_move[0]][oldest_move[1]]
                old_btn.text = ''
                old_btn.background_color = [0.82, 0.82, 0.82, 1]

            if self.check_winner(self.current_player):
                self.game_over = True
                self.show_popup(f"Player {self.current_player} wins!")
            elif self.is_draw():
                self.game_over = True
                self.show_popup("It's a draw!")

            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.status_label.text = f"Player {self.current_player}'s turn"

    def check_winner(self, player):
        b = self.buttons
        for i in range(3):
            if all(b[i][j].text == player for j in range(3)) or all(b[j][i].text == player for j in range(3)):
                return True
        if all(b[i][i].text == player for i in range(3)) or all(b[i][2-i].text == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.buttons[r][c].text != "" for r in range(3) for c in range(3)) and not self.game_over

    def reset_game(self, instance=None):
        self.game_over = False
        self.moves = []
        for row in self.buttons:
            for btn in row:
                btn.text = ""
                btn.background_color = [0.88, 0.88, 0.88, 1]
        self.current_player = 'X'
        self.status_label.text = "Player X's turn"

    def show_popup(self, message):
        popup = Popup(title='Game Over', content=Label(text=message), size_hint=(None, None), size=(200, 200))
        popup.open()

# Démarrez l'application
if __name__ == '__main__':
    TicTacToeApp().run()
