from user_agents import parse
import json
from DataGeneration import CountryData
from DataGeneration import HelperFunctions


class GraphData:
    file_name = ""

    def __init__(self, file_name=""):
        self.file_name = file_name

    def update_input_file(self, file_name):
        """
        Updates the input file to be used for the tasks
        :param file_name: The name of the file
        """
        self.file_name = file_name

    def browser_graph_data(self, distinguish=True):
        """
        Find the browser used by users. Users have to be unique.
        :param distinguish: Parameter to change if browser should be distinguished from the user-agent.
        :return: A dictionary containing the the keys and values of the data.
        """
        data_dict = {}
        unique = set()

        input_file = open(self.file_name, "r", encoding="utf-8")
        for line in input_file:
            json_line = json.loads(line)
            if "visitor_useragent" not in json_line or json_line["event_type"] != "read":
                continue
            if json_line["visitor_uuid"] in unique:
                continue
            unique.add(json_line["visitor_uuid"])
            if distinguish:
                HelperFunctions.add_n_to_dict(data_dict, parse(json_line["visitor_useragent"]).browser.family, 1)
            else:
                HelperFunctions.add_n_to_dict(data_dict, json_line["visitor_useragent"], 1)

        input_file.close()
        return data_dict

    def views_by_country_data(self, document_id):
        """
        Find all the countries that the users accessed from.
        :param document_id: The document id to check for.
        :return: A dictionary containing the the keys and values of the data.
        """
        data_dict = {}
        unique = set()

        input_file = open(self.file_name, "r", encoding="utf-8")
        for line in input_file:
            json_line = json.loads(line)
            if "subject_doc_id" in json_line:
                if document_id == json_line["subject_doc_id"] and json_line["visitor_uuid"] not in unique:
                    HelperFunctions.add_n_to_dict(data_dict, json_line["visitor_country"], 1)
                    unique.add(json_line["visitor_uuid"])

        input_file.close()
        return data_dict

    def views_by_continent_data(self, document_id):
        """
        Find all the continents that the users accessed from.
        :param document_id: The document id to check for.
        :return: A dictionary containing the the keys and values of the data.
        """
        data_dict = self.views_by_country_data(document_id)
        continent_data_dict = {}

        for key, value in data_dict.items():
            HelperFunctions.add_n_to_dict(continent_data_dict,
                                          CountryData.cntry_to_cont[key],
                                          value)

        return continent_data_dict
