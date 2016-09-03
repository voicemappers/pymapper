import sys
import dtw_util
import statistics
import numpy as np


THRESHOLD_PERCENTILE = 85

# returns distances to other files in no particular order, with distance to self removed
def get_distances(index, dist_map):
    dists = []
    for i in range(len(dist_map)):
        dists.append(dist_map[min(index, i)][max(index, i)])

    dists.remove(0)
    return dists


def get_chosen_training_index(dist_map):
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
    dist_map = [[0] * len(files) for _ in range(len(files))]

    print("Calculating distances", file=sys.stderr)
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            dist = dtw_util.get_distance(files[i], files[j])
            dist_map[i][j] = dist
            print("Dist", files[i], files[j], dist, file=sys.stderr)

    # print(dist_map)
    return files[get_chosen_training_index(dist_map)], get_max_distance(get_chosen_training_index(dist_map), dist_map), dist_map
