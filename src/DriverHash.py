from Utils import writeToLogFile, writeToFile, readFile, getPoliceRecord


# A separately chained hash table indexed by license numbers where each entry is of the form < license number,
# number of violations>. A simple hash function h(x) = x mod M, where M is the size of hash table can be used for this.
class DriverHash:
    # constructor to pass the bucket size , hashSize , load factor and violation threshold
    def __init__(self, bucketSize, hashSize, loadFactor, violationThreshold):

        # Minimum bucket size is 5
        if bucketSize < 5:
            self.bucketSize = 5
        else:
            self.bucketSize = bucketSize
        # Minimum hash size is 10
        if hashSize < 10:
            self.hashSize = 10
        else:
            self.hashSize = hashSize
        # load factor must be at least 0.7 and less than 1.0
        if loadFactor < 0.7 or loadFactor >= 1.0:
            self.loadFactor = 0.7
        else:
            self.loadFactor = loadFactor
        # Minimum violation threshold is 1 and default is 3
        if violationThreshold < 3:
            self.violationThreshold = 3
        else:
            self.violationThreshold = violationThreshold

        # This is the hash table which keeps the key value pairs
        self.hashMap = None
        # Tracking the current size of hash table
        self.currentSize = 0

    # This function creates an empty hash table that points to null.
    def initializeHash(self):
        writeToLogFile("Initialized hash with bucket size ="
                       + str(self.bucketSize) +
                       " , Hash Size =" + str(self.hashSize) +
                       " , Load factor=" + str(self.loadFactor) +
                       " , Violation threshold=" + str(self.violationThreshold))
        self.hashMap = [[] for i in range(self.bucketSize)]

    # This function hashes the key and provides the bucket in which key needs to be inserted.
    def hashFunction(self, k):
        try:
            return k % self.bucketSize
        except ValueError:
            print("Invalid license number:" + str(k) + " expected is a number")

    # This is a debug function to print the hash map contents.
    def print(self):
        print(self.hashMap)

    # Calculates the load factor = current size of hash / max hash size
    def currentLoadFactor(self):
        return self.currentSize / self.hashSize

    # This function rehashes all the keys when the load factor is crossed.
    # doubles the size of buckets and max allowed key,value pair in hash table
    def rehash(self, element):
        oldBucketSize = self.bucketSize
        # reset the current hash size , before reinserting
        self.currentSize = 0
        # doubles the bucket size and to tal hash size.
        self.bucketSize *= 2
        self.hashSize *= 2
        writeToLogFile("New Hash Size:" + str(self.hashSize) + " , bucketSize:" + str(self.bucketSize))

        # initialize the temporary hash table with new bucket size.
        newHashMap = [[] for i in range(self.bucketSize)]

        # insert the existing keys with new hash
        for j in range(oldBucketSize):
            bucket = self.hashMap[j]
            key_exists = False
            for i, kv in enumerate(bucket):
                k, v = kv
                newHashMap = self.rehashInsert(k, v, newHashMap)
        self.rehashInsert(element, 1, newHashMap)
        self.hashMap = newHashMap

    # inserts the existing keys after rehashing.
    def rehashInsert(self, key, value, newHashMap):
        hash_key = self.hashFunction(key)
        key_exists = False
        bucket = newHashMap[hash_key]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                key_exists = True
                break
        if key_exists:
            bucket[i] = (key, bucket[i][1] + 1)
        else:
            self.currentSize += 1
            bucket.append((key, value))
        return newHashMap


# This function inserts the licence number lic to the hash table. If a driver’s license number is already present,
# only the number of violations need to be updated else a new entry has to be created.
def insertHash(driverHash, lic):
    writeToLogFile("Inserting element:" + str(lic))
    # check if load factor is crossed.
    if driverHash.currentLoadFactor() <= driverHash.loadFactor:
        hash_key = lic % driverHash.bucketSize
        key_exists = False
        bucket = driverHash.hashMap[hash_key]
        for i, kv in enumerate(bucket):
            k, v = kv
            if lic == k:
                key_exists = True
                break
        if key_exists:
            # if the license is found then we need to increment the violation
            bucket[i] = (lic, bucket[i][1] + 1)
        else:
            # first violation for this license number
            driverHash.currentSize += 1
            bucket.append((lic, 1))
    else:
        writeToLogFile("Hash table has crossed load factor , rehashing")
        driverHash.rehash(lic)
    writeToLogFile("Current hash size:" + str(driverHash.currentSize))
    writeToLogFile("Current load factor:" + str(driverHash.currentLoadFactor()))


# This function prints the serious violators by looking through all hash table entries and printing the license numbers
# of the drivers who have more than 3 violations onto the file violators.txt. The output should be in the format
def printViolators(driverHash):
    violators = []
    for j in range(driverHash.bucketSize):
        bucket = driverHash.hashMap[j]
        for i, kv in enumerate(bucket):
            k, v = kv
            if v > driverHash.violationThreshold:
                violators.append(str(k) + ", " + str(v))
    if len(violators) != 0:
        writeToFile("--------------Violators-------------", "../output/violators.txt", violators)
    else:
        writeToFile("No violators found", "../output/violators.txt", violators)


# This function destroys all the entries inside the hash table. This is a clean-up code.
def destroyHash(driverHash):
    # clear the hash map
    driverHash.hashMap.clear()
    # reset the current size to 0
    driverHash.currentSize = 0


# reads the input file and processes them i.e; inserts to hash map
def processInput(hashMap):
    lines = readFile("../input/inputPS3.txt")
    policeRoot = None
    for line in lines:
        policeRecord = getPoliceRecord(line)
        if policeRecord is not None:
            insertHash(hashMap, policeRecord[1])


if __name__ == '__main__':
    driverHashMap = DriverHash(5, 10, 0.7, 3)
    driverHashMap.initializeHash()
    processInput(driverHashMap)
    printViolators(driverHashMap)
    writeToLogFile("Total elements in hash table:" + str(driverHashMap.currentSize))
    destroyHash(driverHashMap)
    writeToLogFile("Total elements in hash table:" + str(driverHashMap.currentSize))
    driverHashMap.print()
