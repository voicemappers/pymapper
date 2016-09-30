import os
import random

import dtw
import sys

import subprocess

from SimilarityPlot import plot


def euclidean(x, y):
    sum_e = 0
    for i in range(len(x)):
        sum_e += abs(x[i] - y[i]) ** 2
    return sum_e ** 0.5


def get_dtw(filename_1, filename_2):
    with open(filename_1) as file_1:
        v1 = group_by(list(map(float, file_1.read().split()[1:])))
        normalise(v1)
    with open(filename_2) as file_2:
        v2 = group_by(list(map(float, file_2.read().split()[1:])))
        normalise(v2)

    # debug.
    # print(type(l1), type(l2))
    return dtw.dtw(v1, v2, dist=euclidean)[0]


def normalise(rows):
    num_cols = len(rows[0])
    for col in range(num_cols):
        max_val = max(rows, key=lambda x: x[col])[col]
        min_val = min(rows, key=lambda x: x[col])[col]
        for row in rows:
            row[col] = (row[col] - min_val) / (max_val - min_val)


def generate_matrix(mfcc_file_names):
    dtw_mat = []
    for i in range(len(mfcc_file_names)):
        row = [0 for k in range(len(mfcc_file_names))]
        for j in range(len(mfcc_file_names)):
            if i != j:
                row[j] = get_dtw(mfcc_file_names[i], mfcc_file_names[j])
        dtw_mat.append(row)
    return dtw_mat


def find_max_index(vector):
    max_idx = 0
    max_val = -1
    for i in range(len(vector)):
        if vector[i] > max_val:
            max_idx = i
            max_val = vector[i]
    return max_idx


def group_by(raw_nums):
    frames = []
    for i in range(len(raw_nums) // 13):
        frames.append(raw_nums[i * 13: (i + 1) * 13])
    return frames


def train(mfcc_file_names):
    # Generate a matrix containing MFCC vectors for each file as rows.
    dtw_mat = generate_matrix(mfcc_file_names)
    # Obtain the sum of each row.
    rows_sum = []
    for row in dtw_mat:
        rows_sum.append(sum(row))
    # Return the file path corresponding to maximum of row.
    return mfcc_file_names[find_max_index(rows_sum)]


def min_max_normalize(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    if maximum == 0:
        maximum = 1
    return list(map(lambda x: (x - minimum) / (maximum - minimum) + 0.1, numbers))


def test(file_path, librosa_scores, labels):
    with open('error_log.txt', 'w') as error_file:
        file_path = subprocess.check_output(
            r'java -jar VoiceMapper.jar "' + file_path + '"',
            shell=True, stderr=error_file).strip()
    file_path = file_path.decode('utf-8')
    # debug.
    # print(type(file_path), file_path)
    if not os.path.exists('trained.txt'):
        raise Exception('System not trained')
    dtw_score_list = []
    with open('trained.txt') as trained_files:
        for trained_filename in filter(lambda f: len(f) > 0, trained_files.readlines()):
            dtw_score_list.append(get_dtw(file_path.strip(), eval(trained_filename).strip()))
    print(min_max_normalize(dtw_score_list))
    print(min_max_normalize(dtw_score_list))
    plot(min_max_normalize(dtw_score_list), librosa_scores, labels)


def main_train(sound_file_paths):
    mfcc_vector_files = []
    with open('error_log.txt', 'w') as error_file:
        for filename in sound_file_paths:
            mfcc_vector_files.append(subprocess.check_output(
                r'java -jar VoiceMapper.jar "' + filename + '"',
                shell=True, stderr=error_file).strip())

    if os.path.exists('trained.txt'):
        trained_file = open('trained.txt', 'r')
        file_paths = set(trained_file.readlines())
    else:
        file_paths = set()
    with open('trained.txt', 'w') as trained_file:
        file_paths.add(train(mfcc_vector_files))
        for path in file_paths:
            trained_file.write(str(path.strip()) + '\n')

            # dtw_scores=test(r'C:\Users\gauth_000\Documents\Projects\VoiceMapper\Python\VoiceMapper\temp\sample1.m4a.txt')
            # filenames=map(lambda x:x.split('\\')[-1], file_paths)
