from cmu_112_graphics import * 
import random
import copy


class Minesweeper(Mode):
    def appStarted(mode):
        #grid
        mode.margin = mode.width/20
        mode.row = 56
        mode.col = 72
        mode.boxWidth = (mode.width - 2 * mode.margin)/mode.col
        mode.boxHeight = (mode.height - 2 * mode.margin)/mode.row

        #mine
        mode.mine = 600
        mode.mineLocations = []
        assert(mode.mine < mode.row*mode.col)

        #input
        mode.clickedBoxes = []
        mode.gameOver = False
        mode.victory = False
        mode.flagMode = False
        mode.flagLocations = []
     
    def keyPressed(mode,event):
        if event.key == 'f':
            mode.flagMode = not mode.flagMode
    
    def mousePressed(mode,event):
        for row in range(mode.row):
            for col in range(mode.col):
                if mode.mouseInRange(row,col,event.x,event.y): mode.makeMoves(row,col)
    
    def mouseInRange(mode,row,col,x,y):
        return ((mode.margin + mode.boxWidth*col <= x <= mode.margin + mode.boxWidth*(col+1)) and
                (mode.margin + mode.boxHeight*row <= y <= mode.margin + mode.boxHeight*(row+1)))
    
    def restrictMine(mode,row,col):
        if mode.findMine(row,col) > 5: return False
        return True

    def makeMoves(mode,row,col):
        if len(mode.clickedBoxes) == 0:
            while len(mode.mineLocations) < mode.mine:
                newRow = random.randint(0,mode.row-1)
                newCol = random.randint(0,mode.col-1)
                safeRadiusRow = mode.row/8
                safeRadiusCol = mode.col/8
                if (not ((row - safeRadiusRow <= newRow <= row + safeRadiusRow)
                    and (col - safeRadiusCol <= newCol <= col + safeRadiusCol)) 
                    and ((newRow,newCol) not in mode.mineLocations) and mode.restrictMine(row,col)):
                    mode.mineLocations.append((newRow,newCol))
            assert(len(mode.mineLocations) == mode.mine)
            assert(len(set(mode.mineLocations)) == mode.mine)
            mode.numbers = [([0] * mode.col) for row in range(mode.row)]
            mode.getNumbers()
            
        if mode.flagMode:
            if (row,col) not in mode.flagLocations:
                mode.flagLocations.append((row,col))
                mode.mine -= 1
                if mode.mine == 0:
                    for (row,col) in mode.mineLocations:
                        if (row,col) not in mode.flagLocations:
                            return
                    mode.victory = True
            else:
                mode.flagLocations.remove((row,col))
                mode.mine += 1
        elif (row,col) in mode.mineLocations and (row,col) not in mode.flagLocations: 
            mode.clickedBoxes.append((row,col))
            mode.gameOver = True
        elif (row,col) not in mode.flagLocations:
            mode.multiPress(row,col)
    
    def multiPress(mode,row,col):
        if (row,col) in mode.mineLocations:
            return
        elif mode.numbers[row][col] != 0:
            mode.clickedBoxes.append((row,col))
            return
        else:
            mode.clickedBoxes.append((row,col))
            for (i,j) in [(1,0),(-1,0),(0,1),(0,-1)]:
                newRow = row+j
                newCol = col+i
                if 0 <= newRow < mode.row and 0 <= newCol < mode.col and (newRow, newCol) not in mode.clickedBoxes:
                    mode.multiPress(newRow,newCol)
        
    def findMine(mode,row,col):
        total = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i != 0 or j != 0) and (row + i, col + j) in mode.mineLocations:
                    total += 1
        return total
    
    #wrong
    def getNumbers(mode):
        for row in range(mode.row):
            for col in range(mode.col):
                #if (row, col) in mode.mineLocations: continue
                numOfMine = mode.findMine(row,col)
                mode.numbers[row][col] = numOfMine

    def drawNumbers(mode,canvas):
        for (row, col) in mode.clickedBoxes:
            num = str(mode.numbers[row][col])
            if num == "0": num = ""
            canvas.create_text(mode.margin + mode.boxWidth*col + mode.boxWidth//2,
                                mode.margin + mode.boxHeight*row + mode.boxHeight//2, text = num)

    def drawMine(mode,canvas):
        for (row,col) in mode.mineLocations:
            if (row,col) in mode.clickedBoxes:
                canvas.create_oval(mode.margin + mode.boxWidth*col,
                                    mode.margin + mode.boxHeight*row,
                                    mode.margin + mode.boxWidth*(col+1),
                                    mode.margin + mode.boxHeight*(row+1), fill = 'black')
    
    def drawGrid(mode, canvas):
        for row in range(mode.row):
            for col in range(mode.col):
                if (row, col) in mode.clickedBoxes: color = 'light gray'
                else: color = "gray"
                canvas.create_rectangle(mode.margin + mode.boxWidth*col,
                                        mode.margin + mode.boxHeight*row, 
                                        mode.margin + mode.boxWidth*(col+1),
                                        mode.margin + mode.boxHeight*(row+1), fill = color)

    def drawFlagMode(mode,canvas):
        if mode.flagMode:
            canvas.create_text(mode.width//25,mode.height//20, text='flag')

    def drawFlag(mode,canvas):
        for (row,col) in mode.flagLocations:
            canvas.create_oval(mode.margin + mode.boxWidth*col,
                                    mode.margin + mode.boxHeight*row,
                                    mode.margin + mode.boxWidth*(col+1),
                                    mode.margin + mode.boxHeight*(row+1), fill = 'red')
    
    def drawFlagStats(mode,canvas):
        canvas.create_text(24*mode.width//25,mode.height//20,text=mode.mine)

    def drawEnd(mode,canvas):
        if mode.gameOver: output = "GAME OVER"
        elif mode.victory: output = "YOU WIN"
        else: output = ""
        canvas.create_text(mode.width//2,mode.height//2,text=output)

    def redrawAll(mode,canvas):
        mode.drawGrid(canvas)
        mode.drawMine(canvas)
        mode.drawNumbers(canvas)
        mode.drawFlagMode(canvas)
        mode.drawFlag(canvas)
        mode.drawEnd(canvas)
        mode.drawFlagStats(canvas)

class MineSweeperAI(Mode):
    def appStarted(mode):
        #setup Game
        mode.game = Minesweeper()
        mode.game.width = mode.width
        mode.game.height = mode.height
        mode.game.appStarted()
        
        mode.startGame = True

        mode.numbers = []
        


    def keyPressed(mode,event):
        if event.key == "Space":
            mode.appStarted()

    def finalMoves(mode):
        lowestProb = [(-1,-1), 1]
        for (row,col) in mode.game.clickedBoxes:
            openMoves = mode.getAdjacent(row,col)
            bombLeft = mode.numbers[row][col]
            if len(openMoves) == 0: prob = 1
            else: prob = bombLeft/len(openMoves)
            if prob < lowestProb[1]:
                lowestProb = [openMoves, prob]
        print("probabiliy", lowestProb[1])
        return random.choice(lowestProb[0])

    def inRange(mode,row,col):
        return (0 <= row < mode.game.row) and (0 <= col < mode.game.col)
    
    #gets empty spaces
    def getAdjacent(mode,row,col):
        adjacent = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if ((i != 0 or j != 0)
                and (row+i,col+j) not in mode.game.clickedBoxes + mode.game.flagLocations 
                and mode.inRange(row+i,col+j)):
                    adjacent.append((row+i,col+j))
        return adjacent

    def decreaseAdjcent(mode, row, col):
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i != 0 or j != 0) and mode.inRange(row+i,col+j):
                    mode.numbers[row+i][col+j] -= 1

    def mousePressed(mode,event):
        mode.game.mousePressed(event)

    def getFlag(mode,row,col):
        adjacent = mode.getAdjacent(row,col)
        if len(adjacent) == mode.numbers[row][col]:
            for (newRow,newCol) in adjacent:
                mode.decreaseAdjcent(newRow,newCol)
                mode.game.flagLocations.append((newRow,newCol))

                mode.game.mine -= 1
                        
        elif mode.numbers[row][col] == 0:
            for (newRow,newCol) in adjacent:
                mode.game.makeMoves(newRow,newCol)
    
    def looseDecreaseAdjcent(mode,row,col,maxCount, adjToAdj):
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if ((i != 0 or j != 0) and mode.inRange(row+i,col+j) and
                   ((row+i,col+j) not in adjToAdj or adjToAdj[(row+i,col+j)] < maxCount)):
                    mode.numbers[row+i][col+j] -= 1
                    if ((row+i,col+j) not in adjToAdj): adjToAdj[(row+i, col+j)] = 0
                    adjToAdj[(row+i, col+j)] += 1

    def findAdjFlag(mode,row,col):
        total = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i != 0 or j != 0) and (row + i, col + j) in mode.game.flagLocations:
                    total += 1
        return total

    def pigeonHole(mode,pigeon, holes):
        #gives the number of holes that garuntee at least one pigeon
        #gH(1,n) = n
        #gH(2,n) = n - 1
        #gH(3,n) = n - 2
        return holes - pigeon + 1
    
    def sharingBorder(mode, row, col, pigeon, hole, tempBombLocation):
        for i in [-2,-1,0,1,2]:
            for j in [-2,-1,0,1,2]:
                if (i != 0 or j != 0):
                    newRow = row + i
                    newCol = col + j
                    if (mode.inRange(newRow,newCol) and
                       (newRow,newCol) in mode.game.clickedBoxes and 
                        mode.numbers[newRow][newCol] > 0):
                        adj = mode.getAdjacent(newRow,newCol)
                        minRequire = mode.pigeonHole(pigeon, hole)
                        shared = len(set(adj).intersection(set(tempBombLocation)))

                        if shared >= minRequire:
                            mode.numbers[newRow][newCol] -= (shared - minRequire + 1)
                            mode.getFlag(newRow,newCol)
                            mode.numbers[newRow][newCol] += (shared - minRequire + 1)




    
    def looseBombFlag(mode):
        compare = len(mode.game.clickedBoxes + mode.game.flagLocations)
        for (row,col) in mode.game.clickedBoxes:
            if mode.numbers[row][col] > 0:
                tempBombLocation = mode.getAdjacent(row,col)
                origNum = mode.numbers[row][col]
                for (newRow, newCol) in tempBombLocation:
                    mode.game.flagLocations.append((newRow,newCol))
                mode.numbers[row][col] = 0

                mode.sharingBorder(row, col, origNum, len(tempBombLocation), tempBombLocation)

                for (newRow, newCol) in tempBombLocation:
                    mode.game.flagLocations.remove((newRow,newCol))
                mode.numbers[row][col] = origNum
                assert(mode.numbers[row][col] == mode.game.findMine(row,col) - mode.findAdjFlag(row,col))
                #1/0





    def timerFired(mode):
        if not mode.game.gameOver and not mode.game.victory:
            prev = len(mode.game.clickedBoxes + mode.game.flagLocations)
            if len(mode.game.clickedBoxes) == 0:
                (row,col) = (mode.game.row//2,mode.game.col//2)
                mode.game.makeMoves(row,col)
            if mode.startGame:
                mode.numbers = copy.deepcopy(mode.game.numbers)
                mode.startGame = False
            for (row, col) in mode.game.clickedBoxes:
                mode.getFlag(row,col)
            if (set(mode.game.flagLocations) == set(mode.game.mineLocations)):
                mode.game.victory = True
            if prev == len(mode.game.clickedBoxes + mode.game.flagLocations):
                mode.looseBombFlag()
            if prev == len(mode.game.clickedBoxes + mode.game.flagLocations):
                (row,col) = mode.finalMoves()
                print(mode.game.row*mode.game.col- len(mode.game.clickedBoxes) - len(mode.game.flagLocations))
                mode.game.makeMoves(row,col)
        for row in range(mode.game.row):
            for col in range(mode.game.col):
                assert(mode.numbers[row][col] == mode.game.findMine(row,col) - mode.findAdjFlag(row,col))
        


    def redrawAll(mode,canvas):
        mode.game.redrawAll(canvas)
        #mode.drawNumbers(canvas)

class MineSweeper(ModalApp):
    def appStarted(app):
        app.mineSweeper = Minesweeper()
        app.Ai = MineSweeperAI()
        app.setActiveMode(app.Ai) 

MineSweeper(width = 1440, height = 800)
