from DataGeneration import GraphData, ReaderProfiles, AlsoLikes, HelperFunctions
from Graph import GenerateGraph
import GuiController
import os
import sys
import pandas
import argparse


def run_commands():
    """
    Runs the code for command line usage.
    """
    args = setup_argparse()
    switch = {
        '2a': graph_country_views,
        '2b': graph_continent_views,
        '3a': graph_browser3a_uses,
        '3b': graph_browser3b_uses,
        '4': get_reader_profiles,
        '5d': also_likes_list,
        '6': also_likes_graph,
        '7': launch_gui
    }
    switch.get(args.task_id)(args)


def setup_argparse():
    """
    Sets up argparse with the relevant arguments and checks validity.
    :return: Argparse object with all the command line arguments
    """
    my_parser = argparse.ArgumentParser(description='Some Description', formatter_class=argparse.RawTextHelpFormatter)

    my_parser.add_argument(
        '-f',
        "--file_name",
        metavar="",
        required=True,
        type=str,
        help="The path to the input file"
    )

    my_parser.add_argument(
        "-t",
        "--task_id",
        metavar="",
        required=True,
        type=str,
        help="The task to be preformed. Possible task are: \n"
             "'2a' - Views by country, requires document id. \n"
             "'2b' - Views by continent, requires document id. \n"
             "'3a' - Graph of all browser identifiers of the viewers. \n"
             "'3b' - Graph of all browser identifiers of the  - distinguishing them by browser name. \n"
             "'4' - Reader Profiles, The top 10 readers with the highest read times. \n"
             "'5d' - Also Likes list of documents, top 10 documents are returned, requires document id and optionally a user id. \n"
             "'6' - Also Likes graph, requires document id and optionally a user id. \n"
             "'7' - Opens GUI."
    )
    
    my_parser.add_argument(
        "-d",
        "--doc_uuid",
        metavar="",
        type=str,
        help="The Documents UUID"
    )

    my_parser.add_argument(
        "-u",
        "--user_uuid",
        metavar="",
        type=str,
        help="The Users UUID"
    )

    args = my_parser.parse_args()

    # Check inputs
    if not os.path.isfile(args.file_name):
        sys.exit(f"File provided '{args.file_name}' does not exist. All files must be relative to cw2.py.")

    if args.task_id not in ('2a', '2b', '3a', '3b', '4', '5d', '6', '7'):
        sys.exit(f"Task provided '{args.task_id}' is not valid. -h will show possible tasks.")

    return args


def graph_country_views(args):
    """
    Task 2a: Show graph of countries for a document
    :param args: Commandline arguments from argparse
    """
    if args.doc_uuid is None:
        sys.exit(f"Task 2a requires the document id!")
    graph_data = GraphData.GraphData(args.file_name)
    document_data = graph_data.views_by_country_data(args.doc_uuid)
    if document_data == {}:
        sys.exit(f"No data was found with doc ID: {args.doc_uuid}. Either no data was found or the id is incorrect!")
    document_data_frame = pandas.DataFrame({
        'Country': list(document_data.keys()),
        'Number': list(document_data.values())
    })
    GenerateGraph.graph_window_from_data(document_data_frame, "Viewed From Country")


def graph_continent_views(args):
    """
    Task 2b: Show graph of continents for a document
    :param args: Commandline arguments from argparse
    """
    if args.doc_uuid is None:
        sys.exit(f"Task 2b requires the document id!")
    graph_data = GraphData.GraphData(args.file_name)
    document_data = graph_data.views_by_continent_data(args.doc_uuid)
    if document_data == {}:
        sys.exit(f"No data was found with doc ID: {args.doc_uuid}. Either no data was found or the id is incorrect!")
    document_data_frame = pandas.DataFrame({
        'Continent': list(document_data.keys()),
        'Number': list(document_data.values())
    })
    GenerateGraph.graph_window_from_data(document_data_frame, "Viewed From Continent")

def graph_browser3a_uses(args):
    """
    Task 3a: Show user identifiers as a graph and print in terminal
    :param args: Commandline arguments from argparse
    """
    graph_data = GraphData.GraphData(args.file_name)
    browser_data = graph_data.browser_graph_data(False)
    if browser_data == {}:
        sys.exit(f"No data was found for task 3a, either no browser data exists or something went wrong!")
    browser_data_frame = pandas.DataFrame({
        'Browser': list(browser_data.keys()),
        'Number': list(browser_data.values())
    })
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(browser_data_frame.sort_values(by="Number", ascending=False))
    GenerateGraph.graph_window_from_data(browser_data_frame, "Document Views With Browser", sublot=0.5)

def graph_browser3b_uses(args):
    """
    Task 3b: Show graph of browsers used as a graph and print in terminal
    :param args: Commandline arguments from argparse
    """
    graph_data = GraphData.GraphData(args.file_name)
    browser_data = graph_data.browser_graph_data()
    if browser_data == {}:
        sys.exit(f"No data was found for task 3b, either no browser data exists or something went wrong!")
    browser_data_frame = pandas.DataFrame({
        'Browser': list(browser_data.keys()),
        'Number': list(browser_data.values())
    })
    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
        print(browser_data_frame.sort_values(by="Number", ascending=False))
    GenerateGraph.graph_window_from_data(browser_data_frame, "Document Views With Browser", sublot=0.5)


def get_reader_profiles(args):
    """
    Task 4: Show top 10 readers by minutes
    :param args: Commandline arguments from argparse
    """
    reader_profiles = ReaderProfiles.ReaderProfiles(args.file_name)
    reader_data = reader_profiles.top_10_readers()

    for reader in reader_data:
        print(f"Reader UUID: {reader[0]}. Read time(Minutes): {round(reader[1]/60000, 2)}")

def also_likes_list(args):
    """
    Task 5d: Also likes list of given document and optional visitor.
    :param args: Commandline arguments from argparse
    """
    if args.doc_uuid is None:
        sys.exit(f"Task 5d requires the document id!")
    also_likes = AlsoLikes.AlsoLikes(args.file_name)
    alsolikes_list = also_likes.also_likes_list(HelperFunctions.sort_descending, args.doc_uuid, args.user_uuid)
    if alsolikes_list == {}:
        sys.exit(f"No data was found. Make sure the correct document id is given!")
    for val in alsolikes_list:
        print(f"DocID: {val[0]}. Views {val[1]}")

def also_likes_graph(args):
    """
    Task 6: Produces a graph for the also likes list.
    :param args: Commandline arguments from argparse
    """
    if args.doc_uuid is None:
        sys.exit(f"Task 5d requires the document id!")
    also_likes = AlsoLikes.AlsoLikes(args.file_name)
    if not also_likes.also_likes_graph(args.doc_uuid, args.user_uuid, True):
        sys.exit(f"No data was found. Make sure the correct document id is given!")

def launch_gui(args):
    """
    Task 7: Opens the GUI for the tasks.
    :param args: Commandline arguments from argparse
    """
    GuiController.run(args.file_name)
