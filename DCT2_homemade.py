import numpy as np
import math

def dct(f):
    """
    Return the Discrete Cosine Transform of arbitrary array f.

    Parameters
    ----------
    f : array of integers
        The input array.

    Returns
    -------
    c : array of floats
        The transformed input array.
    """

    if(len(f.shape) != 1):
       raise Exception('Dimension is different from 1')

    N = f.size
    c = np.zeros(N)
    alpha = np.zeros(N)

    alpha[0] = math.sqrt(1 / N)
    alpha[1:] = math.sqrt(2 / N)

    for k in range(N):
        for i in range(N):
            c[k] += f[i] * math.cos(k * math.pi * ((2 * i + 1) / (2 * N)))
        c[k] = alpha[k] * c[k]

    return c

def idct(c):
    """
    Return the Inverse Discrete Cosine Transform of arbitrary array c.

    Parameters
    ----------
    c : array of floats
        The input array.

    Returns
    -------
    f : array of integers
        The transformed input array.
    """

    if(len(c.shape) != 1):
        raise Exception('Dimension is different from 1')
    
    N = c.size
    f = np.zeros(N)
    alpha = np.zeros(N)

    alpha[0] = math.sqrt(1 / N)
    alpha[1:] = math.sqrt(2 / N)
    
    for j in range(N):
        for k in range(N):
            f[j] += c[k] * alpha[k] * math.cos(k * math.pi * ((2 * j + 1) / (2 * N)))

    return f

def dct2(f):
    """
    Return the Discrete Cosine Transform in 2D of arbitrary matrix f.

    Parameters
    ----------
    f : matrix of integers
        The input matrix.

    Returns
    -------
    c : matrix of floats
        The transformed input matrix.
    """

    if(len(f.shape) != 2):
        raise Exception('Dimension is different from 2')

    N = f.shape[0]
    M = f.shape[1]
    c = np.zeros((N, M))

    # DCT on columns
    for j in range(M):
        c[:, j] = dct(np.squeeze(np.asarray(f))[:, j])

    # DCT on rows
    for i in range(N):
        c[i, :] = dct(np.squeeze(np.asarray(c))[i, :])

    return c

def idct2(c):
    """
    Return the Inverse Discrete Cosine Transform in 2D of arbitrary matrix c.

    Parameters
    ----------
    c : matrix of floats
        The input matrix.

    Returns
    -------
    f : matrix of integers
        The transformed input matrix.
    """

    if(len(c.shape) != 2):
        raise Exception('Dimension is different from 2')

    N = c.shape[0]
    M = c.shape[1]
    f = np.zeros((N, M))

    # IDCT2 on columns
    for j in range(M):
        f[:, j]  = idct(np.squeeze(np.asarray(c))[:, j])

    # IDCT2 on rows
    for i in range(N):
        f[i, :] = idct(np.squeeze(np.asarray(f))[i, :])

    return f