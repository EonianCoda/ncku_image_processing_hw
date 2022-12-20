from multiprocessing import Pool

def hello(a, b):
    print("Hello", a, b)

if __name__ == '__main__':
    with Pool(2) as p:
        for i in range(10):
            p.starmap(hello, (i, i + 1))