import tkinter as tk
import Graph.GenerateGraph as Graph
from DataGeneration import HelperFunctions
import GUI.Frames as Frames
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os.path
from PIL import ImageTk, Image
import time


def close_current_tab(frame):
    """
    Closes the 1st child of a given frame.
    :param frame: The frame to get the child from.
    """
    children = frame.winfo_children()
    if len(children) != 0:
        children[0].destroy()


def click_views_by_browser(frame, controller, distinguish):
    """
    Click Event for opening the Views by Browser Page.
    :param distinguish: Parameter to determine if the full user-agent is shown
    :param frame: Parent frame.
    :param controller: Frame controller.
    """
    close_current_tab(frame)
    views_by_browser = Frames.GenerateGraphViewsByBrowser(frame, controller, distinguish)
    views_by_browser.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


def click_views_by_country(frame, controller):
    """
    Click Event for opening the Views by Country Page.
    :param frame: Parent frame.
    :param controller: Frame controller.
    """
    close_current_tab(frame)
    views_by_country = Frames.GenerateGraphViewsByCountry(frame, controller)
    views_by_country.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


def click_views_by_continent(frame, controller):
    """
    Click Event for opening the Views by Continent Page.
    :param frame: Parent frame.
    :param controller: Frame controller.
    """
    close_current_tab(frame)
    views_by_country = Frames.GenerateGraphViewsByContinent(frame, controller)
    views_by_country.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


def click_avid_readers(frame, controller):
    """
    Click Event for opening the top 10 avid users page.
    :param frame: Parent frame.
    :param controller: Frame controller.
    """
    close_current_tab(frame)
    views_by_country = Frames.TopReadersPage(frame, controller)
    views_by_country.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


def click_also_likes_list(frame, controller):
    """
    Click Event for opening the top 10 avid users page.
    :param frame: Parent frame.
    :param controller: Frame controller.
    """
    close_current_tab(frame)
    also_likes = Frames.AlsoLikesPageList(frame, controller)
    also_likes.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

def click_also_likes(frame, controller):
    """
    Click Event for opening the top 10 avid users page.
    :param frame: Parent frame.
    :param controller: Frame controller.
    """
    close_current_tab(frame)
    also_likes = Frames.AlsoLikesPage(frame, controller)
    also_likes.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


def click_load_graph_into_frame(frame, data_function, doc_id, title, axis_name):
    """
    Click Event for loading the graph into the Views By Continent frame and adding a values panel.
    :param frame: The frame to add the graph to.
    :param data_function: The function that will be used to retrieve the data
    :param doc_id: The id of the document to retrieve the data from.
    :param title: The title of the graph.
    :param axis_name: The name of the bottom axis.
    """
    if doc_id == "":
        tk.messagebox.showerror("Error", "No input detected.\nPlease enter a valid document UUID!")
        return
    if len(frame.winfo_children()) == 4:
        frame.winfo_children()[3].destroy()
    data = data_function(doc_id)
    if data == {}:
        tk.messagebox.showerror("Error",
                                "No results.\nEither no documents were found matching the ID, or\nan invalid ID was given")
        return
    data_frame = {
        axis_name: list(data.keys()),
        'Number': list(data.values())
    }
    graph_figure = Graph.graph_figure_from_data(data_frame, title)
    frame_graph = FigureCanvasTkAgg(graph_figure, frame)
    frame_graph.get_tk_widget().grid(row=1, rowspan=2, column=0, columnspan=3)

    # Creates a frame to hold the values
    frame_values = tk.Frame(frame, bg="white")
    frame_values.grid(row=0, rowspan=2, column=3, padx=10, pady=10, sticky=tk.N)

    # Value Label
    lbl_vals = tk.Label(frame_values, text="Values", bg="white", font=("Helvetica", 16))
    lbl_vals.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N)

    # Add values to the panel
    for i in range(len(data_frame[axis_name])):
        lbl_browser = tk.Label(frame_values, text=data_frame[axis_name][i], bg="white")
        lbl_browser.grid(row=i + 1, column=0, sticky=tk.N)

        lbl_number = tk.Label(frame_values, text=data_frame['Number'][i], bg="white")
        lbl_number.grid(row=i + 1, column=1, sticky=tk.N)


def update_file(controller, file_name_label):
    """
    Method for updating the file to be used when running tasks
    :param file_name_label: The label of the file name string
    :param controller: The windows controller
    """
    file_name = tk.filedialog.askopenfilename(initialdir="/", title="Select JSON file",
                                              filetypes=(("JSON File", "*.json"),))
    if not os.path.isfile(file_name):
        tk.messagebox.showerror("Error", "File not set - No file chosen!")
        return
    controller.update_data_file(file_name)
    file_name_label['text'] = f"File Name\n{file_name}"
    tk.messagebox.showinfo("New file", f"{file_name} set as new file.")


def click_create_also_likes(frame, controller, doc_id, vis_id):
    """
    Click Event for creating the also likes graph
    :param frame: Frame to put the graph into.
    :param controller: The window controller
    :param doc_id: The document id for the graph
    :param vis_id: The visitor id for the graph
    :return: True/False if the graph was created successfully
    """
    if doc_id == "":
        tk.messagebox.showerror("Error", "Please enter a Document ID!")
        return
    result = controller.AlsoLikes.also_likes_graph(doc_id, vis_id)
    if not result:
        tk.messagebox.showerror("Error", "No Documents found with given ID!")
        return
    if vis_id == "" or vis_id is None:
        dot_file_name = f'DotFiles/{doc_id[-4:]}.jpg'
    else:
        dot_file_name = f'DotFiles/{doc_id[-4:]}_{vis_id[-4:]}.jpg'
    max_checks = 60
    for i in range(max_checks):
        if os.path.isfile(dot_file_name):
            break
        time.sleep(0.5)
    if len(frame.winfo_children()) == 6:
        frame.winfo_children()[5].destroy()
    img = ImageTk.PhotoImage(Image.open(dot_file_name))
    panel = tk.Label(frame, image=img)
    panel.photo = img
    panel.grid(row=2, column=0, columnspan=3)


def click_create_also_likes_list(frame, controller, doc_id, vis_id):
    """
    Click Event for creating the also likes list
    :param frame: Frame to put the graph into.
    :param controller: The window controller
    :param doc_id: The document id for the graph
    :param vis_id: The visitor id for the graph
    :return: True/False if the graph was created successfully
    """
    if doc_id == "":
        tk.messagebox.showerror("Error", "Please enter a Document ID!")
        return
    result = controller.AlsoLikes.also_likes_list(HelperFunctions.sort_descending, doc_id, vis_id)
    if not result:
        tk.messagebox.showerror("Error", "No Documents found with given ID!")
        return

    lbl_doc_id = tk.Label(master=frame, text="Document UUID")
    lbl_number_reads = tk.Label(master=frame, text="Number of Reads")
    lbl_doc_id.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    lbl_number_reads.grid(row=2, column=2, padx=5, pady=5)
    for i, res in enumerate(result):
        lbl_k = tk.Label(master=frame, text=res[0])
        lbl_k.grid(row=3+i, column=0, columnspan=2, padx=5, pady=5)
        lbl_v = tk.Label(master=frame, text=res[1])
        lbl_v.grid(row=3+i, column=2, padx=5, pady=5)
