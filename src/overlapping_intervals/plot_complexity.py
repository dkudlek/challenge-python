from cmath import log
import time
import random
import sys
import math
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt





if __name__ == "__main__":
    


    n_squared = ([],[])
    two_nlogn = ([],[])

    for x in range(1,100000):
        n_squared[0].append(x)
        n_squared[1].append(x**2)
        two_nlogn[0].append(x)
        two_nlogn[1].append(2. * x * math.log(x))


    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(n_squared[0], n_squared[1], 'r', label='n*2')
    ax.plot(two_nlogn[0], two_nlogn[1], 'b', label='2 n log(n)')

    plt.show()
