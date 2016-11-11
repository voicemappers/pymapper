import json
from tkinter import Frame, BOTH, Tk, X, Label, LEFT, Entry, StringVar, Button, RIGHT, messagebox


class CommandConfig(Frame):
    def __init__(self, parent, config_filename, background='white'):
        Frame.__init__(self, parent, background=background)
        self.parent = parent
        self.configFileName = config_filename
        self.textVariables = []
        self.labelsStr = []
        self.init_ui()

    def init_ui(self):
        self.parent.title('Command configuration')
        self.pack(fill=BOTH, expand=True)
        # Reading the config file.
        label_cmd = CommandConfig.read_config(self.configFileName)
        # Filling up the form.
        for label, command in sorted(label_cmd.items()):
            # Creating a new frame for each label-command pair.
            frame = Frame(self)
            frame.pack(fill=X)
            # Creating a new label.
            self.labelsStr.append(label)
            label = Label(frame, text=label, width=10)
            label.pack(side=LEFT, padx=5, pady=5)
            # Text variable to hold the command's value.
            v = StringVar()
            v.set(command)
            self.textVariables.append(v)
            # Field for entering the command.
            entry = Entry(frame, textvariable=v)
            entry.pack(fill=X, padx=5, expand=True)
        # Button
        frame = Frame(self)
        frame.pack(fill=X)
        save_button = Button(frame, text='Save', command=self.save_config)
        save_button.pack(side=RIGHT, padx=5, pady=5)
        self.center_window()

    @staticmethod
    def read_config(config_filename):
        with open(config_filename, 'r') as config_file:
            return {label: cmd for label, cmd in
                    map(lambda x: (x[0], x[1][1] if len(x[1]) == 2 else ''), json.load(config_file).items())}

    def save_config(self):
        for i in range(len(self.textVariables)):
            if self.textVariables[i].get() == '':
                messagebox.showerror(title='Error', message='Command for \'' + self.labelsStr[i] + '\' is empty')
                break
        else:
            with open(self.configFileName, 'r') as config_file:
                label_centroid = json.load(config_file)
            with open(self.configFileName, 'w') as config_file:
                label_cmd = {label: [label_centroid[label][0], cmd] for label, cmd in
                             zip(self.labelsStr, map(lambda x: x.get(), self.textVariables))}
                config_file.write(json.dumps(label_cmd))
            self.quit()

    def center_window(self):
        w = 500
        h = 400
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main_config_ui():
    root = Tk()
    app = CommandConfig(root, 'train_voice_cmd.json')
    root.mainloop()


if __name__ == '__main__':
    main_config_ui()
