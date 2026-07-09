import random

class SnakeGame:
    def __init__(self, width = 10, height = 20):
        self.width = width
        self.height = height
        
        self.reset()
        
    def reset(self):
        #Snake in the middle
        self.snake = [(self.height//2, self.width//2)]
        
        #Initial movement
        self.direction = "right"
        
        self.score = 0
        
        self.game_over = False
        
        self.spawn_food()
        
    def move(self):
        head_row, head_column = self.snake[0]
        
        if self.direction == 'up':
            head_row -= 1
            
        elif self.direction == 'down':
            head_row += 1
            
        elif self.direction == 'right':
            head_column += 1
            
        elif self.direction == 'left':
            head_column -= 1
            
        new_head = (head_row, head_column)
        self.snake.insert(0, new_head)
        
        if self.check_collision(new_head):
            self.game_over = True
            return
        
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()
    
    def spawn_food(self):
        while True:
            row = random.randint(0, self.height-1)
            column = random.randint(0, self.width-1)
            
            food_position = (row, column)
            
            #Food does not land on the snake
            if food_position not in self.snake:
                self.food = food_position
                break
            
    def print_board(self):
        board = []
        
        #Empty board
        for _ in range (self.height):
            row = ['  .'] * self.width
            board.append(row)
            
        #Food
        food_row, food_column = self.food
        board[food_row][food_column] = '  F'
        
        #Snake
        for index, (row, column) in enumerate(self.snake):
            if index == 0:
                board[row][column] = '  H'
                
            else:
                board[row][column] = '  O'
                
        #Top border
        print("+  " + "-  " * (self.width - 1) + " +")
        
        for row in board:
            print("|" + "".join(row) + "|")
        
        #Bottom border
        print("+  " + "-  " * (self.width - 1)+ " +")
        print(f"Score: {self.score}")
      
     #For the agent   
    def get_state(self):
        head_row, head_column = self.snake[0]
        
        if self.direction == "up":
            straight = (head_row - 1, head_column)
            left = (head_row, head_column - 1)
            right = (head_row, head_column + 1)
        elif self.direction == "down":
            straight = (head_row + 1, head_column)
            left = (head_row, head_column + 1)
            right = (head_row, head_column - 1)
        elif self.direction == "right":
            straight = (head_row, head_column + 1)
            left = (head_row - 1, head_column)
            right = (head_row + 1, head_column)
        elif self.direction == "left":
            straight = (head_row, head_column - 1)
            left = (head_row + 1, head_column)
            right = (head_row - 1, head_column)
        
        danger_straight = self.check_collision(straight)
        danger_left = self.check_collision(left)
        danger_right = self.check_collision(right)
        
        food_row, food_column = self.food

        food_up = food_row < head_row
        food_down = food_row > head_row
        food_left = food_column < head_column
        food_right = food_column > head_column
        
        moving_up = self.direction == "up"
        moving_down = self.direction == "down"
        moving_left = self.direction == "left"
        moving_right = self.direction == "right"

        state= [
            danger_straight,
            danger_left,
            danger_right,
            
            food_up,
            food_down,
            food_left,
            food_right,
            
            moving_up,
            moving_down,
            moving_left,
            moving_right
        ]
        
        return state
    
    #For the agent
    def step(self, action):

        directions = {
            0: "up",
            1: "down",
            2: "left",
            3: "right"
        }

        self.direction = directions[action]

        old_score = self.score

        #Move
        self.move()

        #Observe new situation
        next_state = self.get_state()

        #Calculate reward
        if self.game_over:
            reward = -10
            done = True

        elif self.score > old_score:
            reward = 10
            done = False

        else:
            reward = 0
            done = False

        return next_state, reward, done
    
    def check_collision(self, position=None):
        if position is None:
            position = self.snake[0]

        row, column = position

        # Wall collision
        if (
            row < 0
            or row >= self.height
            or column < 0
            or column >= self.width
        ):
            return True
        
        #Self-collision
        if position in self.snake[1:]:
            return True
        
        return False
                
            
        