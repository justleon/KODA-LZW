import matplotlib.pyplot as plt
import numpy as np
import math
from time import time


def printTime(start):
    end = time()
    duration = end - start
    if duration < 60:
        return str(round(duration, 2)) + "s."
    else:
        mins = int(duration / 60)
        secs = round(duration % 60, 2)
        if mins < 60:
            return str(mins) + "m " + str(secs) + "s."
        else:
            hours = int(duration / 3600)
            mins = mins % 60
            return str(hours) + "h " + str(mins) + "m " + str(secs) + "s."


def readFilePGM(filename: str, pathFile: str = ""):
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


def calculateDataCount(data: list, alphabet: list = []):
    countData = {}
    countDataForSecondRank = {}
    countDataForThirdRank = {}
    countDataForSeventhRank = {}

    # Prepare histograms of data for base entropy
    # and data blocks for second and third rank entropy.
    for i in alphabet:
        countData[i] = 0
        countDataForSecondRank[np.uint32(i)] = 0
        countDataForThirdRank[np.uint32(i)] = 0
        countDataForSeventhRank[np.uint32(i)] = 0

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
        block = np.uint32(data[i]) + (np.uint32(data[i + 1] << 8))

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

    for i in range(0, len(data) - 6, 7):
        block = np.uint32(data[i]) + (np.uint32(data[i + 1] << 8)) + (np.uint32(data[i + 2] << 16)) + (
            np.uint32(data[i + 3] << 24)) + (np.uint32(data[i + 4] << 32)) + (np.uint32(data[i + 5] << 40)) + (
                    np.uint32(data[i + 6] << 48))

        if block in countDataForSeventhRank.keys():
            countDataForSeventhRank[block] += 1
        else:
            alphabet.append(block)
            countDataForSeventhRank[block] = 1

    return countData, countDataForSecondRank, countDataForThirdRank, countDataForSeventhRank


def showHistogram(countData: dict, dataName: str = "", showHist: bool = False, saveHist: bool = False,
                  pathSaveFile: str = ""):
    plt.bar(list(countData.keys()), list(countData.values()), width=1)
    plt.title(dataName)
    if saveHist:
        plt.savefig(pathSaveFile + dataName + ".png")
    if showHist:
        plt.show()
    plt.close()


def calculateEntropy(countData: dict, countData_second: dict, countData_third: dict, countData_seven: dict, logBase=2):
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
            p = countData_second[i] / (countAllData / 2)
            entropy_second += p * math.log(p, logBase)

    entropy_third = 0
    for i in countData_third:
        if countData_third[i] > 0:
            p = countData_third[i] / (countAllData / 3)
            entropy_third += p * math.log(p, logBase)

    entropy_seven = 0
    for i in countData_seven:
        if countData_seven[i] > 0:
            p = countData_seven[i] / (countAllData / 3)
            entropy_seven += p * math.log(p, logBase)

    return entropy * (-1), entropy_second * (-1 / 2), entropy_third * (-1 / 3), entropy_seven * (-1 / 7)


def dataAnalize(data: list, alphabet: list = [], dataName: str = "", showHist: bool = False, saveHist: bool = False,
                histogramPath: str = ""):
    countData, countData_second, countData_third, countData_seven = calculateDataCount(data, alphabet)
    showHistogram(countData, dataName=dataName, showHist=showHist, saveHist=saveHist,
                                pathSaveFile=histogramPath)
    entropy, entropy_second, entropy_third, entropy_seven = calculateEntropy(countData, countData_second,
                                                                                           countData_third,
                                                                                           countData_seven)

    return (entropy, entropy_second, entropy_third, entropy_seven)


def analizeDataFromPGM(filename: str, pathFile: str = "", showHist: bool = False, saveHist: bool = False,
                       histogramPath: str = ""):
    header, data = readFilePGM(filename, pathFile=pathFile)
    entropies = dataAnalize(data, list(range(header[2] + 1)), dataName=filename[:-4], showHist=showHist,
                            saveHist=saveHist, histogramPath=histogramPath)
    return (data, list(range(header[2] + 1)), entropies)


def analizeTextData(filename: str, pathFile: str = "", showHist: bool = False, saveHist: bool = False,
                    histogramPath: str = ""):
    with open(pathFile + filename, "rb") as in_file:
        data = in_file.read()
    entropies = dataAnalize(data, list(range(256)), dataName=filename[:-4], showHist=showHist, saveHist=saveHist,
                            histogramPath=histogramPath)
    return (data, list(range(256)), entropies)


def bitLength(n: int):
    if n > 0:
        count = math.ceil(math.log(n, 2))
        if count > 8:
            return count
    return 8


def resultAnalize(encode_data, decode_data):
    list_decode_data = [x for x in decode_data]
    comp_rate = encode_data.__sizeof__() / list_decode_data.__sizeof__()
    avg_bit_word_length = sum([bitLength(x) for x in encode_data]) / list_decode_data.__sizeof__() * 8
    return ["{:.2%}".format(comp_rate), avg_bit_word_length]
