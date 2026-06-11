import random

class Game:
    PLAYER = 1
    OBSTACLE = 2
    EMPTY = 0
    
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player_pos = 1
        self.player_row = 4
        self.score = 0
        self.game_over = False
        self.collision_occurred = False
        
    def move_player(self, direction):
        if self.game_over:
            return False
        
        new_pos = self.player_pos + direction
        
        if 0 <= new_pos <= 2:
            if self.board[self.player_row][new_pos] == self.OBSTACLE:
                return False
            self.player_pos = new_pos
            return True
        return False
    
    def spawn_obstacle(self):
        if self.game_over:
            return
        if any(self.board[1][col] == self.OBSTACLE for col in range(3)):
            return
        count = random.randint(1, 2)
        cols = random.sample(range(3), count)
        for col in cols:
            self.board[0][col] = self.OBSTACLE
    
    def descend_obstacles(self):
        if self.game_over:
            return
        
        new_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == self.OBSTACLE:
                    if row + 1 < 5:
                        new_board[row + 1][col] = self.OBSTACLE
        
        self.board = new_board
    
    def check_collision(self):
        if self.board[self.player_row][self.player_pos] == self.OBSTACLE:
            self.game_over = True
            self.collision_occurred = True
            return True
        return False
    
    def update_game(self):
        if self.game_over:
            return
        
        self.descend_obstacles()
        self.spawn_obstacle()
        
        if self.check_collision():
            self.game_over = True
        else:
            self.score += 1
    
    def get_board_display(self):
        display_board = [row[:] for row in self.board]
        display_board[self.player_row][self.player_pos] = self.PLAYER
        return display_board
    
    def is_game_over(self):
        return self.game_over
    
    def get_score(self):
        return self.score
