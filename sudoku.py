import copy
class Solution(object):

    """
    Calculates the indicies of the indexes of the 3x3 that we want.
    """

    def get3x3Ind(self, board, row, col):
        rInd, colInd = 0, 0
        if (row >= 3 and row <= 5):
            rInd = 3
        elif (row >= 6 and row <= 8):
            rInd = 6

        if (col >= 3 and col <= 5):
            colInd = 3
        elif(col >= 6 and col <= 8):
            colInd = 6

        return rInd, colInd

    """
    Gets the values of 3x3 matricies that we know
    """

    def get3x3vals(self, board, row, col):
        theSquare = []
        rInd, colInd = self.get3x3Ind(board, row, col)    # Starting index for the row to iter through

        #Get square values
        for i in range(3):
            for j in range(3):
                if (board[rInd + i][colInd + j] != '.'):
                    theSquare.append(int(board[rInd + i][colInd + j]))
        return theSquare

    """
    Returns true if game is over
    """

    def gameOver(self, board):
        num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == '.':
                    return False

        return True

    """
    Gets the unknown neighbors of a singular node.
    input = 0,2
    rv = [(0,3), (0,4), (0, 6)...]
    """

    def getUnknownNeighbors(self, board, row, col):
        rIndex, cIndex = self.get3x3Ind(board, row, col)
        unknownNeighbors, helper = [], []
        unknownNeighbors.append([(row, x) for x in range(9) if board[row][x] == '.'])  # rows
        unknownNeighbors.append([(x, col) for x in range(9) if board[x][col] == '.']) # cols

        #Get square values
        for i in range(3):
            for j in range(3):
                if (board[rIndex + i][cIndex + j] == '.'):
                    helper.append((rIndex + i, cIndex + j))

        unknownNeighbors.append(helper)

        return unknownNeighbors

    """
    rv = {(0, 2) : [(0, 3),...], (0,3) : [(0,3) : [0,2,...]]}
    """
    def allUnknownNeighbors(self, board, keys):
        unknownNeighbors = {}
        for key in keys:
            unknownNeighbors[key] = self.getUnknownNeighbors(board, key[0], key[1])
        return unknownNeighbors

    """
    What values between 1-9 is missing in all 3 of the sections?
    """
    def possibleVals(self, missingKeys):
        vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        theKeys = missingKeys.keys()
        pvals = {}

        for key in theKeys:
            missingVals = []
            theRow = missingKeys[key][0]
            theCols = missingKeys[key][1]
            the3x3 = missingKeys[key][2]

            for num in vals:

                if not (num in theRow or num in theCols or num in the3x3):
                    missingVals.append(num)

            pvals[key] = missingVals

        return pvals

    """
    output:
        dict missingKeys = (i, j) : [[values in each row], [values in each column],               [values in each 3x3 square]]


    """
    def findKnownValues(self, board, knownValues={}, missingKeys = []):
        missingKeys, knownValues = [], {}
        for row in range(len(board)):
            for col in range(len(board)):
                if (board[row][col] == '.'):

                    missingKeys.append((row, col))

                    valuePairs = [] # vp[0] = row, vp[1] = col, vp[2] = 3x3 square
                    valuePairs.append([int(board[row][x]) for x in range(9) if board[row][x] != '.'])  # rows
                    valuePairs.append([int(board[x][col]) for x in range(9) if board[x][col] != '.']) # cols
                    valuePairs.append(self.get3x3vals(board, row, col)) # 3x3

                    knownValues[(row, col)] = valuePairs
        return knownValues, missingKeys

    """
    Updates pvals, missingKeys, board, and unknownNeighbors
    """
    def updateBoard(self, board, pvals, missingKeys):
        completed = True    # Stays true if we iterate through all keys, and none of them one possible value
        for keys in pvals.keys():
            if (len(pvals[keys]) == 1):
                completed = False
                board[keys[0]][keys[1]] = str(pvals[keys][0])
                print("(" + str(keys[0]) + ',' + str(keys[1]) + ') = ' + str(pvals[keys]))

        knownValues, missingKeys = self.findKnownValues(board)
        unknownNeighbors = self.allUnknownNeighbors(board, missingKeys)
        pvals = self.possibleVals(knownValues)

        if (not completed):
            if (not self.gameOver(board)):
                return self.updateBoard(board, pvals, missingKeys)

        return board, pvals, missingKeys, unknownNeighbors

    """
    Bruce force algo

    We might need to keep a history, and if it doesn't work out take the other route:
    actually, i am thinking we try an index, and see which one results in the minimum missing keys.
    Whichever one has a less amount, we take that board and continue on.
    input:
        board board
        Dict pvals

    output:
        winning board
    """
    def bruceAlgo(self, board, pvals):
        #Find the key that has the smallest amount pvals size, limits amount of iterations
        min = 100
        missingKeys = pvals.keys()
        thePoint = None

        for key in missingKeys:
            if (min == 2):
                break

            elif (len(pvals[key]) < min):
                min = len(pvals[key])
                thePoint = key

        possibleVals = pvals[thePoint]
        test_boards = []    # [(missing_elems, board)]
        for val in possibleVals:
            #Copying the init board to a new board so that we can have some history to revert to for each time step
            theBoard = copy.deepcopy(board)
            theBoard[thePoint[0]][thePoint[1]] = val

            print(thePoint, val)
            #Take a step on the board.
            knownValues, missingKeys1 = self.findKnownValues(board)
            pvalsTest = self.possibleVals(knownValues)
            theBoard, test_pvals1, missingKeys1, _ = self.updateBoard(theBoard, pvalsTest, missingKeys1)

            #If we won, return the board, else append it to the test_boards alongside its amount of missing values left.
            if (self.gameOver(theBoard)):
                print('winnder!\n\n')
                return theBoard

            test_boards.append((len(missingKeys1), theBoard))

            print(len(missingKeys1), 'boards = ', theBoard, 'test_boards = ', test_boards)

        # print("\n the boards possibleVals = ", possibleVals, "\n", test_boards)
        while True:

            if (len(test_boards) == 1):
                return test_boards[0]

            min = 100
            theTestBoard = None
            for i in range(len(test_boards)):
                if test_boards[i][0] < min:
                    min = test_boards[i][0]
                    theTestBoard = test_boards[i][1]

            if (theTestBoard is None):
                return board

            knownValues2, missingKeys2 = self.findKnownValues(theTestBoard)
            pvalsTest2 = self.possibleVals(knownValues2)

            print("\n the boards; pvalsTest2 = ", pvalsTest2, "\n", test_boards)

            winner = self.bruceAlgo(theTestBoard, pvalsTest2)

            print('winner = ', winner)
            kv, _ = self.findKnownValues(winner)
            winpv = self.possibleVals(kv)

            print(winpv, len(winpv))
            if (self.gameOver(winner)):
                return winner
            elif (len(winpv) == 0):
                return winner
            else:
                for x in test_boards:
                    if x == winner:
                        test_boards.pop(x)
                        break

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: None Do not return anything, modify board in-place instead.
        """
        #Checking the restrictions
        if (len(board) != 9):
            return -1

        for i in range(len(board)):
            if (len(board[i]) != 9):
                return -1

        knownValues, missingKeys = self.findKnownValues(board)   # dict missingKeys = (i, j) : [[2,4,..], [3,5,..],[1,2,..]]
        pVals = self.possibleVals(knownValues) # dict pvals = (i, j) : [[1, 2..,], [4,5,..], [2,3..]]
        unknownNeighbors = self.allUnknownNeighbors(board, missingKeys)

        #updates board based on the Pvals that have a single item in their list
        board, pVals, missingKeys, unknownNeighbors = self.updateBoard(board, pVals, missingKeys)
        if (self.gameOver(board)):
            return board

        # if it couldn't be completed on fist pass through, we taking it to the brute force
        return self.bruceAlgo(board, pVals)

    def test(self):
        output = self.solveSudoku(
        [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]
        ]

        )

        solution = [["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"]]

        if output == solution:
            print('\n Correct!')
        else:
            print('\n Wrong!')

        output2 = self.solveSudoku(
        [[".", ".", "9", "7", "4", "8", ".", ".", "."],
        ["7", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", "2", ".", "1", ".", "9", ".", ".", "."],
        [".", ".", "7", ".", ".", ".", "2", "4", "."],
        [".", "6", "4", ".", "1", ".", "5", "9", "."],
        [".", "9", "8", ".", ".", ".", "3", ".", "."],
        [".", ".", ".", "8", ".", "3", ".", "2", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "6"],
        [".", ".", ".", "2", "7", "5", "9", ".", "."]]
        )

        output3 = self.solveSudoku(
        [[".",".",".","2",".",".",".","6","3"],
        ["3",".",".",".",".","5","4",".","1"],
        [".",".","1",".",".","3","9","8","."],
        [".",".",".",".",".",".",".","9","."],
        [".",".",".","5","3","8",".",".","."],
        [".","3",".",".",".",".",".",".","."],
        [".","2","6","3",".",".","5",".","."],
        ["5",".","3","7",".",".",".",".","8"],
        ["4","7",".",".",".","1",".",".","."]]
        )

        print(output2)
        print(output3)
val = Solution()
val.test()
