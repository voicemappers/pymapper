import librosa
import sys

y1, sr1 = librosa.load(sys.argv[1])
mfcc1 = librosa.feature.mfcc(y1, sr1, n_mfcc=100)

print(len(mfcc1.T[0]))
print(len(mfcc1.T))
print(len(mfcc1.T[1]))