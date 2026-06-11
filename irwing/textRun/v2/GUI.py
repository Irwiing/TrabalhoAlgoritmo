import os
import sys
import time

GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

try:
    import msvcrt
    def getch():
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            arrow_map = {b'H': '\x1b[A', b'P': '\x1b[B', b'K': '\x1b[D', b'M': '\x1b[C'}
            return arrow_map.get(ch2, '')
        return ch.decode('utf-8', errors='replace')
except ImportError:
    import tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return '\x1b[' + ch3
                return '\x1b'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

from Game import Game
from Ranking import Ranking

class GUI:
    def __init__(self):
        self.MenuOptions = { 1: "Jogar", 2: "Ranking", 3: "Como Jogar", 4: "Sair" }
        self.game = None
        self.ranking = Ranking()

    def ShowMainMenu(self):
        self._render_menu(1)

    def _render_menu(self, selected):
        self.ClearScreen()
        print("=== TEXT RUN ===\n")
        for index, option in self.MenuOptions.items():
            if index == selected:
                print(f"{YELLOW}{BOLD}> {index}. {option}{RESET}")
            else:
                print(f"  {index}. {option}")

    def GetMainMenuInput(self):
        selected = 1
        max_option = len(self.MenuOptions)
        self._render_menu(selected)
        while True:
            key = getch()
            if key == '\x1b[A':
                selected = max(1, selected - 1)
                self._render_menu(selected)
            elif key == '\x1b[B':
                selected = min(max_option, selected + 1)
                self._render_menu(selected)
            elif key in ('\r', '\n'):
                return selected
            elif key.isdigit() and 1 <= int(key) <= max_option:
                return int(key)

    def ShowStartScreen(self):
        self.ClearScreen()
        print("Bem vindo ao Text Run")
        print("Jogo desenvolvido como trabalho de Algoritmos")
        print("Selecione qualquer tecla para continuar...")
        getch()
        self.ClearScreen()

    def ShowHowToPlayScreen(self):
        self.ClearScreen()
        print("=== COMO JOGAR ===")
        print("Você controla um carro (P) que deve desviar de obstáculos (#)")
        print("que descem pela tela.")
        print()
        print("Controles:")
        print("  A - Mover para esquerda")
        print("  D - Mover para direita")
        print("  S - Não se mover")
        print()
        print("Objetivo: Desvie dos obstáculos o máximo de tempo possível!")
        print()
        print("Pressione qualquer tecla para voltar ao menu...")
        getch()

    def ShowRankingScreen(self):
        self.ClearScreen()
        print("╔════════════════════════════════╗")
        print("║         TOP 10 RANKING          ║")
        print("╚════════════════════════════════╝")
        print()
        
        rankings = self.ranking.get_top_10()
        
        if not rankings:
            print("Nenhuma pontuação registrada ainda!")
        else:
            print("POS  NOME  SCORE")
            print("-" * 25)
            for i, entry in enumerate(rankings, 1):
                print(f"{i:2d}.  {entry['name']:3s}  {entry['score']:4d}")
        
        print()
        print("Pressione qualquer tecla para voltar ao menu...")
        getch()

    def DisplayBoard(self, board, score):
        self.ClearScreen()
        print("=== TEXT RUN ===")
        print(f"Score: {score}")
        print()
        
        symbols = {
            0: ".",
            1: GREEN + "P" + RESET,
            2: RED   + "#" + RESET,
        }
        
        for i, row in enumerate(board):
            row_str = "[ " + " | ".join(symbols[cell] for cell in row) + " ]"
            if i == 4:
                print(">>> " + row_str + " ← YOU")
            else:
                print("    " + row_str + "      ")
        
        print()
        print("Controles: A/← (esquerda) | D/→ (direita)")
        print()

    def GetPlayerInput(self):
        while True:
            try:
                print("Digite seu movimento (A/D/S): ", end='', flush=True)
                key = getch().upper()
                print(key)
                if key in ['A', 'D', 'S']:
                    if key == 'A':
                        return -1
                    elif key == 'D':
                        return 1
                    else:
                        return 0
                else:
                    print("Comando inválido! Use A (esquerda), D (direita) ou S (não mover)")
            except Exception:
                print("Erro ao processar entrada")

    def ShowGameScreen(self):
        self.game = Game()
        TICK = 0.5  # segundos entre cada descida de obstáculo

        self.DisplayBoard(self.game.get_board_display(), self.game.get_score())
        last_tick = time.time()

        try:
            import select as _sel, tty as _tty, termios as _ter

            fd = sys.stdin.fileno()
            old = _ter.tcgetattr(fd)

            def _key(timeout):
                # Raw mode só durante a leitura; restaura antes de qualquer print
                _tty.setraw(fd)
                try:
                    r, _, _ = _sel.select([sys.stdin], [], [], max(0, timeout))
                    if not r:
                        return None
                    ch = sys.stdin.read(1)
                    if ch == '\x1b':
                        r2, _, _ = _sel.select([sys.stdin], [], [], 0.05)
                        if r2:
                            ch2 = sys.stdin.read(1)
                            if ch2 == '[':
                                r3, _, _ = _sel.select([sys.stdin], [], [], 0.05)
                                if r3:
                                    return '\x1b[' + sys.stdin.read(1)
                        return '\x1b'
                    return ch.upper() if ch.isalpha() else ch
                finally:
                    _ter.tcsetattr(fd, _ter.TCSADRAIN, old)

            try:
                while not self.game.is_game_over():
                    now = time.time()
                    key = _key(TICK - (now - last_tick))
                    moved = False
                    if key in ('A', '\x1b[D'):
                        self.game.move_player(-1)
                        moved = True
                    elif key in ('D', '\x1b[C'):
                        self.game.move_player(1)
                        moved = True
                    elif key == '\x03':  # Ctrl+C
                        break
                    now = time.time()
                    ticked = now - last_tick >= TICK
                    if ticked:
                        self.game.update_game()
                        last_tick = now
                    if (moved or ticked) and not self.game.is_game_over():
                        self.DisplayBoard(self.game.get_board_display(), self.game.get_score())
            finally:
                _ter.tcsetattr(fd, _ter.TCSADRAIN, old)

        except ImportError:
            # Fallback Windows: usa threading
            import threading, queue
            q = queue.Queue()
            running = [True]

            def _reader():
                while running[0]:
                    try:
                        k = getch()
                        if running[0]:
                            q.put(k.upper() if len(k) == 1 else k)
                    except Exception:
                        pass

            threading.Thread(target=_reader, daemon=True).start()

            while not self.game.is_game_over():
                now = time.time()
                moved = False
                try:
                    key = q.get(timeout=max(0.01, TICK - (now - last_tick)))
                    if key == 'A':
                        self.game.move_player(-1)
                        moved = True
                    elif key == 'D':
                        self.game.move_player(1)
                        moved = True
                except queue.Empty:
                    pass
                now = time.time()
                ticked = now - last_tick >= TICK
                if ticked:
                    self.game.update_game()
                    last_tick = now
                if (moved or ticked) and not self.game.is_game_over():
                    self.DisplayBoard(self.game.get_board_display(), self.game.get_score())

            running[0] = False

        final_score = self.game.get_score()
        player_name = self.GetPlayerNamePinball()
        if player_name:
            self.ranking.add_score(player_name, final_score)
        self.ShowGameOverScreen(final_score, player_name)

    def GetPlayerNamePinball(self):
        self.ClearScreen()
        print("╔════════════════════════════════╗")
        print("║      DIGITE SEU NOME (3)        ║")
        print("╚════════════════════════════════╝")
        print()
        
        name = []
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        current_index = [0, 0, 0]
        
        for pos in range(3):
            while True:
                self.ClearScreen()
                print("╔════════════════════════════════╗")
                print("║      DIGITE SEU NOME (3)        ║")
                print("╚════════════════════════════════╝")
                print()
                
                display = ""
                for i in range(3):
                    if i == pos:
                        char = letters[current_index[i]]
                        display += f"[{char}]"
                    else:
                        if i < len(name):
                            display += f" {name[i]} "
                        else:
                            display += f" _ "
                
                print(f"Nome: {display}")
                print()
                print("W - Anterior  |  S - Próximo  |  Enter - Confirmar")
                
                try:
                    key = getch()
                    if key in ['\r', '\n']:
                        name.append(letters[current_index[pos]])
                        break
                    key = key.strip().upper()
                    if key in ('W', '\x1b[A'):
                        current_index[pos] = (current_index[pos] - 1) % len(letters)
                    elif key in ('S', '\x1b[B'):
                        current_index[pos] = (current_index[pos] + 1) % len(letters)
                except:
                    pass
        
        return ''.join(name).upper()

    def ShowGameOverScreen(self, score, player_name=None):
        self.ClearScreen()
        print("╔════════════════╗")
        print("║   GAME OVER!   ║")
        print("╚════════════════╝")
        print()
        print(f"Score Final: {score}")
        if player_name:
            print(f"Jogador: {player_name}")
        print()
        print("Pressione qualquer tecla para voltar ao menu...")
        getch()

    def ClearScreen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            print('\033[2J\033[H', end='', flush=True)
