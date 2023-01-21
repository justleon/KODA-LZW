import csv
from python_scrypt.data_analysis import analizeDataFromPGM, analizeTextData, printTime, resultAnalize
from python_scrypt import codec
from time import time

def testProcessData(data, name):
    print("\tEntropy = %s" % (data[-1][0]))
    print("\tEntropy^2 = %s" % (data[-1][1]))
    print("\tEntropy^3 = %s" % (data[-1][2]))
    print("\tEntropy^7 = %s" % (data[-1][3]))

    print("\tcode ...")
    start = time()
    code_ret = codec.code(data[0])
    code_time = printTime(start)
    print("\tTime code: " + code_time)

    print("\tdecode ...")
    start = time()
    decode_ret = codec.decode(code_ret)
    decode_time = printTime(start)
    print("\tTime decode: " + decode_time)
    
    assert bytes(decode_ret) == bytes(data[0])
    result = resultAnalize(code_ret, decode_ret)
    print("\tCompression rate: %s of original file" % (result[0]))
    print("\tAverage bit word length: ", result[1])

    return [name, codec.c_max_dict_bit_size, code_time, decode_time,
            data[-1][0], data[-1][1], data[-1][2], data[-1][3], result[1], result[0]]

def main():
    print("Start test LZW codec ...")
    nameDataPGMFiles = ["barbara.pgm", "boat.pgm", "chronometer.pgm", "geometr_05.pgm", "geometr_09.pgm",
                        "geometr_099.pgm", "laplace_10.pgm", "laplace_20.pgm", "laplace_30.pgm", "lena.pgm",
                        "mandril.pgm", "normal_10.pgm", "normal_30.pgm", "normal_50.pgm", "peppers.pgm", "uniform.pgm"]
    nameTextData = ["pan-tadeusz.txt", "random.txt", "text_test.txt", "alice29.txt", "asyoulik.txt",
                    "c-code.txt", "lcet10.txt", "plrabn12.txt"]

    results_file = open('LZW_results.csv', 'a')
    writer = csv.writer(results_file)

    data_header = ["File_name", "Max_bit_word_size", "Compression_time", "Decompression_time",
                    "Entropy", "Entropy_2", "Entropy_3", "Entropy_7", "Avg_bit_word_size", "Compression_ratio"]
    writer.writerow(data_header)

    for max_bit_word_size in [9, 13, 17]:
        codec.c_max_dict_bit_size = max_bit_word_size

        for i in nameDataPGMFiles:
            print("Start %s for max_bit_word_size = %s ..." % (i, max_bit_word_size))
            data = analizeDataFromPGM(i, pathFile="data/", showHist=False, saveHist=True, histogramPath="histograms/")
            data_final = testProcessData(data, i)
            writer.writerow(data_final)
            print("End %s for max_bit_word_size = %s" % (i, max_bit_word_size))

        for i in nameTextData:
            print("Start %s for max_bit_word_size = %s ..." % (i, max_bit_word_size))
            data = analizeTextData(i, pathFile="data/", showHist=False, saveHist=True, histogramPath="histograms/")
            data_final = testProcessData(data, i)
            writer.writerow(data_final)
            print("End %s for max_bit_word_size = %s" % (i, max_bit_word_size))

    results_file.close()
    print("End test LZW codec")


if __name__ == "__main__":
    main()
