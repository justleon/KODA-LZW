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
    for i in alphabet:
        countData[i] = 0
    for i in data:
        if i in countData.keys():
            countData[i] += 1
        else:
            print("WARNING: add new value (%s) to alphabet" % (i))
            alphabet.append(i)
            countData[i] = 1
    return countData

def showHistogram(countData:dict, dataName:str="", showHist:bool=False, saveHist:bool=False, pathSaveFile:str=""):
    plt.bar(list(countData.keys()), list(countData.values()), width=1)
    plt.title(dataName)
    if saveHist:
        plt.savefig(pathSaveFile + dataName + ".png")
    if showHist:
        plt.show()
    plt.close()

def calculateEntropy(countData:dict, logBase=2):
    countAllData = 0
    for i in countData:
        countAllData += countData[i]

    entropy = 0
    for i in countData:
        if countData[i] > 0:
            p = countData[i]/countAllData
            entropy += p * math.log(p, logBase)
    return entropy*(-1)