import Snake
import random
'''
done():
update():
show():
setBestSnake():
selectParent():
naturalSelection():
mutate():
caculateFitness():
caculateFitnessSum():
'''
class Population():

    def __init__(self):
        self.snakes
        self.beskSnake
        self.bestSnakeScore = 0
        self.generation = 0
        self.samebest = 0
        self.bestFitness = 0.0
        self.fitnessSum = 0.0
    def Population(self,size):
        self.snakes = Snake[size]
        for i in range(len(self.snakes)):
            self.snakes[i] = Snake()
        self.bestSnake = self.snakes[0].clone()
        self.bestSnake.replay = True

    #检查是否种群中所有蛇都死亡
    def done(self):
        for i in range(len(self.snakes)):
            if self.snakes.isDead == False:
                return False
        if self.bestSnake.isDead == False:
            return False
        return True

    #更新种群中所有蛇
    def update(self):
        # 如果当前种群最优蛇没死，则保留最优蛇，并使它重新游戏
        if self.bestSnake.isDead == False:
            self.bestSnake.look()
            self.bestSnake.think()
            self.bestSnake.move()
        for i in range(len(self.snakes)):
            if self.snakes[i].isDead == False:
                self.snakes[i].look()
                self.snakes[i].think()
                self.snakes[i].move()

    def show(self):
        self.bestSnake.show();

    #设置最优蛇
    def setBestSnake(self):
        maxFitness = 0
        maxIndex = 0
        for i in range(len(self.snakes)):
            if self.snakes[i].fitness > maxFitness:
                maxFitness = self.snakes[i].fitness
                maxIndex = i
        if maxFitness > self.bestFitness:
            self.bestFitness = maxFitness
            self.bestSnake = self.snakes[maxIndex].cloneForReplay()
        else:
            self.bestSnake = self.bestSnake.cloneForReplay()

    # 选择随机父辈
    def selectParent(self):
        rand = random.uniform(0,self.fitnessSum)
        summation = 0
        for i in range(len(self.snakes)):
            summation += self.snakes[i].fitness
            if summation > rand:
                return self.snakes[i]
        return self.snakes[0]

    #神经选择
    def naturalSelection(self):
        newSnakes = Snake[len(self.snakes)]

        self.setBestSnake()
        self.caculateFitnessSum()

        newSnakes[0] = self.bestSnake.clone()
        for i in range(len(self.snakes)):
            child = self.selectParent().crossover(self.selectParent())
            child.mutate()
            newSnakes[i] = child
        self.snakes = newSnakes.clone()
        self.generation += 1

    #使种群中的蛇发生突变
    def mutate(self):
        #从1开始，因为snakes[0]总是储存上一代最优的蛇，不用突变
        for i in range(1,len(self.snakes),1):
            self.snakes[i].mutate()

    #计算每条蛇的适应度
    def caculateFitness(self):
        for i in range(len(self.snakes)):
            self.snakes[i].caculateFitness()

    def caculateFitnessSum(self):
        self.fitnessSum = 0
        for i in range(len(self.snakes)):
            self.fitnessSum += self.snakes[i].fitness


