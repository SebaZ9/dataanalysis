import json
from graphviz import Digraph
from collections import Counter


class AlsoLikes:
    file_name = ""

    def __init__(self, file_name=""):
        self.file_name = file_name

    def update_input_file(self, file_name):
        """
        Updates the input file to be used for the tasks
        :param file_name: The name of the file
        """
        self.file_name = file_name

    def get_documents_readers(self, doc_uuid):
        """
        Get all users that have read a certain document
        :param doc_uuid: The document to find
        :return: List of all visitors of a document
        """
        input_file = open(self.file_name, "r", encoding="utf-8")

        result_data = set()
        for line in input_file:
            json_line = json.loads(line)
            if "subject_doc_id" not in json_line:
                continue
            if json_line["subject_doc_id"] == doc_uuid and json_line["event_type"] == "read":
                result_data.add(json_line["visitor_uuid"])

        # Close the open file stream
        input_file.close()
        # Return found visitor IDs
        return result_data

    def get_users_read_docs(self, visitor_id):
        """
        Get all documents read by a visitor
        :param visitor_id: The visitor to find
        :return: List of all documents read by them
        """
        input_file = open(self.file_name, "r", encoding="utf-8")

        result_data = set()
        for line in input_file:
            json_line = json.loads(line)
            if "subject_doc_id" not in json_line:
                continue
            if json_line["visitor_uuid"] == visitor_id and json_line["event_type"] == "read":
                result_data.add(json_line["subject_doc_id"])

        # Close the open file stream
        input_file.close()
        # Return found visitor IDs
        return result_data

    def also_likes(self, doc_id, visitor_id=""):
        """
        Finds also likes documents for a document and a visitor
        :param doc_id: The document is to use
        :param visitor_id: The visitor to use
        :return: Dictionary containing the also like data
        """
        user_read = {}

        if visitor_id != "" and visitor_id is not None:
            user_read[visitor_id] = {doc_id}

        document_readers = self.get_documents_readers(doc_id)
        if document_readers == set():
            return {}
        for reader in document_readers:
            if reader == visitor_id:
                continue
            readers_docs = self.get_users_read_docs(reader)
            user_read[reader] = {k for k in readers_docs}

        return user_read

    def also_likes_list(self, sorting_method, doc_id, vis_id=""):
        """
        Creates a sorted list of 10 also likes documents.
        :param sorting_method: Sorting method to be used, from HelperFunctions
        :param doc_id: Document id for the also likes
        :param vis_id: Visitor id for the also likes
        :return: The top 10 list of the resulting also like and sorting method
        """
        data = self.also_likes(doc_id, vis_id)
        counted = Counter([item for sublist in data.values() for item in sublist])
        return list(sorting_method(counted).items())[:10]

    def also_likes_graph(self, doc_id, vis_id="", view=False):
        """
        Creates an also likes graph.
        :param doc_id: Document id for the graph
        :param vis_id: Visitor id for the graph
        :param view: If the resulting graph should be opened, True for command line, False for GUI usage
        :return: True/False, success of the graph creation
        """
        data = self.also_likes(doc_id, vis_id)
        if data == {}:
            return False
        dot = Digraph(comment='Also Likes')

        dot.node("Readers", shape="plaintext")
        dot.node("Documents", shape="plaintext")
        dot.edge("Readers", "Documents", label="File:\n" + self.file_name)
        for k in data.keys():
            if k == vis_id:
                dot.node(k[-4:], shape="box", style="filled", fillcolor="green")
            else:
                dot.node(k[-4:], shape="box")
            for v in data[k]:
                if v == doc_id:
                    dot.node(v[-4:], style="filled", fillcolor="green")
                else:
                    dot.node(v[-4:])
                dot.edge(k[-4:], v[-4:])
        if vis_id == "" or vis_id is None:
            file_name = f'DotFiles/{doc_id[-4:]}'
        else:
            file_name = f'DotFiles/{doc_id[-4:]}_{vis_id[-4:]}'
        if not view:
            dot.render(file_name, view=False, format="jpg")
        dot.render(file_name, view=view, format="pdf")
        return True
