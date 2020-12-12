import tkinter as tk
import GUI.Frames as Frames
from DataGeneration import GraphData, ReaderProfiles, AlsoLikes
import os.path

'''
    GraphApplication: tkinter main window 
    Holds all other tkinter frames:
        Left bar with task options
        Right bar which contains the resulting graphs
'''
class GraphApplication(tk.Tk):
    """
    Root window for tkinter, stores object for data generation.
    """
    def __init__(self, file_name="", *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "CW2 Graph GUI Application")

        self.file_name = file_name
        self.GraphData = GraphData.GraphData(self.file_name)
        self.ReaderProfiles = ReaderProfiles.ReaderProfiles(self.file_name)
        self.AlsoLikes = AlsoLikes.AlsoLikes(self.file_name)

        container = tk.Frame(master=self, width=1000, height=500, bg="white")
        container.pack(fill=tk.BOTH, expand=True)

        frame_right = Frames.GraphHolder(container, self)
        frame_options_page = Frames.OptionsPage(container, self, frame_right)

        frame_options_page.pack(fill=tk.Y, side=tk.LEFT)
        frame_right.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def update_data_file(self, file_name):
        self.file_name = file_name
        self.GraphData.update_input_file(file_name)
        self.ReaderProfiles.update_input_file(file_name)
        self.AlsoLikes.update_input_file(file_name)

    def is_valid_path(self):
        if not os.path.isfile(self.file_name) or self.file_name == "":
            tk.messagebox.showerror("Error",
                                    "Data file is invalid.\nMake sure file name is set and is relative to the cw.py file!")
            return False
        return True


def run(input_file=""):
    """
    Creates and runs a window.
    :param input_file: File name of the input file, can be left empty
    """
    app = GraphApplication(file_name=input_file)
    app.mainloop()
