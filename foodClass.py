import random
SIZE=20

class Food:
    def __init__(self):                #38是怎么来的??
        self.x=20*SIZE+SIZE+random.randint(0,38)*SIZE
        self.y=SIZE+random.randint(0,38)*SIZE

    def clone(self):
        clone=Food()
        clone.x=self.return_pos()[0]
        clone.y=self.return_pos()[1]
        return clone

    def return_pos(self):
        return {'x':self.x,'y':self.y}

    # codes waiting for rewrite
    # void show() {
    #    stroke(0);
    #    fill(255,0,0);
    #    rect(pos.x,pos.y,SIZE,SIZE);
    # }