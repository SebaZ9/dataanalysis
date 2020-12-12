import json
from DataGeneration import HelperFunctions


class ReaderProfiles:
    file_name = ""

    def __init__(self, file_name=""):
        self.file_name = file_name

    def update_input_file(self, file_name):
        """
        Updates the input file to be used for the tasks
        :param file_name: The name of the file
        """
        self.file_name = file_name

    def top_10_readers(self):
        """
        Return the the top 10 readers, based on their readtime
        :return: Dict of 10 readers with their read times.
        """
        data_dict = {}
        try:
            input_file = open(self.file_name, "r", encoding="utf-8")
            for line in input_file:
                json_line = json.loads(line)
                if "event_readtime" in json_line:
                    HelperFunctions.add_n_to_dict(data_dict, json_line["visitor_uuid"], json_line["event_readtime"])

            input_file.close()
            ordered_dict = {k: v for k, v in sorted(data_dict.items(), key=lambda item: item[1], reverse=True)}

            return list(ordered_dict.items())[:10]
        except json.JSONDecodeError:
            return
