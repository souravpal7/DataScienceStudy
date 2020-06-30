class GeneticAlgoFor8QueenChess:

    def __init__(self,n):
        self.board = self.createBoard(n)
        self.solutions = []
        self.size = n
        self.env = []
        self.goal = None
        self.goalIndex = -1


    def createBoard(self,n):
        board = [[0 for i in range(n)] for j in range(n)]
        return board

    def setBoard(self,board,gen):
        for i in range(self.size):
            board[gen[i]][i] = 1

    def genereteDNA(self):
        #genereates random list of length n
        import random
        
        #Random 1
        DNA = list(range(self.size))
        #random.shuffle(DNA)
        while DNA in self.env:
            random.shuffle(DNA)
        
        #Random 2
        #DNA = [ random.randint(0, self.size-1) for _ in range(self.size) ]
        
        return DNA

    def generateInitialPopulation(self):
        for i in range(100):
            self.env.append(self.genereteDNA())

    def scorePopulation(self,gen):

        hits = 0
        
        #Create nested list representation of a 8*8 blank board - All elements are 0
        board = self.createBoard(self.size)
        
        #Update the nested list representation of a 8*8 blank board - 1 holds the queen positions
        self.setBoard(board,gen)
        
        col = 0
        for dna in gen:
            
            #Horizontal Hit Count on the left side
            try:
                for i in range(col-1,-1,-1):
                    if board[dna][i] == 1:
                        hits+=1
            except IndexError:
                print(gen)
                quit()
            
            #Diagonal Hit Count on the upper left side
            for i,j in zip(range(dna-1,-1,-1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    hits+=1
            
            #Diagonal Hit Count on the lower left side
            for i,j in zip(range(dna+1,self.size,1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    hits+=1
            col+=1

        return hits

    def isGoalGen(self,gen):
        if self.scorePopulation(gen) == 0:
            return True
        return False

    def crossOverGens(self,firstGen,secondGen):
        for i in range(1,len(firstGen)):
            if abs(firstGen[i-1] - firstGen[i])<2:
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]
            if abs(secondGen[i-1] - secondGen[i])<2:
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]


    def MutantGen(self,gen):
        bound = self.size//2
        newGen = []
        
        
        # discarding duplicate occurences of the elements
        for dna in gen:
            if dna not in newGen:
                newGen.append(dna)
        
        # filling the remaining elements with the non occuring numbers
        for i in range(self.size):
            if i not in newGen:
                newGen.append(i)
        
        gen = newGen
        
        # two elements selected randomly will be swapped with each other
        from random import randint as rand
        leftSideIndex = rand(0,bound)
        RightSideIndex = rand(bound+1,self.size-1)
        gen[leftSideIndex],gen[RightSideIndex] = gen[RightSideIndex],gen[leftSideIndex]
        
        return gen


    def crossOverAndMutant(self):
        for i in range(1,len(self.env),2):
            firstGen = self.env[i-1][:]
            secondGen = self.env[i][:]
            self.crossOverGens(firstGen,secondGen)
            firstGen = self.MutantGen(firstGen)
            secondGen = self.MutantGen(secondGen)
            self.env.append(firstGen)
            self.env.append(secondGen)

    def makeSelection(self):
        #index problem
        genUtilities = []
        newEnv = []

        for gen in self.env:
            genUtilities.append(self.scorePopulation(gen))
        if min(genUtilities) == 0:
            self.goalIndex = genUtilities.index(min(genUtilities))
            self.goal = self.env[self.goalIndex]
            return self.env
        minUtil=None
        while len(newEnv) < self.size:
            minUtil = min(genUtilities)
            minIndex = genUtilities.index(minUtil)
            newEnv.append(self.env[minIndex])
            genUtilities.remove(minUtil)
            self.env.remove(self.env[minIndex])
        return newEnv

    def solveGA(self):
        self.generateInitialPopulation()
        
        for gen in self.env:
            if self.isGoalGen(gen):
                return gen
            
        count = 0
        while True:
            self.crossOverAndMutant()
            self.env = self.makeSelection()
            count +=1
            if self.goalIndex >= 0 :
                try:
                    #print(count)
                    return self.goal
                except IndexError:
                    print(self.goalIndex)
            else:
                continue
        
#main function
def main():
    dimension = 8
    chess = GeneticAlgoFor8QueenChess(dimension)
    from time import time
    solution = chess.solveGA()
    print(solution)

main()
