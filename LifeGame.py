import numpy as np
import graphics as gp
import random as rd
from model import Logger as log
from model import Holder as hld
import matplotlib.pyplot as plt
import time

AREA_SIZE = 50  # HOW_MANY_WE_WANT_TO_SEE
CELL_SIZE = 5  # SIZE OF SINGLE CELL TO DETERMINE WINDOW SIZE
WINDOW_SIZE = AREA_SIZE * CELL_SIZE
TIME = 11000
AREA_NEW = np.zeros((AREA_SIZE, AREA_SIZE))
AREA_CURRENT = np.zeros((AREA_SIZE, AREA_SIZE))
LIFE, DEATH = 1, 0
DASHBOARD = np.zeros(10)
LOG = log.Logger("logger")
DB = hld.Holder("databaseXD")


def main():
    win = gp.GraphWin("GameLife", WINDOW_SIZE, WINDOW_SIZE)
    stats = plt.plot()
    win.setBackground((gp.color_rgb(0, 0, 0)))
    bckg = gp.Image(gp.Point(WINDOW_SIZE / 2, WINDOW_SIZE / 2), WINDOW_SIZE, WINDOW_SIZE)
    populateAreaRandomly(AREA_CURRENT, AREA_SIZE, 14)
    populateImageFromArea(bckg, AREA_CURRENT, CELL_SIZE, AREA_SIZE)
    bckg.draw(win)
    win.getMouse()
    newArea = AREA_CURRENT
    for i in range(0, TIME):
        newArea = evolve(newArea, AREA_SIZE, CELL_SIZE)
        if i > 1 and i % 20 == 0:
            newArea = addEventToArea(newArea, AREA_SIZE)
        populateImageFromArea(bckg, newArea, CELL_SIZE, AREA_SIZE)
        bckg.undraw()
        start = time.time()
        bckg.draw(win)
        stop = time.time()
        prctg,life,death = checkStatusOfArea(newArea)
        DASHBOARD[i % 5] = prctg
        if prctg == 0:
            LOG.log("END", "[gen: {0}] ALL DEAD".format(i))
            break
        sumLast = 0
        for dbx in range(4, 9):
            sumLast += DASHBOARD[dbx]
        sumLast = sumLast / 5 / DASHBOARD[9]
        if sumLast < 0.99965:
            LOG.log("STABLE", "[gen: {0}] Reached stable state".format(i))
            break
        LOG.log("EVOLVING", "[gen: {0}]There is only life percentage: [{1}], in all cells.".format(i, prctg))
        DB.add(i, life, death, prctg)
        time.sleep(0.06)

    win.close()


def draw2ndImageOneByOne(window, imgSecond, area, areaSize, cellSize):
    for i in range(0, areaSize):
        for j in range(0, areaSize):
            if i >= areaSize or j >= areaSize or i <= 0 or j <= 0:
                pass
            else:
                imgSecond.undraw()
                status = area[i][j]
                for py in range(cellSize * i, cellSize * i + cellSize):
                    for px in range(cellSize * j, cellSize * j + cellSize):
                        if int(status) == 1:
                            color = gp.color_rgb(0, 255, 0)
                        else:
                            color = gp.color_rgb(255, 0, 0)
                        imgSecond.setPixel(px, py, color)
                imgSecond.draw(window)


def addEventToArea(area, areaSize, modAdded=0.1, modKilledBaseOnAdded=0.8):
    lifeCells = list()
    for i in range(0, areaSize):
        for j in range(0, areaSize):
            if area[i][j] == 1:
                lifeCells.append((i, j))
    addCells = int(lifeCells.__len__() * modAdded)
    killCells = int(addCells * modKilledBaseOnAdded)
    LOG.log("EVENT", "Birth: {0}, Death: {1}".format(addCells, killCells))
    # add close to existing?
    counterAdded = 0
    while counterAdded < addCells:
        randNum = rd.randrange(0, lifeCells.__len__() - 1)
        randNumTwo = rd.randrange(-1, 2)
        randNumThree = rd.randrange(-1, 2)
        lifeCellChosen = lifeCells[randNum]
        pX = lifeCellChosen[0] + randNumTwo
        pY = lifeCellChosen[1] + randNumThree
        if not(pX >= areaSize or pX <= 0 or pY >= areaSize or pY <= 0):
            if (area[pX][pY] == 0):
                area[pX, pY] = 1
                counterAdded += 1

    # kill from OLD life
    counterKilled = 0
    while counterKilled < killCells:
        randNum = rd.randrange(0, lifeCells.__len__() - 1)
        randNumTwo = rd.randrange(-1, 2)
        randNumThree = rd.randrange(-1, 2)
        deathBySnuSnu = lifeCells[randNum]
        pX = deathBySnuSnu[0] + randNumTwo
        pY = deathBySnuSnu[1] + randNumThree
        if not (pX >= areaSize or pX <= 0 or pY >= areaSize or pY <= 0):
            if (area[pX][pY] == 1):
                area[pX, pY] = 0
                counterKilled += 1
    return area


def populateAreaRandomly(area, areaSize, randomSeed=10):
    randomSeed += 5
    for i in range(0, areaSize):
        for j in range(0, areaSize):
            rand = rd.randrange(0, randomSeed)
            if (rand / randomSeed) <= 0.7 * 0.05 * randomSeed:
                area[i, j] = 0
            else:
                area[i, j] = 1


def populateAreaSquares(area, areaSize):
    for i in range(0, areaSize):
        for j in range(0, areaSize):
            if j % 10 > 5 and i % 10 > 5:
                area[i, j] = 1
            else:
                area[i, j] = 0


def evolve(areaCurrent, areaSize, cellSize):
    areaN = np.zeros((areaSize, areaSize))
    for i in range(0, areaSize):
        for j in range(0, areaSize):
            # Edges
            # Count live
            lifeNeighbours = countNeighboors(areaCurrent, i, j, areaSize)
            if (lifeNeighbours == 3 and int(areaCurrent[i, j]) == 0):
                areaN[i, j] = 1
            elif (int(areaCurrent[i][j]) == 1 and (lifeNeighbours == 2 or lifeNeighbours == 3)):
                areaN[i, j] = 1
            else:
                areaN[i, j] = 0
    return areaN


def countNeighboors(area, x, y, areaSize):
    sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Handle edges
            if x + j >= areaSize or y + i >= areaSize or x + j <= 0 or y + i <= 0:
                # killing the ones clsoe to edge
                pass
            else:
                sum += area[x + j, y + i]
    sum -= area[x][y]
    return sum


def populateImageFromArea(img, area, cellSize, areaSize):
    for i in range(0, areaSize):
        for j in range(0, areaSize):
            status = area[i][j]
            for py in range(cellSize * i, cellSize * i + cellSize):
                for px in range(cellSize * j, cellSize * j + cellSize):
                    if int(status) == 1:
                        color = gp.color_rgb(0, 255, 0)
                    else:
                        color = gp.color_rgb(255, 0, 0)
                    img.setPixel(px, py, color)


def checkStatusOfArea(area):
    life = 0
    death = 0
    for i in range(0, AREA_SIZE):
        for j in range(0, AREA_SIZE):
            if int(area[i][j]) == 1:
                life += 1
            else:
                death += 1
    lifePrctg = life / (life + death)
    return lifePrctg, life, death


if __name__ == '__main__':
    main()
