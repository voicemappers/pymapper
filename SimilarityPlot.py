import random

import matplotlib.pyplot as plt


def plot(sphinx_dtw, librosa_dtw, labels):
    x = [i for i in range(len(sphinx_dtw)*2)]
    y = []
    for i in range(len(sphinx_dtw)):
        y.append(sphinx_dtw[i])
        y.append(librosa_dtw[i])
    bars = plt.bar(x, y)
    for bar in bars[::2]:
        bar.set_color('g')
    plt.title('Green - sphinx\n Blue - librosa')
    plt.ylabel('Relative distance')
    for xlabel in zip(range(len(sphinx_dtw)), labels):
        plt.text(xlabel[0]*2, -.1, xlabel[1])
    plt.show()

if __name__ == '__main__':
    plot([random.random() for i in range(5)], [random.random() for i in range(5)], ['Aaaaaaaaaa', 'B', 'C', 'D', 'E'])