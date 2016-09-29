#!/usr/bin/python

import os
import pickle
from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askopenfilename

import TrainSphinxData
import train
import dtw_util

PKL_FILE = "trained_ui.pkl"

category_dict_rosa = {}
category_dict_sphinx = {}

name = []

data_cv = []
data_cboxes = []

test_label = []
global_test_input = []

window = Tk()
window.title("Voice Mapper")

label1 = Label(window, text="Training Set")
label1.grid(row=0, column=1, pady=10)
#
# label2 = Label(window, text="Data Set")
# # label2.grid(row=0, column=3, pady=10)
#
frame1 = Frame(window, width=180, height=340, bg='white', bd=3, relief=RIDGE)
frame1.grid(row=1, column=1, padx=35, pady=20)
frame1.pack_propagate(False)


#
# frame2 = Frame(window, width=180, height=340, bg='white', bd=3, relief=RIDGE)
# frame2.grid(row=1, column=3, padx=35, pady=20)

# label3 = Label(window, text="Testing Set")
# label3.grid(row=0, column=2, pady=10)
#
# frame3 = Frame(window, width=180, height=340, bg='white', bd=3, relief=RIDGE)
# frame3.grid(row=1, column=2, padx=35, pady=20)
# frame3.pack_propagate(False)


def read_trained_pickle():
    # trained_files is label filename pairs
    if not os.path.isfile(PKL_FILE):
        return {}
    with open(PKL_FILE, "rb") as f:
        return pickle.load(f)


def write_trained_pickle(trained_dict):
    # trained_files is label filename pairs
    with open(PKL_FILE, "wb") as f:
        pickle.dump(trained_dict, f)


def testFileDialog():
    n = askopenfilename(parent=window, filetypes=[('audio files', '*.mp3'),
                                                  ('audio files', '*.m4a'),
                                                  ('audio files', '*.wav')])
    if n == "":
        return
    global global_test_input
    global_test_input = [n]
    bar_graph()


def fileDialog():
    '''
        Opens MP3, M4A and WAV files
    '''

    n = list(askopenfilename(multiple=True, parent=window, filetypes=[('audio files', '*.mp3'),
                                                                      ('audio files', '*.m4a'),
                                                                      ('audio files', '*.wav')]))
    if len(n) == 0:
        return
    global name
    name = n
    train_list()


def selected():
    selected_list = []
    name_len = len(name)

    return list(range(name_len))


def init_trained_display(trained_dict):
    for key in trained_dict:
        train_label = Label(frame1, text=key)
        train_label.pack(padx=10, pady=10)


def train_list():
    selected_to_train = []
    selected_to_train_num = selected()

    for i in selected_to_train_num:
        selected_to_train.append(name[i])

    s_len = len(selected_to_train)

    if not (s_len == 0):

        category_window = Toplevel(master=window)
        category_window.title("Create Category")
        category_window.resizable(width=False, height=False)

        category_label = Label(category_window, text="Enter Category Name : ")
        category_label.grid(row=0, column=0, padx=10, pady=10)

        category_entry = Entry(category_window)
        category_entry.grid(row=0, column=1, padx=10, pady=10)

        def update_train_list():

            category_entry_value = category_entry.get()
            # train and keep a single file representing the centroid
            category_dict_rosa[category_entry_value] = train.train(selected_to_train)[0]
            # GAUTHAM: gautrain.train(selected_to_train)
            TrainSphinxData.main_train(selected_to_train)
            write_trained_pickle(category_dict_rosa)
            train_label = Label(frame1, text=category_entry_value)
            train_label.pack(padx=10, pady=10)
            category_window.destroy()

            print("\nUpdated Category List : \n\n")
            print(category_dict_rosa)

        category_ok_button = Button(category_window, text='OK', command=update_train_list)
        category_ok_button.grid(row=1, column=1, padx=10, pady=10)

    else:
        tkinter.messagebox.showerror("Error", "Please select the files to train or browse for files.")


def quick_test():
    pass


def min_max_normalize(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    denominator = maximum - minimum + 1
    return list(map(lambda x: (x - minimum + 1) / denominator, numbers))


def bar_graph():
    dists_rosa = {label: dtw_util.get_distance(global_test_input[0], centroid)
                  for label, centroid in category_dict_rosa.items()}
    labels_bar_graph = []
    librosa_scores_list = []
    for k, v in dists_rosa.items():
        labels_bar_graph.append(k)
        librosa_scores_list.append(v)

    librosa_scores_list = min_max_normalize(librosa_scores_list)

    TrainSphinxData.test(global_test_input[0], librosa_scores_list, labels_bar_graph)
    # GAUTHAM: Read your files here as {label:filename}
    # dists_sphinx = {label: gautrain.get_dist(global_test_input[0], centroid)
    #                 for label, centroid in gautrain.read_label_file_dict().items()}


def spectrogram():
    pass


def classify():
    classify_window = Toplevel()
    classify_window.title("Classification Options")
    classify_window.resizable(width=False, height=False)

    check_var1 = IntVar()
    check_var2 = IntVar()

    c1 = Checkbutton(classify_window, text="Librosa", variable=check_var1,
                     onvalue=1, offvalue=0, height=2,
                     width=10)
    c2 = Checkbutton(classify_window, text="Sphinx", variable=check_var2,
                     onvalue=1, offvalue=0, height=2,
                     width=10)
    c1.grid(row=0, column=0, padx=20, pady=10)
    c2.grid(row=1, column=0, padx=20, pady=10)

    def result():
        classify_window.destroy()
        result_window = Toplevel()
        result_window.title("Results")
        result_window.resizable(width=False, height=False)

        label1 = Label(result_window, text="Statistical Metrics")
        label1.grid(row=0, column=1, pady=10)

        frame1 = Frame(result_window, width=180, height=340, bg='white', bd=3, relief=RIDGE)
        frame1.grid(row=1, column=1, padx=35, pady=20)

        s_len = len(global_test_input)

        for i in range(s_len):
            filename = os.path.split(global_test_input[i])[1]
            test_label = Label(frame1, text=filename)
            test_label.pack(padx=10, pady=10)

        graph_button = Button(result_window, text='Bar Graph for selected file', bd=3, padx=35, command=bar_graph)
        graph_button.grid(row=1, column=2)

        specto_button = Button(result_window, text='Spectogram for selected file(s)', bd=3, padx=35,
                               command=spectrogram)
        specto_button.grid(row=2, column=2)

        test_button = Button(result_window, text='Quick Test', bd=3, pady=15, command=quick_test)
        test_button.grid(row=2, column=1)

    ok_button = Button(classify_window, text="OK", command=result)
    ok_button.grid(row=2, column=0, padx=20, pady=20)

    quit_button = Button(classify_window, text="Cancel", command=lambda: classify_window.destroy())
    quit_button.grid(row=2, column=1, padx=20, pady=20)


category_dict_rosa = read_trained_pickle()
init_trained_display(category_dict_rosa)
#
# train_button = Button(window, text='<', bd=3, padx=20, pady=20, command=train_list)
# train_button.grid(row=1, column=2)
#
# test_button = Button(window, text='>', bd=3, padx=20, pady=20, command=test_list)
# test_button.grid(row=1, column=4)

browse_button = Button(window, text='Add Training Set', bd=3, padx=20, pady=20, command=fileDialog)
browse_button.grid(row=2, column=1)

c_button = Button(window, text='Classify File', bd=3, pady=15, command=testFileDialog)
c_button.grid(row=3, column=1)

window.resizable(width=False, height=False)

window.mainloop()