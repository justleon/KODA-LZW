# KODA-LZW
LZW coder/decoder project for Data Compression on WUT

## Kodek LZW
Implementacja kodeka znajduje się w folderze 'codec'.

### Wymagania
- kompilator c++ ze standardem 14
- CMake

### Kompilacja
```console
KODA-LZW$ cd codec
KODA-LZW/codec$ mkdir build
KODA-LZW/codec$ cd build
KODA-LZW/codec/build$ cmake ..
KODA-LZW/codec/build$ make
```

### Pliki wynikowe
Skompilowana biblioteka zostanie umieszczona w folderze 'KODA-LZW/codec/lib'.

## Wrapper kodeka LZW
Wrapper pythonowy kodeka LZW znajduje się w pliku 'KODA-LZW/python_scrypt/codec.py'.

### UWAGA
Wrapper przygotowany jest do wykorzystywania biblioteki nazwanej 'libCodec_lzw.so' znajdującej się w 'codec/lib/' (ścieżka względna, względem folderu uruchomienia skrytpów pythonowych). Jest to nazwa i ścieżka poprawna dla wykonania kompilacji kodeka za pomocą CMake na systemie linux i uruchomienia skryptów pythonowych z poziomu głównego folderu projektu - 'KODA-LZW'.
<br>
Aby wykorzystać wrapper w innym systemie, po pszemieszczeniu (instalacji) biblioteki, lub wywołaniu skryptów z innego folderu należy uaktualnić ścieżkę znajdującą się w 3 linii pliku wrappera ('KODA-LZW/python_scrypt/codec.py').

```console
libc = CDLL("codec/lib/libCodec_lzw.so")
```

## Tester kodeka
Tester wymaga wcześniejszego skompilowania biblioteki c++ kodeka LZW (patrz rozdział 'Kodek LZW').<br>
Dane testowe umieszczone są w folderze 'data'.<br>
Uzyskane histogramy umieszczane są w folderze 'histograms'.<br>
Pozostałe dane umieszczane są w pliku 'LZW_results.csv'.<br>
Funkcje służace do wczytania oraz analizy danych i wyników znajdują się w pliku 'KODA-LZW/python_scrypt/data_analysis.py'.

### Uruchomienie skryptu
```console
KODA-LZW$ python3 test_codec.py
```

### UWAGA
Skrypt należy uruchamiać z poziomu folderu głównego projektu - 'KODA-LZW' (patrz 'UWAGA' w rozdziale 'Wrapper kodeka LZW').
