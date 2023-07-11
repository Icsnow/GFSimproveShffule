

import multiprocessing


def c():
    pass


if __name__ == '__main__':
    pool = multiprocessing.Pool(4)
    for i in range(2 ** 16):
        pool.apply_async(c)

    pool.close()
    pool.join()
