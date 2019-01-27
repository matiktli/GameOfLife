
class Holder():
    def __init__(self, name="db"):
        self.name = name
        self.buffor = list()

    def add(self, genNo, life, death, eventBirth=0, eventDeath=0):
        ratio = life / (life + death)
        self.buffor.append((genNo, life, death, ratio))

    def getAll(self):
        return self.buffor
