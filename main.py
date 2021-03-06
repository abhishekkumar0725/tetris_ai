from tetris import Tetris
from agent import Agent

def run():
    game = Tetris()
    episodes = 2000
    discount=0.9 
    epsilon=.99
    nuerons=[32, 32, 32]
    activation_functions=['relu', 'relu', 'relu', 'linear']
    batchSize = 32
    epoch = 5
    trainIteration = 1

    dqn = Agent(4, discount, epsilon, nuerons, activation_functions)
    episodes = 2000
    scores = []
    for episode in range(episodes):
        current = game.newGame()
        gameOver, step = False, 0
        renderEpisode = episode % 50 == 0

        while not gameOver:
            actions = game.getLegalActions()
            bestAction, bestState = dqn.best_state(list(actions.keys()), list(actions.values()))

            reward, gameOver = game.play(xLoc=bestAction[0], degrees=bestAction[1], render=renderEpisode)
            dqn.add_sample(current, bestState, reward, gameOver)
            current = bestState
            scores.append(reward)
        
        if episode % trainIteration == 0:
            dqn.train(batch_size=batchSize, epoch=epoch)

if __name__ == '__main__':
    run()