import Snake
import Population
import Food
import NeuroNetwork
import Matrix
import numpy as np
#set const values
#-----------------------------------------------
#consts for game logic
SIZE = 20
hidden_nodes = 16
hidden_layers = 2
fps = 100
highscore = 0

mutationRate = 0.05
defaultmutation = 0.05

humanPlaying = False
replayBest = True
seeVision = False
modelLoaded = False

evolution = []
#这里只是为了确定变量类型
snake = Snake.Snake()
model = Snake.Snake()

pop
#consts for graphical rendering
WND_WIDTH = 1200
WND_HEIGHT = 800
#font, buttons, evolution graph ...
#-----------------------------------------------
#渲染 + 更新逻辑
def loop():
    #draw game stage
    #
    if humanPlaying :
        snake.move()
        snake.show()
        #draw text, show snake score
        #
        if snake.dead :
            snake = Snake.Snake()
    #AI ctrl
    #------------------------------------------
    else :
        if not modelLoaded:
            if pop.done() :
                #运用遗传算法, 产生下一代
                highscore = pop.bestSnake.score
                pop.calculateFitness()
                pop.naturalSelection()
            else :
                #AI控制输出
                pop.update()
                pop.show()
                #draw text, show generation, mutation rate, score, highscore
                #show buttons
                #

        #model loaded:
        else :
            model.look()
            model.think()
            model.move()
            model.show()
            #show neuro network
            #model.brain.show(...)
            if model.dead:
                new = Snake.Snake()
                new.brain = model.brain.clone()
                model = new
            #draw text
            #draw button
            #
    return
#对应SnakeAI.pde::fileSelectedIn
#先用固定的文件路径, 以省略传参
def load_model():
    #file access
    out = np.zeros((4, hidden_nodes + 1))
    #load out ...
    weights = Matrix.Matrix(out)
    #
    #实例化model
    model = Snake.Snake(len(weights) - 1)
    model.brain.load(weights)
    return
#对应SnakeAI.pde::fileSelectedOut
#先用固定的文件路径, 以省略传参
def save_model():
    pass
if __name__ == "__main__":
    #set up
    #-----------------------------------------
    if humanPlaying :
        snake = Snake.Snake()
    else :
        #需要有个地方能让用户输入modelLoaded的值
        if not modelLoaded:
            pop = Population.Population(2000)
        else :
            load_model()
    #graphical set ups:

    #-----------------------------------------
    #loop