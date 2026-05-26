import os
from Game import Game
from Ranking import Ranking

class GUI:
    def __init__(self):
        self.MenuOptions = { 1: "Jogar", 2: "Ranking", 3: "Como Jogar", 4: "Sair" }
        self.game = None
        self.ranking = Ranking()

    def ShowMainMenu(self):
        self.ClearScreen()
        for index, option in self.MenuOptions.items():
            print(f"{index}. {option}")

    def GetMainMenuInput(self):
        return int(input("Escolha uma opção: "))

    def ShowStartScreen(self):
        self.ClearScreen()
        print("Bem vindo ao Text Run")
        print("Jogo desenvolvido como trabalho de Algoritmos")
        input("Selecione qualquer tecla para continuar...")
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
        input("Pressione Enter para voltar ao menu...")

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
        input("Pressione Enter para voltar ao menu...")

    def DisplayBoard(self, board, score):
        self.ClearScreen()
        print("=== TEXT RUN ===")
        print(f"Score: {score}")
        print()
        
        symbols = {0: ".", 1: "P", 2: "#"}
        
        for i, row in enumerate(board):
            row_str = "[ " + " | ".join(symbols[cell] for cell in row) + " ]"
            if i == 4:
                print(">>> " + row_str + " ← YOU")
            else:
                print("    " + row_str)
        
        print()
        print("Controles: A (esquerda) | D (direita) | S (não mover)")
        print()

    def GetPlayerInput(self):
        while True:
            try:
                move = input("Digite seu movimento (A/D/S): ").strip().upper()
                if move in ['A', 'D', 'S']:
                    if move == 'A':
                        return -1
                    elif move == 'D':
                        return 1
                    else:
                        return 0
                else:
                    print("Comando inválido! Use A (esquerda), D (direita) ou S (não mover)")
            except:
                print("Erro ao processar entrada")

    def ShowGameScreen(self):
        self.game = Game()
        
        while not self.game.is_game_over():
            board = self.game.get_board_display()
            score = self.game.get_score()
            
            self.DisplayBoard(board, score)
            
            player_move = self.GetPlayerInput()
            self.game.move_player(player_move)
            self.game.update_game()
        
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
                    key = input().strip().upper()
                    
                    if key == 'W':
                        current_index[pos] = (current_index[pos] - 1) % len(letters)
                    elif key == 'S':
                        current_index[pos] = (current_index[pos] + 1) % len(letters)
                    elif key == '':
                        name.append(letters[current_index[pos]])
                        break
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
        input("Pressione Enter para voltar ao menu...")

    def ClearScreen(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')


