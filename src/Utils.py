# This class contains utility functions.

import os


# Reads the input file content
def readFile(fileName):
    lines = []
    try:
        file = open(filePath(fileName))
        for line in file:
            lines.append(line)
    except IOError:
        print("File not present or unable to read from file", fileName)
    return lines


# Writes the content to output file
def writeToFile(header, fileName, lines):
    file = open(filePath(fileName), "w")
    print(header)
    file.write(header + "\n")
    for line in lines:
        print(line)
        file.write(line + "\n")
    file.close()


# Writes the logs to log file
def writeToLogFile(line):
    fileName = "../log/logs.txt"
    file = open(filePath(fileName), "a")
    print(line)
    file.write(line + "\n")
    file.close()


# Parses the input record and tokenise in to tuples containing police id , license number and fine amount.
def getPoliceRecord(line):
    if line is not None:
        tokens = line.split('/')
        if len(tokens) != 3:
            print("invalid input in file:")
            print(tokens)
        else:
            try:
                policeRecord = tuple((int(tokens[0].strip()), int(tokens[1].strip()), float(tokens[2].strip())))
            except ValueError:
                print("Invalid input : " + str(tokens[0]) + " and " + tokens[1] + " , expected input is numbers")
            return policeRecord


def filePath(fileName):
    dirName = os.path.dirname(__file__)
    fileName = os.path.join(dirName, fileName)
    return fileName
