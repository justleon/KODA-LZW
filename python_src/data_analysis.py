import matplotlib.pyplot as plt
import numpy as np
import math

def readFilePGM(filename:str, pathFile:str =""):
    with open(pathFile + filename, 'rb') as pgmf:
        lines = pgmf.readlines()

    header = []
    for i in lines:
        if len(header) >= 3:
            break
        if i[0] != ord('#'):
            for j in i.split():
                if len(header) == 0:
                    header.append(j)
                elif len(header) == 1:
                    header.append([int(j)])
                elif len(header) == 2:
                    if len(header[1]) == 1:
                        header[1].append(int(j))
                    else:
                        header.append(int(j))
                else:
                    break

    with open(pathFile + filename, 'rb') as pgmf:
        im = plt.imread(pgmf)

    return header, np.concatenate(im, axis=None)

def calculateDataCount(data:list, alphabet:list=[]):
    countData = {}
    countDataForSecondRank = {}
    countDataForThirdRank = {}

    # Prepare histograms of data for base entropy
    # and data blocks for second and third rank entropy.

    for i in alphabet:
        countData[i] = 0
        countDataForSecondRank[np.uint32(i)] = 0
        countDataForThirdRank[np.uint32(i)] = 0

    # Calculate data counts for entropy

    for i in data:
        if i in countData.keys():
            countData[i] += 1
        else:
            print("WARNING: add new value (%s) to alphabet" % (i))
            alphabet.append(i)
            countData[i] = 1

    # Calculate counts of data blocks of second rank for entropy-2

    for i in range(0, len(data) - 1, 2):
        block = np.uint32(data[i]) + (np.uint32(data[i+1] << 8))

        if block in countDataForSecondRank.keys():
            countDataForSecondRank[block] += 1
        else:
            alphabet.append(block)
            countDataForSecondRank[block] = 1

    # Calculate counts of data blocks of third rank for entropy-3

    for i in range(0, len(data) - 2, 3):
        block = np.uint32(data[i]) + (np.uint32(data[i + 1] << 8)) + (np.uint32(data[i + 2] << 16))

        if block in countDataForThirdRank.keys():
            countDataForThirdRank[block] += 1
        else:
            alphabet.append(block)
            countDataForThirdRank[block] = 1

    return countData, countDataForSecondRank, countDataForThirdRank

def showHistogram(countData:dict, dataName:str="", showHist:bool=False, saveHist:bool=False, pathSaveFile:str=""):
    plt.bar(list(countData.keys()), list(countData.values()), width=1)
    plt.title(dataName)
    if saveHist:
        plt.savefig(pathSaveFile + dataName + ".png")
    if showHist:
        plt.show()
    plt.close()

def calculateEntropy(countData:dict,countData_second:dict,countData_third:dict, logBase=2):
    countAllData = 0
    for i in countData:
        countAllData += countData[i]

    entropy = 0
    for i in countData:
        if countData[i] > 0:
            p = countData[i] / countAllData
            entropy += p * math.log(p, logBase)

    entropy_second = 0
    for i in countData_second:
        if countData_second[i] > 0:
            p = countData_second[i] / (countAllData/2)
            entropy_second += p * math.log(p, logBase)

    entropy_third = 0
    for i in countData_third:
        if countData_third[i] > 0:
            p = countData_third[i] / (countAllData/3)
            entropy_third += p * math.log(p, logBase)

    return entropy*(-1), entropy_second*(-1), entropy_third*(-1)
