import tkinter as tk
import GUI.ClickEvents as Events
import Graph.GenerateGraph as Graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphHolder(tk.Frame):
    """
    Tkinter frame for holding graphs
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent, width=800, height=500, bg="lightgray")


class OptionsPage(tk.Frame):
    """
    OptionsPage: tkinter frame
    Holds all the buttons for selecting which task to show on right frame
    """

    def __init__(self, parent, controller, graph_container):
        tk.Frame.__init__(self, master=parent, width=200, height=500, bg="lightgray")

        lbl_file_name = tk.Label(master=self, text="File Name\nNone Set!")
        if controller.file_name != "":
            lbl_file_name['text'] = f"File Name\n{controller.file_name}"
        lbl_file_name.pack(fill=tk.X, padx=10, pady=5)

        btn_new_file = tk.Button(master=self, text="Set new file",
                                 command=lambda: Events.update_file(controller, lbl_file_name))
        btn_new_file.pack(fill=tk.X, padx=10, pady=5)

        lbl_tasks = tk.Label(master=self, text="Tasks")
        lbl_tasks.pack(fill=tk.X, padx=10, pady=20)

        # Button for View By Country Task
        btn_view_country = tk.Button(master=self, text="2a - Views By Country",
                                     command=lambda: Events.click_views_by_country(graph_container, controller))
        btn_view_country.pack(fill=tk.X, padx=10, pady=5)

        # Button for View By Continent Task
        btn_view_country = tk.Button(master=self, text="2b - Views By Continent",
                                     command=lambda: Events.click_views_by_continent(graph_container, controller))
        btn_view_country.pack(fill=tk.X, padx=10, pady=5)

        # Button for View By Browser Task 3a
        btn_view_browser_full = tk.Button(master=self, text="3a - Views By Browser. Full identifier",
                                          command=lambda: Events.click_views_by_browser(graph_container, controller, False))
        btn_view_browser_full.pack(fill=tk.X, padx=10, pady=5)

        # Button for View By Browser Task 3b
        btn_view_browser = tk.Button(master=self, text="3b - Views By Browser. Browser Name",
                                     command=lambda: Events.click_views_by_browser(graph_container, controller, True))
        btn_view_browser.pack(fill=tk.X, padx=10, pady=5)

        # Button for Reader Profiles Tasks
        btn_reader_profiles = tk.Button(master=self, text="4 - Reader Profiles",
                                        command=lambda: Events.click_avid_readers(graph_container, controller))
        btn_reader_profiles.pack(fill=tk.X, padx=10, pady=5)

        btn_also_likes = tk.Button(master=self, text="5 - Also Likes list",
                                   command=lambda: Events.click_also_likes_list(graph_container, controller))
        btn_also_likes.pack(fill=tk.X, padx=10, pady=5)

        btn_also_likes_graph = tk.Button(master=self, text="6 - Also Likes graph",
                                         command=lambda: Events.click_also_likes(graph_container, controller))
        btn_also_likes_graph.pack(fill=tk.X, padx=10, pady=5)


class GenerateGraphViewsByBrowser(tk.Frame):
    """
    Frame for Views By Browser Graph.
    Created when the option on left panel is clicked.
    """

    def __init__(self, parent, controller, distinguish):
        tk.Frame.__init__(self, master=parent, width=800, height=500, bg="lightgray")

        if controller.is_valid_path():
            # Get the data for the Browser uses
            data = controller.GraphData.browser_graph_data(distinguish)
            data_frame = {
                'Browser': list(data.keys()),
                'Number': list(data.values())
            }

            # Create a graph figure for the data
            graph_figure = Graph.graph_figure_from_data(data_frame, 'Number of Users Vs Browser')
            frame_graph = FigureCanvasTkAgg(graph_figure, self)
            frame_graph.get_tk_widget().grid(row=0, rowspan=2, column=0, padx=10, pady=10)
        """
        
        This code is used for displaying the values for the "Browser task" but with large files, like the 
        3m lines file the output is too long so this functionality has been disabled.
        
        # Creates a frame to hold the values
        frame_values = tk.Frame(self, bg="white")
        frame_values.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N)

        # Value Label
        lbl_vals = tk.Label(frame_values, text="Values", bg="white", font=("Helvetica", 16))
        lbl_vals.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N)

        # Loop through data and create labels for each data entry
        for i in range(len(data_frame['Browser'])):
            lbl_browser = tk.Label(frame_values, text=data_frame['Browser'][i], bg="white")
            lbl_browser.grid(row=i + 1, column=0, sticky=tk.N)

            lbl_number = tk.Label(frame_values, text=data_frame['Number'][i], bg="white")
            lbl_number.grid(row=i + 1, column=1, sticky=tk.N)
        """


class GenerateGraphViewsByContinent(tk.Frame):
    """
    Frame for Views By Continent Graph.
    Created when the option on left panel is clicked.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent, width=800, height=500, bg="lightgray")

        if controller.is_valid_path():
            lbl_doc_id = tk.Label(master=self, text="Document UUID")
            ent_doc_id = tk.Entry(master=self, width=40)
            btn_generate = tk.Button(master=self, width=32, text="Generate Continent Graph",
                                     command=lambda: Events.click_load_graph_into_frame(self,
                                                                                        controller.GraphData.views_by_continent_data,
                                                                                        ent_doc_id.get(),
                                                                                        "Users per Continent",
                                                                                        "Continent"))

            lbl_doc_id.grid(row=0, column=0, padx=10, pady=10)
            ent_doc_id.grid(row=0, column=1, padx=10, pady=10)
            btn_generate.grid(row=0, column=2, padx=10, pady=10)


class GenerateGraphViewsByCountry(tk.Frame):
    """
    Frame for Views By Country Graph.
    Created when the option on left panel is clicked.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent, width=800, height=500, bg="lightgray")

        if controller.is_valid_path():
            lbl_doc_id = tk.Label(master=self, text="Document UUID")
            ent_doc_id = tk.Entry(master=self, width=40)
            btn_generate = tk.Button(master=self, width=32, text="Generate Country Graph",
                                     command=lambda: Events.click_load_graph_into_frame(self,
                                                                                        controller.GraphData.views_by_country_data,
                                                                                        ent_doc_id.get(),
                                                                                        "Users per Country", "Country"))

            lbl_doc_id.grid(row=0, column=0, padx=10, pady=10)
            ent_doc_id.grid(row=0, column=1, padx=10, pady=10)
            btn_generate.grid(row=0, column=2, padx=10, pady=10)


class TopReadersPage(tk.Frame):
    """
    Frame for showing the top 10 avid readers.
    Created when the option on left panel is clicked.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent, width=800, height=500, bg="lightgray")

        if controller.is_valid_path():
            reader_data = controller.ReaderProfiles.top_10_readers()

            lbl_title = tk.Label(self, text="Top 10 avid readers!", bg="white")
            lbl_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            lbl_user = tk.Label(self, text="User ID", bg="white")
            lbl_user.grid(row=1, column=0)

            lbl_amount = tk.Label(self, text="Read Time (Minutes)", bg="white")
            lbl_amount.grid(row=1, column=1)

            if reader_data is None:
                tk.messagebox.showerror("Error", "No data found! Make sure valid document is used!")
            else:
                for i, item in enumerate(reader_data):
                    lbl_key = tk.Label(self, text=item[0], bg="white")
                    lbl_key.grid(row=i + 2, column=0, sticky=tk.N, padx=20, pady=10)

                    lbl_value = tk.Label(self, text=round(item[1] / 60000, 2), bg="white")
                    lbl_value.grid(row=i + 2, column=1, sticky=tk.N, padx=20, pady=10)


class AlsoLikesPage(tk.Frame):
    """
    Frame for showing the also likes page.
    Created when the option on left panel is clicked.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent, width=800, height=500, bg="white")

        if controller.is_valid_path():
            lbl_doc_id = tk.Label(master=self, text="Document UUID")
            lbl_vis_id = tk.Label(master=self, text="Visitor UUID")
            ent_doc_id = tk.Entry(master=self, width=40)
            ent_vis_id = tk.Entry(master=self, width=40)
            btn_enter = tk.Button(master=self, text="Create Graph", command=lambda: Events.click_create_also_likes(self,
                                                                                                                   controller,
                                                                                                                   ent_doc_id.get(),
                                                                                                                   ent_vis_id.get()))

            lbl_doc_id.grid(row=0, column=0, padx=5, pady=5)
            ent_doc_id.grid(row=0, column=1, padx=5, pady=5)
            lbl_vis_id.grid(row=1, column=0, padx=5, pady=5)
            ent_vis_id.grid(row=1, column=1, padx=5, pady=5)
            btn_enter.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

class AlsoLikesPageList(tk.Frame):
    """
    Frame for showing the also likes List.
    Created when the option on left panel is clicked.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent, width=800, height=500, bg="white")

        if controller.is_valid_path():
            lbl_doc_id = tk.Label(master=self, text="Document UUID")
            lbl_vis_id = tk.Label(master=self, text="Visitor UUID")
            ent_doc_id = tk.Entry(master=self, width=40)
            ent_vis_id = tk.Entry(master=self, width=40)
            btn_enter = tk.Button(master=self, text="Create Graph", command=lambda: Events.click_create_also_likes_list(self,
                                                                                                                   controller,
                                                                                                                   ent_doc_id.get(),
                                                                                                                   ent_vis_id.get()))

            lbl_doc_id.grid(row=0, column=0, padx=5, pady=5)
            ent_doc_id.grid(row=0, column=1, padx=5, pady=5)
            lbl_vis_id.grid(row=1, column=0, padx=5, pady=5)
            ent_vis_id.grid(row=1, column=1, padx=5, pady=5)
            btn_enter.grid(row=0, column=2, rowspan=2, padx=5, pady=5)
