import json
import os
import pickle
import dtw_util
import subprocess

from VoiceCommandConfigUI import main_config_ui
from sound_recorder import record_audio


def get_label(ip_file, label_dict):
    dist_dict = {key: dtw_util.get_distance(ip_file, value) for key, value in label_dict.items()}
    min_label = min(dist_dict, key=lambda x: dist_dict[x])
    return min_label


def read_config():
    if os.path.exists('trained_ui.pkl'):
        with open('trained_ui.pkl', 'rb') as trained_file:
            centroids = pickle.load(trained_file)
        if os.path.exists('train_voice_cmd.json'):
            with open('train_voice_cmd.json', 'r') as config_file:
                centroids = json.load(config_file)
                # Safety check.
                # for k, v in centroids.items():
                #     if len(v) != 2:
                #         print('no commands found')
                #         main_config_ui()
                return centroids
        else:
            with open('train_voice_cmd.json', 'w') as config_file:
                config_dict = {}
                for label, centroid in centroids.items():
                    config_dict[label] = [centroid]
                config_file.write(json.dumps(config_dict))
    else:
        print('trained_ui.pkl file does not exist')
        exit(1)


def read_pkl():
    if os.path.exists('trained_ui.pkl'):
        with open('trained_ui.pkl', 'rb') as trained_file:
            return pickle.load(trained_file)
    else:
        print('trained_ui.pkl file does not exist')
        exit(1)


def run_command(label):
    config_dict = read_config()
    try:
        command = config_dict[label][1]
        print('command:\t', command)
        subprocess.call(command, shell=True)
    except (IndexError, TypeError):
        print('command not found for ', label)
        main_config_ui()
        subprocess.call(config_dict[label][1], shell=True)


if __name__ == '__main__':
    record_audio()
    ip_file = 'sample.wav'
    label_dict = read_pkl()
    min_label = get_label(ip_file, label_dict)
    run_command(min_label)
    pass
