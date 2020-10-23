from Utils import readFile, getPoliceRecord, writeToFile, writeToLogFile


# PoliceTree: This is a Binary Tree of entries of the form <police ID, total fine amount>
class PoliceNode:
    def __init__(self, policeId, fineAmt,bonusThreshold):
        self.policeId = policeId
        self.fineAmt = fineAmt
        self.left = None
        self.right = None
        if bonusThreshold is None:
            self.bonusThreshold = 0.90
        else:
            self.bonusThreshold = bonusThreshold


# This function inserts an entry <policeId, amount> into the police tree ordered by police id.
# If the Police id is already found in the tree, then this function adds up to the existing amount
# to get the total amount collected by him. This function returns the updated tree.
def insertByPoliceId(policeRoot, policeId, amount):
    if policeRoot is None:
        policeRoot = PoliceNode(policeId, amount, None)
    elif policeId == policeRoot.policeId:
        # if the police id is found then we need to add the fine amount
        policeRoot.fineAmt += amount
    elif policeId < policeRoot.policeId:
        policeRoot.left = insertByPoliceId(policeRoot.left, policeId, amount)
    else:
        policeRoot.right = insertByPoliceId(policeRoot.right, policeId, amount)
    return policeRoot


# This function reorders the Binary Tree on the basis of total fine amount, instead of police id.
# This function removes the nodes from the original PoliceTree, and puts it in a new tree ordered by fine amount.
# Note that if the fine amount in node i is equal to the amount in node j, then the node i will be inserted to the
# left of the node j. This function returns the root node of the new tree.
def reorderByFineAmount(policeRoot):
    nodes = []
    newPoliceRoot = None
    nodes = getPoliceNodes(policeRoot, nodes)
    for node in nodes:
        modifiedRoots = changeKey(policeRoot, newPoliceRoot, node.policeId, node.fineAmt)
        policeRoot = modifiedRoots[0]
        newPoliceRoot = modifiedRoots[1]
    return newPoliceRoot


# This function prints the list of police ids which have earned equal to or more than 90% of maximum total fine amount
# collected by an individual. The output is pushed to a file called bonus.txt. The output will be in the format
# -------------- Bonus -------------
# <license no>, no of violations
def printBonusPolicemen(policeRoot):
    if policeRoot is not None:
        maxFineAmount = maximumFine(policeRoot)
        threshold = policeRoot.bonusThreshold * maxFineAmount
        bonusPolicemen = []
        filterPolicemen(policeRoot, threshold, bonusPolicemen)
        lines = []
        for policeman in bonusPolicemen:
            lines.append(str(policeman[0]) + "," + str(policeman[1]))
        writeToFile("-------------- Bonus -------------", "../output/bonus.txt", lines)


# This function is a clean-up function that destroys all the nodes in the police tree.
def destroyPoliceTree(policeRoot):
    if policeRoot is not None:
        writeToLogFile("Deleting Tree")
        destroyTree(policeRoot)
        policeRoot = None
    else:
        writeToLogFile("Empty Tree")
    return policeRoot


# deletes the nodes of the tree recursively
def destroyTree(policeRoot):
    if policeRoot is None:
        return
    # first delete both subtrees
    destroyTree(policeRoot.left)
    destroyTree(policeRoot.right)
    # then delete the node
    writeToLogFile("Deleting node:" + str(policeRoot.policeId))


# This is a debug function is meant for debugging purposes. This function prints the contents of the PoliceTree
# in-order.
def printPoliceTree(policeRoot):
    if policeRoot is not None:
        writeToLogFile("Printing Tree: In-Order Tree:")
        printInOrder(policeRoot)
    else:
        writeToLogFile("Printing Tree: Tree is empty")


# printing the tree in-order
def printInOrder(policeRoot):
    if policeRoot is not None:
        printInOrder(policeRoot.left)
        writeToLogFile(str(policeRoot.policeId) + ':' + str(policeRoot.fineAmt))
        printInOrder(policeRoot.right)


# traverse the original tree and get all the nodes
def getPoliceNodes(policeRoot, nodes):
    if policeRoot is not None:
        getPoliceNodes(policeRoot.left, nodes)
        nodes.append(PoliceNode(policeRoot.policeId, policeRoot.fineAmt, None))
        getPoliceNodes(policeRoot.right, nodes)
    return nodes


# Changes the key of Binary Search Tree
def changeKey(policeRoot, newPoliceRoot, oldKey, newKey):
    # First delete old key value
    policeRoot = deleteNode(policeRoot, oldKey)
    # Then insert new key value
    newPoliceRoot = insertByFine(newPoliceRoot, oldKey, newKey)

    # Return new police root
    return tuple((policeRoot, newPoliceRoot))


# orders the police root by fine amount.
def insertByFine(newPoliceRoot, policeId, amount):
    if newPoliceRoot is None:
        newPoliceRoot = PoliceNode(policeId, amount, None)
    else:
        if amount <= newPoliceRoot.fineAmt:
            newPoliceRoot.left = insertByFine(newPoliceRoot.left, policeId, amount)
        else:
            newPoliceRoot.right = insertByFine(newPoliceRoot.right, policeId, amount)
    return newPoliceRoot


# Returns maximum fine value in the
def maximumFine(policeRoot):
    if policeRoot is not None:
        current = policeRoot
        # loop down to find the rightmost leaf
        while current.right:
            current = current.right
        return current.fineAmt


# Get policemen who have collected 0.90 of max fine.
def filterPolicemen(policeRoot, filterCondition, filteredPolicemen):
    if policeRoot is not None:
        filterPolicemen(policeRoot.left, filterCondition, filteredPolicemen)
        if policeRoot.fineAmt >= filterCondition:
            filteredPolicemen.append(tuple((policeRoot.policeId, policeRoot.fineAmt)))
        filterPolicemen(policeRoot.right, filterCondition, filteredPolicemen)


# Given a binary search tree and a key, this
# function deletes the node matching the key and returns the new root
def deleteNode(policeRoot, key):
    # base case
    if policeRoot is None:
        return policeRoot

    # If the key to be deleted is smaller than
    # the root's key, then it lies in left subtree
    if key < policeRoot.policeId:
        policeRoot.left = deleteNode(policeRoot.left, key)

    # If the key to be deleted is greater than
    # the root's key, then it lies in right subtree
    elif key > policeRoot.policeId:
        policeRoot.right = deleteNode(policeRoot.right, key)

    # if key is same as police root's key, then
    # this is the node to be deleted
    else:

        # node with only one child or no child
        if policeRoot.left is None:
            temp = policeRoot.right
            return temp
        elif policeRoot.right is None:
            temp = policeRoot.left
            return temp

        # node with two children
        temp = minValueNode(policeRoot.right)

        # Copy the in order successor's content
        # to this node
        policeRoot.policeId = temp.policeId

        # Delete the in order successor
        policeRoot.right = deleteNode(policeRoot.right, temp.policeId)
    return policeRoot


# Given a non-empty binary search tree, return
# the node with minimum key value found in that
# This function is used for deleting the tree.
def minValueNode(node):
    current = node
    # loop down to find the leftmost leaf
    while current.left is not None:
        current = current.left
    return current


def processInput():
    lines = readFile("../input/inputPS3.txt")
    root = None
    for line in lines:
        policeRecord = getPoliceRecord(line)
        if policeRecord is not None:
            root = insertByPoliceId(root, policeRecord[0], policeRecord[2])
    return root


# Driver Code
if __name__ == '__main__':
    originalRoot = processInput()
    newRoot = reorderByFineAmount(originalRoot)
    printPoliceTree(newRoot)
    printBonusPolicemen(newRoot)
    newRoot = destroyPoliceTree(newRoot)
    printPoliceTree(newRoot)
