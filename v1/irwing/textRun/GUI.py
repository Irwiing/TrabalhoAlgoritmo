import os
from Game import Game

class GUI:
    def __init__(self):
        self.MenuOptions = { 1: "Jogar", 2: "Ranking", 3: "Como Jogar", 4: "Sair" }
        self.game = None

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
        print("Ranking...")
        print("(Funcionalidade não implementada)")
        input("Pressione Enter para voltar...")

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
        
        self.ShowGameOverScreen(score)

    def ShowGameOverScreen(self, score):
        self.ClearScreen()
        print("╔════════════════╗")
        print("║   GAME OVER!   ║")
        print("╚════════════════╝")
        print()
        print(f"Score Final: {score}")
        print()
        input("Pressione Enter para voltar ao menu...")

    def ClearScreen(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

