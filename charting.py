import multiprocessing as mp
import time

import matplotlib.pyplot as plt
import numpy as np

from hash import check_hash


def charting(setting: dict) -> None:
    """функция для рисования графика
    """
    times = np.empty(shape=0)
    for i in range(1, 8):
        start = time.time()
        with mp.Pool(i) as p:
            item = [(i, setting) for i in range(99999, 10000000)]
            for i, result in enumerate(p.starmap(check_hash, item)):
                if result:
                    end = time.time() - start
                    times = np.append(times, end)
                    p.terminate()
                    break

    plt.bar(range(len(times)), np.round(times, 2).tolist())
    plt.xlabel("Number of pools")
    plt.ylabel("Time, s")
    plt.title("Dependence of time on the number of pool")
    plt.show()
