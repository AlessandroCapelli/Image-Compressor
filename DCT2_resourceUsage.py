import numpy as np
import matplotlib.pyplot as plt
import datetime
import scipy.fft as DCT2_library
import DCT2_homemade

def main():
    # DCT1 on the test array
    # f = np.array([231, 32, 233, 161, 24, 71, 140, 245])
    # c = DCT2_homemade.dct(f)
    # print(c)
    # f = DCT2_homemade.idct(c)
    # print(f)

    # DCT2 on the test matrix
    # f = np.matrix('231 32 233 161 24 71 140 245; 247 40 248 245 124 204 36 107; 234 202 245 167 9 217 239 173; 193 190 100 167 43 180 8 70; 11 24 210 177 81 243 8 112; 97 195 203 47 125 114 165 181; 193 70 174 167 41 30 127 245; 87 149 57 192 65 129 178 228')
    # c = DCT2_homemade.dct2(f)
    # print(c)
    # f = DCT2_homemade.idct2(c)
    # print(f)
    # c = DCT2_library.dctn(f, 2, norm='ortho')
    # print(c)
    # f = DCT2_library.idctn(c, 2, norm='ortho')
    # print(f)

    max_value = 255
    times_DCT2_homemade = []
    times_DCT2_library = []

    n_min = 50
    n_max = 500
    steps = 50
    for n in range(n_min, (n_max+1), steps):
        f = np.matrix(np.random.randint(max_value, size=(n, n))).astype(float)

        begin_time = datetime.datetime.now()
        DCT2_homemade.dct2(f)
        time = datetime.datetime.now() - begin_time
        times_DCT2_homemade.append(time.seconds*1000 + time.microseconds/1000)
        print("Execution time of DCT2_homemade (n={}): {}".format(n, time))

        begin_time = datetime.datetime.now()
        DCT2_library.dctn(f, 2, norm='ortho')
        time = datetime.datetime.now() - begin_time
        times_DCT2_library.append(time.seconds*1000 + time.microseconds/1000)
        print("Execution time of DCT2_library (n={}): {}".format(n, time))

    palette = plt.get_cmap('Set1')
    plt.xlabel('N')
    plt.ylabel('Time (milliseconds in log scale)')
    plt.yscale('log')
    plt.grid(True, alpha=0.2)
    plt.plot(range(n_min, (n_max+1), steps), times_DCT2_homemade, color=palette(1), linewidth=2)
    plt.plot(range(n_min, (n_max+1), steps), times_DCT2_library, color=palette(4), linewidth=2)
    plt.legend(['DCT2_homemade', 'DCT2_library'],loc=2, ncol=2)
    plt.show()

if __name__ == "__main__":
    main()
