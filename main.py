import python_src.data_analysis as data_analysis

def dataAnalize(data:list, alphabet:list=[], dataName:str="", showHist:bool=False, saveHist:bool=False, histogramPath:str=""):
    countData = data_analysis.calculateDataCount(data, alphabet)
    data_analysis.showHistogram(countData, dataName=dataName, showHist=showHist, saveHist=saveHist, pathSaveFile=histogramPath)
    print("Entropia '%s' = %s" % (dataName, data_analysis.calculateEntropy(countData)))

def analizeDataFromPGM(filename:str, pathFile:str="", showHist:bool=False, saveHist:bool=False, histogramPath:str=""):
    header, data = data_analysis.readFilePGM(filename, pathFile=pathFile)
    dataAnalize(data, list(range(header[2] + 1)), dataName=filename[:-4], showHist=showHist, saveHist=saveHist, histogramPath=histogramPath)

if __name__ == "__main__":
    nameDataPGMFiles = ["barbara.pgm", "boat.pgm", "chronometer.pgm", "geometr_05.pgm", "geometr_09.pgm", "geometr_099.pgm", "laplace_10.pgm", "laplace_20.pgm", "laplace_30.pgm", "lena.pgm", "mandril.pgm", "normal_10.pgm", "normal_30.pgm", "normal_50.pgm", "peppers.pgm", "uniform.pgm"]
    for i in nameDataPGMFiles:
        analizeDataFromPGM(i, pathFile="data/", showHist=False, saveHist=True, histogramPath="histograms/")