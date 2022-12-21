import csv
import python_scrypt.data_analysis as data_analysis
from python_scrypt import codec


def dataAnalize(data: list, alphabet: list = [], dataName: str = "", showHist: bool = False, saveHist: bool = False,
                histogramPath: str = ""):
    countData, countData_second, countData_third, countData_seven = data_analysis.calculateDataCount(data, alphabet)
    data_analysis.showHistogram(countData, dataName=dataName, showHist=showHist, saveHist=saveHist,
                                pathSaveFile=histogramPath)
    entropy, entropy_second, entropy_third, entropy_seven = data_analysis.calculateEntropy(countData, countData_second,
                                                                                           countData_third,
                                                                                           countData_seven)

    return (entropy, entropy_second, entropy_third, entropy_seven)


def analizeDataFromPGM(filename: str, pathFile: str = "", showHist: bool = False, saveHist: bool = False,
                       histogramPath: str = ""):
    header, data = data_analysis.readFilePGM(filename, pathFile=pathFile)
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


def main():
    results_file = open('LZW_results.csv', 'a')
    writer = csv.writer(results_file)

    data = ["File_name", "Max_bit_word_size", "Compression_time", "Decompression_time",
            "Entropy", "Entropy_2", "Entropy_3", "Entropy_7",
            "Avg_bit_word_size", "Compression_ratio"]
    writer.writerow(data)

    # nameDataPGMFiles = ["barbara.pgm", "boat.pgm", "chronometer.pgm", "geometr_05.pgm", "geometr_09.pgm",
    #                     "geometr_099.pgm", "laplace_10.pgm", "laplace_20.pgm", "laplace_30.pgm", "lena.pgm",
    #                     "mandril.pgm", "normal_10.pgm", "normal_30.pgm", "normal_50.pgm", "peppers.pgm", "uniform.pgm"]
    nameDataPGMFiles = []
    for i in nameDataPGMFiles:
        print(i + ": ...")

        data = analizeDataFromPGM(i, pathFile="data/", showHist=False, saveHist=False, histogramPath="histograms/")
        data_final = data_analysis.processFile(data, i)
        writer.writerow(data_final)

        print(i + ": DONE")

    # nameTextData = ["text_test.txt", "pan-tadeusz.txt"]
    nameTextData = ["pan-tadeusz.txt"]
    for i in nameTextData:
        print(i + ": ...")

        data = analizeTextData(i, pathFile="data/", showHist=False, saveHist=False, histogramPath="histograms/")
        data_final = data_analysis.processFile(data, i)
        writer.writerow(data_final)

        print(i + ": DONE")

    print("Tests concluded. CLOSING...")
    results_file.close()


def main_testloop():
    test_max_bit_word_size = [9, 13, 17]
    for i in test_max_bit_word_size:
        print("Current test max bit word size: " + str(i))
        codec.c_max_dict_bit_size = i
        main()


if __name__ == "__main__":
    main_testloop()
    # main()
