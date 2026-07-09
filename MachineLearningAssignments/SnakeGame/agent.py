import random

class Agent:
    def __init__(self):
        self.q_table = {}
        self.epsilon = 1
        
    def get_q_values(self, state):
        state = tuple(state)
        
        if state not in self.q_table:
            self.q_table[state] = [0,0,0,0]
            
        return self.q_table[state]
    
    def choose_action(self, state):
        q_values  = self.get_q_values(state)
        
        #Explore
        if random.random() < self.epsilon:
            return random.randint(0, 3)
        
        #Exploit
        return q_values.index(max(q_values))
    
    def update_q_value(self, state, action, reward, next_state):
        learning_rate = 0.1
        discount = 0.9
        
        q_values = self.get_q_values(state)
        current_q = q_values[action]
        next_q_values = self.get_q_values(next_state)
        best_future_q = max(next_q_values)
        
        new_q = current_q + learning_rate * (
        reward + discount * best_future_q - current_q
        )
        
        q_values[action] = new_q
        