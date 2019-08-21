"""
初始函数
__init__(self,number=-1,generation=-1,hidden_layers=2,replay=False,foods=None)
number是蛇的序号，可以不传；
generation是该蛇在整个种群中的代数，可以不传
hidden_layers指蛇的大脑，即神经网络隐藏层的层数；输入层节点和输出层节点的个数都已经固定，要修改只能在代码中修改
replay表明该蛇是不是所处的一代中最为优秀的，在训练过程中的蛇不需要传参：
    当其值为True时，需要传递食物列表；其值为False时，则不需要

碰撞检测函数：
bodyCollide(self,x,y)
x,y是蛇的头部坐标；这个函数可以用来检测当前蛇的状态，判断是否撞到了自己的身体
foodCollide(self,x,y)
x,y是蛇的头部坐标；这个函数可以用来检测当前蛇的状态，判断是否“撞上了”食物，可以用来判断是不是吃到了食物
wallCollide(self,x,y)
x,y是蛇的头部坐标；这个函数可以用来检测当前蛇的状态，判断是否撞上了墙

蛇的运动函数
move(self)
调用此函数之前首先要设置self.xVel和self.yVel，即小蛇动的方向
eat(self)
控制蛇吃下食物
shiftBody(self)
移动蛇身

克隆函数、基因相关函数
cloneForReplay(self)
克隆该蛇，以便于呈现给用户
clone(self)
克隆该蛇，与前一个函数的区别在于：cloneForReplay(self)还克隆了食物列表
crossover(self,parent)
将本蛇与传进来的另一条蛇杂交，将返回一个子蛇对象
mutate(self,mutationRate=0.05)
可以用来对个体蛇进行基因突变；突变率可以不传，默认为0.05

评价指标函数
calculateFitness(self)
计算适应率，需要调用才会计算！

look(self)
让小蛇看看八周
look_in_direction(self,direction)
look函数中调用，一般不需要使用，调试时可以使用

think(self)
思考应该往哪个方向走，结果保存在decision列表中

moveUp()/moveDown()/moveLeft()/moveRight()这四个函数由think()函数调用，函数将会对xVel和yVel进行修改
"""

from foodClass import Food
from NeuralNetClass import NeuralNet
import sys

SIZE=20#一格的边长
height=800#也许是蛇活动的最大高度？
width=800  #大概懂了，height和width是由整体窗口的大小，其中的分布由自己定
humanPlaying=False
modelLoaded=False
hidden_nodes=16

class Snake:                    #两层隐藏层，所以一共三层计算    foods是食物列表，如果replay==True，那么既要传递foods
    def __init__(self,number=-1,generation=-1,hidden_layers=2,replay=False,foods=None):
        self.number=number           #蛇的编号 ,默认为-1
        self.generation=generation   #该蛇所属代数，默认为-1
        self.hidden_layers=hidden_layers

        #评价指标
        self.score=1
        self.lifeLeft=200
        self.lifetime=0
        self.fitness=0

        #蛇的训练变量
        self.head=[40*SIZE,height/2]
        self.xVel,self.yVel=0
        self.body=[]       #身体节点用列表存储
        self.foodList=[]   #只能存储Food对象
        #该神经网络的食物，在机器学习时，采用的是固定的食物列表。以后版本可以尝试随机食物列表
        self.foodItterate=0
        #食物
        self.food=Food()
        #大脑
        self.brain=None

        #训练指标
        self.dead=False
        self.replay=False
        self.vision=[]    #存放蛇所能看到的，即神经网络的输入列表，这里是需要改进的，输入参数过于局限
        self.decision=[]  #蛇所做出的决定，即神经网络的输出列表。作为一个列表是因为本神经网络采用
                          #最大概率输出，即向着值最大的输出节点前进


        #如果该蛇是表现最好的蛇
        if replay==True:
            self.vision=[0]*24
            self.decision=[0]*24
            self.foodList=[None]*len(foods)
            for fooditem in foods:
                self.foodList.append(fooditem.clone())
            try:
                self.food=self.foodList[self.foodItterate]
            except:
                print('要取得食物超出界限了嗷')
                sys.exit(-1)
            self.foodItterate+=1
            self.body.append([40*SIZE,height/2+SIZE])
            self.body.append([40*SIZE,height/2+2*SIZE])
            self.score+=2

        #------------------------unknown  operation   inside-----------------------------
        #机器在训练
        if humanPlaying==False:
            self.vision=[0]*24
            self.decision=[0]*4
            self.foodList.append(self.food.clone())  #这个克隆是干啥的？！
            self.brain=NeuralNet(24,hidden_nodes=hidden_nodes,output_nodes=4,hidden_layers=self.hidden_layers)

            #初始化蛇的身体，头在40*SIZE,height/2处，身体从上往下一共两个，这也是之前score初始化为1的原因
            self.body.append([40*SIZE,height/2+SIZE])
            self.body.append([40*SIZE,height/2+2*SIZE])
            self.score+=2     #开局三分hhh

    #检测走出下一步后是否撞上了自己的身体
    def bodyCollide(self,x,y):
        """
        for i in range(len(self.body)):
            if x==self.body[i][0] and y==self.body[i][1]:
                return True
        """
        if [x,y] in self.body:
            return True
        return False

    #检测是否撞上食物，即是否吃到了食物
    def foodCollide(self,x,y):
        if x==self.food.return_pos()['x'] and y==self.food.return_pos()['y']:
            return True
        return False

    #检测是否撞墙
    def wallCollide(self,x,y):
           #超出右边界         超出左边界         超出下边界  超出上边界
        if x>=width-SIZE or x<400+SIZE or y>=height-SIZE or y<SIZE:
            return True
        return False

    #------------------------蛇的动作函数------------------------
    def move(self):
        if self.dead==False:     #如果蛇还没死
            if humanPlaying==False and modelLoaded==False:
                self.lifetime+=1    #已存活时间+1
                self.lifeLeft-=1    #可走步数-1
            if self.foodCollide(self.head[0],self.head[1]):
                self.eat()       #吃掉食物eat()
            self.shiftBody()     #整体向前动一下

            #以下情况都判定蛇死亡
            if self.wallCollide(self.head[0],self.head[1]):   #如果撞墙了
                self.dead=True
            elif self.bodyCollide(self.head[0],self.head[1]): #如果撞到自己的身体了
                self.dead=True
            elif self.lifeLeft<=0 and humanPlaying==False:   #如果生命到头了
                self.dead=True
    #咱们先看下面的函数吧,eat()/shiftbody(),etc
    #------------------------------------------------------------

    def eat(self):
        length=len(self.body)-1    #身体的长度-1
        self.score+=1              #吃到了食物，成绩+1
        #奖励机制   也许可以采用更加平滑的奖励机制，用一个连续函数来代替该跳跃函数
        if humanPlaying==False and modelLoaded==False:
            if self.lifeLeft<500:
                if self.lifeLeft>400: self.lifeLeft=500
                else:self.lifeLeft+=100
        #???
        #----------------------------看不太懂这操作--------------------------
        if length>=0:
            self.body.append([self.body[length][0],self.body[length][1]])
        else:
            self.body.append([self.head[0],self.head[1]])
        #--------------------------------------------------------------------

        if self.replay==False:
            #生成一个不在蛇身体和头（？）上的食物
            self.food=Food()
            while self.bodyCollide(self.food.return_pos()['x'],self.food.return_pos()['y']):
                self.food=Food()
            if humanPlaying==False:
                self.foodList.append(self.food)
        #如果这条蛇是演示蛇
        else:
            self.food=self.foodList[self.foodItterate]   #演示蛇直接从食物列表中读取
            self.foodItterate+=1

    def shiftBody(self):
        tempx,tempy=self.head[0],self.head[1]
        self.head[0]+=self.xVel
        self.head[1]+=self.yVel

        self.body=self.body[:-1].insert(0,[tempx,tempy])

    #-------------------------undo---------------------------------
    def cloneForReplay(self):
        clone=Snake(replay=True,foods=self.foodList.copy())
        clone.brain=self.brain.clone()           #这一行代码需要实现
        return clone

    def clone(self):
        clone=Snake(hidden_layers=self.hidden_layers)
        clone.brain=self.brain.clone()
        return clone

    #将该蛇与其他蛇杂交
    def crossover(self,parent):
        child=Snake(hidden_layers=self.hidden_layers)
        child.brain=self.brain.crossover(parent.brain)
        return child

    #突变率的设置
    def mutate(self,mutationRate=0.05):
        self.brain.mutate(mutationRate)
    #--------------------------------------------------------------
    #计算蛇本蛇的适应率，这将是进化选择的重要依据！
    #这里的评价机制也许可以做出适当的改进
    def calculateFitness(self):
        if self.score<10:
            self.fitness=(self.lifetime**2)*(2**self.score)
        else:
            self.fitness=(self.lifetime**2)*(2**10)*(self.score-9)  #???什么鬼评价

    #蛇的视界所看到的
    #正如原代码所介绍的，蛇只能看到它的八个方向的任何事物；也许改进时可以将小蛇的坐标归一化后也作为输入
    def look(self):
        temp=self.look_in_direction([-SIZE,0])
        self.vision.extend(temp)
        temp=self.look_in_direction([-SIZE,-SIZE])
        self.vision.extend(temp)
        temp=self.look_in_direction([0,-SIZE])
        self.vision.extend(temp)
        temp=self.look_in_direction([SIZE,-SIZE])
        self.vision.extend(temp)
        temp=self.look_in_direction([SIZE,0])
        self.vision.extend(temp)
        temp=self.look_in_direction([SIZE,SIZE])
        self.vision.extend(temp)
        temp=self.look_in_direction([0,SIZE])
        self.vision.extend(temp)
        temp=self.look_in_direction([-SIZE,SIZE])
        self.vision.extend(temp)

    #就判断一下有没有撞到身体、撞到墙、吃到食物
    def look_in_direction(self,direction):
        what_the_snake_looked=[0]*3
        pos=[self.head[0],self.head[1]]
        distance=0#what's this?
        foodFound=False
        bodyFound=False

        #假想蛇的头向指定方向爬出一步
        pos[0]+=direction[0]
        pos[1]+=direction[1]
        distance+=1  #走出一步

        #如果头没有撞到墙里面去???
        #这个while的目的在于，让蛇可以看到特定方向上的所有格子
        #但是，这也存在局限性，就是蛇无法看到斜角线上的东西
        #比如：
        #  食物  □    □
        #  □    □    蛇头
        while self.wallCollide(pos[0],pos[1])==False:
            #如果这个方向可以吃到食物
            if foodFound==False and self.foodCollide(pos[0],pos[1]):
                foodFound=True
                what_the_snake_looked[0]=1
            #如果这个方向是来时的方向
            if bodyFound==False and self.bodyCollide(pos[0],pos[1]):
                bodyFound=True
                what_the_snake_looked[1]=1

              # codes waiting for rewrite
              #       if(replay && seeVision) {
              #          stroke(0,255,0);
              #          point(pos.x,pos.y);
              #          if(foodFound) {
              #               noStroke();
              #               fill(255,255,51);
              #               ellipseMode(CENTER);
              #               ellipse(pos.x,pos.y,5,5);
              #              }
              #           if(bodyFound) {
              #               noStroke();
              #               fill(102,0,102);
              #               ellipseMode(CENTER);
              #               ellipse(pos.x,pos.y,5,5);
              #           }
              #         }

            pos[0]+=direction[0]
            pos[1]+=direction[1]
            distance+=1
        #end while
        # codes waiting for rewrite
        #     if(replay && seeVision) {
        #         noStroke();
        #         fill(0,255,0);
        #         ellipseMode(CENTER);
        #         ellipse(pos.x,pos.y,5,5);
        #     }
        what_the_snake_looked[2]=1/distance    #这个厉害，直接归一化了
        return what_the_snake_looked
    #end function:look_in_direction

    #-----------------------------undo------------------------------
    #go through the network to decide which direction to go
    def think(self):
        self.decision=self.brain.output(self.vision)
        maxIndex=0
        max=0
        for j in range(len(self.decision)):
            if self.decision[j]>max:
                max=self.decision[j]
                maxIndex=j

        if maxIndex==0:
            self.moveUp()
        elif maxIndex==1:
            self.moveDown()
        elif maxIndex==2:
            self.moveLeft()
        elif maxIndex==3:
            self.moveRight()

    #end think
    #---------------------------------------------------------------
    def moveUp(self):
        if self.yVel!=SIZE:
            self.xVel=0
            self.yVel=-SIZE
    def moveDown(self):
        if self.yVel!=-SIZE:
            self.xVel=0
            self.yVel=SIZE
    def moveLeft(self):
        if self.xVel!=SIZE:
            self.xVel=-SIZE
            self.yVel=0
    def movRight(self):
        if self.xVel!=-SIZE:
            self.xVel=SIZE
            self.yVel=0