from snake_game import SnakeGame
from agent import Agent

game = SnakeGame()
agent = Agent()

episodes = 1000

total_score = 0

for episode in range(episodes):

    game.reset()

    state = game.get_state()

    done = False

    steps = 0

    while not done:

        steps += 1

        action = agent.choose_action(state)

        next_state, reward, done = game.step(action)

        agent.update_q_value(
            state,
            action,
            reward,
            next_state
        )

        state = next_state

    total_score += game.score

    #Epsilon decay
    if agent.epsilon > 0.01:
        agent.epsilon *= 0.995

    #Every 100 episodes
    if (episode + 1) % 100 == 0:

        print(
            f"Episode {episode + 1}, "
            f"Average Score: {total_score / 100:.2f}, "
            f"Epsilon: {agent.epsilon:.3f}"
        )

        total_score = 0