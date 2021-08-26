import random
# for random forest, not for CART or pruning


# ----------- SINGLE DECISION TREE (CART) -------------

def countClass(data):
    counts = {}
    for row in data:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts
    # A dictionary {"YES": int, "NO": int} in this case

def isPure(data):
    uniqueClasses = list(set([row[-1] for row in data]))
    if len(uniqueClasses) == 1:
        return True
    else:
        return False

# Final answer to the classification
def classifyData(data):
    countDict = countClass(data)
    # Take maximum occurrence
    if max(list(countDict.values())) == countDict[list(countDict.keys())[0]]:
        classification = list(countDict.keys())[0]
    else:
        classification = list(countDict.keys())[1]
    return classification

# Find mid-values (potential split values) for each feature
def getPotentialSplits(data):
    rowLen, colLen = len(data), len(data[0])
    potentialSplit = {}
    for col in range(colLen - 1):
        potentialSplit[col] = []
        # Get list of values for each feature
        values = [row[col] for row in data]
        uniqueValues = sorted(list(set(values)))
        # Get mid-values
        for i in range(len(uniqueValues)):
            if i != 0:
                theSplit = (uniqueValues[i - 1] + uniqueValues[i]) / 2
                potentialSplit[col].append(theSplit)
    return potentialSplit
    # A dictionary {col index: [list of mid-values in this col]}

# Split the data according to which row & which mid-value to consider
def splitData(data, splitColumn, splitValue):
    leftNode = []
    rightNode = []
    for row in data:
        if row[splitColumn] <= splitValue:
            leftNode.append(row)
        else:
            rightNode.append(row)
    return leftNode, rightNode
    # 2D-list containing rows whose splitColumnValues satisfy the condition of being <= or > than the splitValue

# Calculate Gini impurity
# Gini impurity = 1 - sum of (probability ** 2)
def giniImpurity(data):
    counts = countClass(data)
    impurity = 1
    for clas in counts:
        probability = counts[clas] / float(len(data))
        impurity -= (probability ** 2)
    return impurity

# Calculate information gain
# Information gain = uncertainty of the starting node - the weighted impurity of 2 child nodes
def infoGain(leftNode, rightNode, currentGini):
    probability = float(len(leftNode)) / (len(leftNode) + len(rightNode))
    infoGain = currentGini - (probability * giniImpurity(leftNode)) - ((1 - probability) * giniImpurity(rightNode))
    return infoGain

# Find the best question to ask according to info gain
def findBestSplit(data, potentialSplit):
    currentGini = giniImpurity(data)
    maxInfoGain = 0
    bestSplitCol = 0
    bestSplitValue = 0
    # Iterate through the keys in the dictionary
    # Try every combination of features & mid-values
    for col in potentialSplit:
        for value in potentialSplit[col]:
            leftNode, rightNode = splitData(data, col, value)
            tryInfoGain = infoGain(leftNode, rightNode, currentGini)
            maxInfoGain = max(maxInfoGain, tryInfoGain)
            if maxInfoGain == tryInfoGain:
                bestSplitCol = col
                bestSplitValue = value
    return bestSplitCol, bestSplitValue

# Decision Tree algorithm
# algoCode = "DT" -> default decision tree algorithm
# algoCode = others -> modified decision tree algorithm for random forest
def DTalgorithm(data, algoCode="DT"):
    # Base case - create leaf nodes
    if isPure(data):
        classification = classifyData(data)
        return classification
    # Recursion - construct the tree
    else:
        if algoCode == "DT":
            potentialSplit = getPotentialSplits(data)
        else:
            potentialSplit = getRandomSubspaceSplits(data)
        bestSplitCol, bestSplitValue = findBestSplit(data, potentialSplit)
        leftNode, rightNode = splitData(data, bestSplitCol, bestSplitValue)
        # If maxDepth is set, one of the nodes can be empty
        if len(leftNode) == 0 or len(rightNode) == 0:
            classification = classifyData(data)
            return classification
        question = str(bestSplitCol) + " <= " + str(bestSplitValue)
        treeModel = {question: []}
        trueBranch = DTalgorithm(leftNode, algoCode)
        falseBranch = DTalgorithm(rightNode, algoCode)
        # If maxDepth is set, one of the nodes can be == to the other (forced classification)
        if falseBranch == trueBranch:
            treeModel = trueBranch
        else:
            treeModel[question].append(trueBranch)
            treeModel[question].append(falseBranch)
    return treeModel

def DTpredictThis(testRow, treeModel):
    question = list(treeModel.keys())[0]
    questionCol, useless, questionValue = question.split()
    # Ask the question
    if testRow[int(questionCol)] <= float(questionValue):
        answer = treeModel[question][0]
    else:
        answer = treeModel[question][1]
    # Base case - if the answer is not another question
    if not isinstance(answer, dict):
        return answer
    # Recursion - go to another question's tree branch
    else:
        return DTpredictThis(testRow, answer)

def DTprediction(testData, treeModel):
    cntCorrect = 0
    for testRow in testData:
        answer = DTpredictThis(testRow, treeModel)
        if answer == testRow[-1]:
            cntCorrect += 1
    return cntCorrect

# Calculate accuracy
# Accuracy = correct predictions / no. of test samples
def getAccuracy(testData, cntCorrect):
    accuracy = float(cntCorrect / len(testData))
    return accuracy

# ----------- PRUNING -------------

left, right = [], []

# Calculate the probability of getting into a node
def probNode(node):
    probLeftNode = (countClass(node)["YES"] / len(node)) ** 2
    probRightNode = (countClass(node)["NO"] / len(node)) ** 2
    return probLeftNode + probRightNode

# Calculate Pruning Score
# used to decide whether to prun the branch or not
def pruningScore(leftNode, rightNode):
    try:
        # Put one more condition to avoid cutting off branch too early
        if (len(leftNode) > (0.25 * len(dataset))) or (len(rightNode) > (0.25 * len(dataset))):
            return True
        else:
            probTrue = len(leftNode) / (len(rightNode) + len(leftNode))
            probFalse = 1 - probTrue
            pruningScore = float("%.3f" % round(probNode(leftNode) * probTrue + probNode(rightNode) * probFalse, 3))
            currentPruning = pruningScore - lastPruning
            return currentPruning
    except ZeroDivisionError:
        # When rightNode or leftNode is None
        return 0
    except KeyError:
        # When rightNode or LeftNode contain 1 variance only
        return 0
    # return int or float type of pruning score

def DTalgorithmPruning(data, cnt, maxDepth=2):
    global left, right, lastPruning
    # Base case - create leaf nodes
    # for pruningScore below 1%, create leaf nodes (cut the branch off)
    if isPure(data) or cnt == maxDepth or cnt != 0 and pruningScore(left, right) < 0.01:
        classification = classifyData(data)
        lastPruning = pruningScore(left, right)
        return classification
    # Recursion - construct the tree
    else:
        cnt += 1
        bestSplitCol, bestSplitValue = findBestSplit(data, getPotentialSplits(data))
        leftNode, rightNode = splitData(data, bestSplitCol, bestSplitValue)
        question = str(bestSplitCol) + " <= " + str(bestSplitValue)
        treeModel = {question: []}
        if len(leftNode) == 0 or len(rightNode) == 0:
            classification = classifyData(data)
            return classification

        left, right = leftNode, rightNode
        lastPruning = pruningScore(left, right)

        trueBranch = DTalgorithmPruning(leftNode, cnt, maxDepth)
        falseBranch = DTalgorithmPruning(rightNode, cnt, maxDepth)

        if trueBranch == falseBranch:
            treeModel = trueBranch
        else:
            treeModel[question].append(trueBranch)
            treeModel[question].append(falseBranch)
    return treeModel

def DTpredictThisPruning(testRow, treeModel):
    question = list(treeModel.keys())[0]
    questionCol, useless, questionValue = question.split()
    # Ask the question
    if testRow[int(questionCol)] <= float(questionValue):
        answer = treeModel[question][0]
    else:
        answer = treeModel[question][1]
    # Base case - if the answer is not another question
    if not isinstance(answer, dict):
        return answer
    # Recursion - go to another question's tree branch
    else:
        return DTpredictThisPruning(testRow, answer)

def DTpredictionPruning(testData, treeModel):
    cntCorrect = 0
    for testRow in testData:
        answer = DTpredictThisPruning(testRow, treeModel)
        if answer == testRow[-1]:
            cntCorrect += 1
    return cntCorrect

# Get subsets of the features
def getRandomSubspaceSplits(data):
    colLen = len(data[0])
    nSubsets = (colLen ** (0.5))
    if isinstance(nSubsets, float):
        nSubsets = int(nSubsets)
    subsetCols = []
    for i in range(nSubsets):
        # Exclude the last "YES"/"NO" column
        randomCol = random.randint(0, colLen - 2)
        subsetCols.append(randomCol)
        # randomCol is a list containing nSubsets randomly picked columns
    potentialSplit = {}
    for col in subsetCols:
        potentialSplit[col] = []
        # Get list of values for each feature
        values = [row[col] for row in data]
        uniqueValues = sorted(list(set(values)))
        # Get mid-values
        for i in range(len(uniqueValues)):
            if i != 0:
                theSplit = (uniqueValues[i - 1] + uniqueValues[i]) / 2
                potentialSplit[col].append(theSplit)
    return potentialSplit
    # A dictionary {col index: [list of mid-values in this col]}

# ----------- MAIN -------------

# Handling of TRAINING DATA
dataset = [line.strip().split(',') for line in open("train.csv")]
del dataset[0]
for row in dataset:
    # Convert all numbers to float
    for col in range(len(dataset[0]) - 1):
        row[col] = float(row[col])
    # If quality > 6 - "YES", otherwise "NO".
    if float(row[-1]) > 6:
        row[-1] = "YES"
    else:
        row[-1] = "NO"

# Handling of TEST SAMPLE
testData = [line.strip().split(',') for line in open("test.csv")]
del testData[0]
for row in testData:
    # Convert all numbers to float
    for col in range(len(testData[0]) - 1):
        row[col] = float(row[col])
    # If quality > 6 - "YES", otherwise "NO".
    if float(row[-1]) > 6:
        row[-1] = "YES"
    else:
        row[-1] = "NO"

print("[Calculating accuracy...]")
myTreeModel = DTalgorithm(dataset)
DTaccuracy = getAccuracy(testData, DTprediction(testData, myTreeModel))
print("Decision tree accuracy:", DTaccuracy)
print("[Please wait...]")
myTreeModelP = DTalgorithmPruning(dataset, 0)
pruningAccuracy = getAccuracy(testData, DTpredictionPruning(testData, myTreeModelP))
print("Pruning accuracy:", pruningAccuracy)

allMethods = {DTaccuracy: "One decision tree", pruningAccuracy: "One decision tree + pruning"}
print("[Finished.]\n")

print("CONCLUSION:")
print("Best approach:", allMethods[max(list(allMethods.keys()))])
print("Accuracy:", max(list(allMethods.keys())))
