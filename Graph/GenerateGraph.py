import matplotlib.pyplot as plt
import pandas


def graph_window_from_data(data, title, sort=True, sublot=0.2):
    """
    Creates a bar graph with provided data and opens a window containing the graph.
    :param data: A dictionary containing the data to be graphed.
    :param title: The title that is given to the graph.
    :param sort: Bool to sort the data. Default True.
    """
    dataframe = pandas.DataFrame(data, columns=list(data.keys()))
    if sort:
        dataframe = dataframe.sort_values(by=dataframe.columns[1], ascending=False)
    dataframe.plot.bar(x=dataframe.columns[0], y=dataframe.columns[1], rot=90, title=title, legend=False)
    plt.subplots_adjust(bottom=sublot)
    plt.show()


def graph_figure_from_data(data, title):
    """
    Creates a Figure for a graph with the data and title provided.
    :param data: A dictionary containing the data to be graphed.
    :param title: The title that is given to the graph.
    :return: Matplotlib Figure containing the graph.
    """
    data_frame = pandas.DataFrame(data, columns=list(data.keys()))
    data_frame = data_frame[list(data.keys())].groupby(list(data.keys())[0]).sum()
    data_frame = data_frame.sort_values(by="Number", ascending=False)

    figure = plt.Figure(figsize=(6, 5), dpi=100, tight_layout=True)
    axes = figure.add_subplot(111)
    axes.set_title(title)
    data_frame.plot(kind='bar', legend=False, ax=axes)

    return figure
