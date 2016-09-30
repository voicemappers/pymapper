import sys
import dtw_util
import statistics
import numpy as np

THRESHOLD_PERCENTILE = 85


# returns distances to other files in order, with distance to self removed
def get_distances(index, dist_map):
    dists = []
    for i in range(len(dist_map)):
        if i != index:
            dists.append(dist_map[min(index, i)][max(index, i)])

    return dists


def get_chosen_training_index(dist_map):
    if len(dist_map) < 2:
        raise Exception("Need at least 2 files to train")

    min_median = statistics.median(get_distances(0, dist_map))
    min_index = 0
    for i in range(1, len(dist_map)):
        median = statistics.median(get_distances(i, dist_map))
        if min_median > median:
            min_median = median
            min_index = i
    return min_index


def get_max_distance(index, dist_map):
    return np.percentile(np.array(get_distances(index, dist_map)), THRESHOLD_PERCENTILE)


def train(files):
    if len(files) == 1:
        return files[0], 0, [[0]]
    elif len(files) == 0:
        raise Exception("No files given to train!")
    dist_map = [[0] * len(files) for _ in range(len(files))]

    print("Calculating distances", file=sys.stderr)
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            dist = dtw_util.get_distance(files[i], files[j])
            dist_map[i][j] = dist
            print("Dist", files[i], files[j], dist, file=sys.stderr)

    # print(dist_map)
    chosen_ind = get_chosen_training_index(dist_map)
    return files[chosen_ind], get_max_distance(chosen_ind, dist_map), dist_map
