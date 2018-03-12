from _main import open_json_file, save_json_file

from os import listdir
from difflib import SequenceMatcher

class Converter_csv:
    def __init__(self):
        pass


    """ main converter functions """

    def save_combined_csv(self, input_file_name="datasets/combined_data_match.json", output_file_name="combined_data_match.csv.csv"):
        self.data_to_csv(function=self.convert_data_to_csv_format(),input_file_name=input_file_name, output_file_name=output_file_name)

    def save_pattern_csv(self, input_file_name="datasets/combined_data_match.json", output_file_name="datasets/_pattern.csv"):
        self.data_to_csv(function=self.convert_data_to_csv_pattern(),input_file_name=input_file_name, output_file_name=output_file_name)



    """ component converter functions """

    def data_to_csv(self, function, input_file_name, output_file_name):
        data = open_json_file(input_file_name)

        csv_data = function

        self.save_to_csv(file_name=output_file_name, content=csv_data)

    def convert_data_to_csv_format(self, data):
        output_list = []
        for item in data:
            building_list = []
            for nav_dict in data[item]:
                for key in data[item][nav_dict].keys():
                    value = data[item][nav_dict][key]
                    building_list.append((str(value)))
            building_list.append("\n")
            output_list.append(building_list)
        csv_list = []
        for element in output_list:
            csv_el = "|".join(element)
            csv_list.append(csv_el)
        return "".join(csv_list)

    def convert_data_to_csv_pattern(self, data):
        pattern_list = []

        items = [i for i in data.keys()]
        item = items[0]
        for nav_dict in data[item]:
            for key in data[item][nav_dict].keys():
                print(key)
                pattern_list.append(key)

        return "|".join(pattern_list)



    """ saving csv """

    def save_to_csv(self, file_name, content):
        if type(content) == str:
            with open(file_name, "w", encoding="UTF-8") as fp:
                fp.write(content)
        print("saved to a file: {}".format(file_name))



if __name__ == "__main__":
    c = Converter_csv()

    c.save_combined_csv()
    # c.save_pattern_csv()