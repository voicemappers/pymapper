import itertools
import sys
import dtw_util


# def normalise(rows):
#     num_cols = len(rows[0])
#     for col in range(num_cols):
#         max_val = max(rows, key=lambda x: x[col])[col]
#         min_val = min(rows, key=lambda x: x[col])[col]
#         for row in rows:
#             row[col] = (row[col] - min_val) / (max_val - min_val)
#
#
# def euclidean(x, y):
#     sum_e = 0
#     for i in range(len(x)):
#         sum_e += abs(x[i] - y[i])
#     return sum_e ** 0.5
#
#
# def read_file_as_frames(file):
#     with open(file) as f:
#         raw_nums = list(map(float, f.readline().split()))
#         if raw_nums[0] % 13 != 0:
#             print("WARNING: Number of nums in file is not divisible by 13!", file=sys.stderr)
#         raw_nums = raw_nums[1:]  # skip over the first number which is number of vectors
#         frames = []
#         for i in range(len(raw_nums) // 13):
#             frames.append(raw_nums[i * 13: (i + 1) * 13])
#     return frames
#
#
# def get_cost(file1, file2):
#
#     f1_rows = read_file_as_frames(file1)
#     f2_rows = read_file_as_frames(file2)
#
#     normalise(f1_rows)
#     normalise(f2_rows)
#
#     # if you want to inspect the waves themselves
#     # print("set 1")
#     # for row in f1_rows:
#     #     print(",".join(map(str, row)))
#     # print("set 2")
#     # for row in f2_rows:
#     #     print(",".join(map(str, row)))
#
#     f1_vectors = np.array(f1_rows)
#     f2_vectors = np.array(f2_rows)
#     distance, cost, acc, path = dtw(f1_vectors, f2_vectors, dist=lambda a, b: euclidean(a, b))
#     return distance


def main():
    files = sys.argv[1:]
    for file1, file2 in itertools.combinations(files, 2):
        print(file1, file2, dtw_util.get_distance(file1, file2))


main()


# with open(input()) as f:
#     x_nums = list(map(float, f.readline().split()))
#
# x_co = []
# for i in range(len(x_nums) // 13):
#     x_co.append(tuple(x_nums[13 * i:13 * (i + 1)] + [i]))
# x = np.array(x_co)
#
# with open(input()) as f:
#     y_nums = list(map(float, f.readline().split()))
#
# y_co = []
# for i in range(len(y_nums) // 13):
#     y_co.append(tuple(y_nums[13 * i:13 * (i + 1)] + [i]))
# y = np.array(y_co)
#
# distance, path = fastdtw(x, y, dist=lambda a, b: euclidean(a, b))
# print(distance)
