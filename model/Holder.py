import matplotlib.pyplot as plt


class Holder():
    def __init__(self, name="db"):
        self.name = name
        self.buffor = list()

    def add(self, genNo, life, death, eventBirth=0, eventDeath=0):
        ratio = life / (life + death)
        self.buffor.append((genNo, life, death, ratio))

    def getAll(self):
        return self.buffor

    def plot(self, X_MIN=0, X_MAX=2500, Y_MIN=0, Y_MAX=2500):
        fig = plt.figure()
        pp = fig.add_subplot(111)
        pp.set_xlim(X_MIN, X_MAX)
        pp.set_ylim(Y_MIN, Y_MAX)
        pp.legend()
        for b in self.buffor:
            pp.plot(b[0], b[1], 'bo', label="gen: {0}_LIFE".format(b[0]), color='blue', markersize=5)
            pp.plot(b[0], b[2], 'ro', label="gen: {0}_DEATH".format(b[0]), color='red', markersize=5)
        plt.show()

    def findMinByY(self):
        min = self.buffor[0][1]
        for b in self.buffor:
            if b[1] < min:
                min = b[1]