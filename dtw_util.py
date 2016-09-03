# taken from https://github.com/pierre-rouanet/dtw/blob/master/MFCC%20%2B%20DTW.ipynb

import librosa
from dtw import dtw


def euclidean(x, y):
    sum_e = 0
    for i in range(len(x)):
        sum_e += (x[i] - y[i])**2
    return sum_e ** 0.5


def get_distance(file1, file2):
    y1, sr1 = librosa.load(file1)
    y2, sr2 = librosa.load(file2)

    mfcc1 = librosa.feature.mfcc(y1, sr1, n_mfcc=39)

    mfcc2 = librosa.feature.mfcc(y2, sr2, n_mfcc=39)

    dist, cost, acc, path = dtw(mfcc1.T, mfcc2.T, dist=euclidean)
    return dist
