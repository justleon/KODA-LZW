import python_scrypt.data_analysis as data_analysis
import python_scrypt.codec as codec

def dataAnalize(data:list, alphabet:list=[], dataName:str="", showHist:bool=False, saveHist:bool=False, histogramPath:str=""):
    countData, countData_second, countData_third = data_analysis.calculateDataCount(data, alphabet)
    data_analysis.showHistogram(countData, dataName=dataName, showHist=showHist, saveHist=saveHist, pathSaveFile=histogramPath)
    entropy, entropy_second, entropy_third = data_analysis.calculateEntropy(countData, countData_second, countData_third)
    print("Entropia '%s' = %s" % (dataName, entropy))
    print("Entropia '%s' blokowego drugiego rzędu  = %s" % (dataName, entropy_second))
    print("Entropia '%s' blokowego trzeciego rzędu = %s" % (dataName, entropy_third))
    return (entropy, entropy_second, entropy_third)

def analizeDataFromPGM(filename:str, pathFile:str="", showHist:bool=False, saveHist:bool=False, histogramPath:str=""):
    header, data = data_analysis.readFilePGM(filename, pathFile=pathFile)
    entropies = dataAnalize(data, list(range(header[2] + 1)), dataName=filename[:-4], showHist=showHist, saveHist=saveHist, histogramPath=histogramPath)
    return (data, list(range(header[2] + 1)), entropies)

def analizeTextData(filename:str, pathFile:str="", showHist:bool=False, saveHist:bool=False, histogramPath:str=""):
    with open(pathFile + filename, "rb") as in_file:
        data = in_file.read()
    entropies = dataAnalize(data, list(range(256)), dataName=filename[:-4], showHist=showHist, saveHist=saveHist, histogramPath=histogramPath)
    return (data, list(range(256)), entropies)

if __name__ == "__main__":
    #nameDataPGMFiles = ["barbara.pgm", "boat.pgm", "chronometer.pgm", "geometr_05.pgm", "geometr_09.pgm", "geometr_099.pgm", "laplace_10.pgm", "laplace_20.pgm", "laplace_30.pgm", "lena.pgm", "mandril.pgm", "normal_10.pgm", "normal_30.pgm", "normal_50.pgm", "peppers.pgm", "uniform.pgm"]
    nameDataPGMFiles = []
    for i in nameDataPGMFiles:
        data = analizeDataFromPGM(i, pathFile="data/", showHist=False, saveHist=True, histogramPath="histograms/")
    
    #nameTextData = ["text_test.txt"]
    nameTextData = []
    for i in nameTextData:
        data = analizeTextData(i, pathFile="data/", showHist=True, saveHist=False, histogramPath="histograms/")

    print("-------------------------")
    print("Test code:")
    data = bytes("WYS*WYGWYS*WYSWYSG", 'UTF-8')
    print("Before code:")
    print(data)
    ret = codec.code(data)
    print("After code:")
    print(ret)
    print("-------------------------")
    print("Test decode:")
    data = ret
    print("Before decode:")
    print(data)
    ret = codec.decode(data)
    print("After decode:")
    print(ret)
    print("-------------------------")
