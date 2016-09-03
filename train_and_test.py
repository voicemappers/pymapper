import sys
import train
import dtw_util


class Tester:
    def __init__(self, base_file, threshold_dist):
        self.base_file = base_file
        self.threshold_dist = threshold_dist

    def is_matching(self, test_file):
        return dtw_util.get_distance(self.base_file, test_file) <= self.threshold_dist

    def count_matches(self, files):
        return sum(map(lambda file: self.is_matching(file), files))


def main():
    try:
        n_train = int(sys.argv[1])
        train_files = sys.argv[2:2 + n_train]
        n_pos_index = 2 + n_train
        n_pos_test = int(sys.argv[n_pos_index])
        pos_test_files = sys.argv[n_pos_index + 1: n_pos_index + 1 + n_pos_test]
        n_neg_index = n_pos_index + n_pos_test + 1
        n_neg_test = int(sys.argv[n_neg_index])
        neg_test_files = sys.argv[n_neg_index + 1:n_neg_index + 1 + n_neg_test]
    except IndexError:
        print("ERROR: Incorrect number of arguments", file=sys.stderr)
        print("Usage:",
              "command <number of training files> <training files>",
              "<number of pos test files> <pos files> <number of neg test files> <neg files>", file=sys.stderr)
        return

    print("Training", file=sys.stderr)
    chosen_file, threshold_dist, dist_map = train.train(train_files)
    print("Finished Training", file=sys.stderr)

    tester = Tester(chosen_file, threshold_dist)

    print("Testing Positive Files", file=sys.stderr)
    true_pos = tester.count_matches(pos_test_files)
    print("Testing Negative Files", file=sys.stderr)
    false_pos = tester.count_matches(neg_test_files)
    true_neg = len(neg_test_files) - false_pos
    false_neg = len(pos_test_files) - true_pos

    print("Testing Training Files", file=sys.stderr)
    true_pos_training = tester.count_matches(train_files)

    print("Test Set Results")
    print("True Pos:", true_pos)
    print("False Pos:", false_pos)
    print("True Neg:", true_neg)
    print("False Neg:", false_neg)
    print("Recall:", true_pos / (false_neg + true_pos))
    print("Precision:", true_pos / (false_pos + true_pos))
    print("Accuracy:", (true_pos + true_neg) / (n_neg_test + n_pos_test))
    print("Training Set Results")
    print("Accuracy/Recall:", true_pos_training / n_train)


main()