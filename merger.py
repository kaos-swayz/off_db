from _main import open_json_file, save_json_file

from os import listdir
from difflib import SequenceMatcher

class Merger:
    def __init__(self):
        pass

    """ compare components """




    """ csv components """

    def save_combined_csv_data(self):
        file_name = "datasets/combined_data.csv"

        with open(file_name, "w", encoding="UTF-8") as fp:
            fp.write("")

        for file in [f for f in listdir("datasets")]:
            if "final" in file:
                file_data = open_json_file("datasets/{}".format(file))
                # print(len(file_data))
                csv_data = self.convert_final_data_file_to_csv(file_data)
                self.save_to_csv(file_name=file_name, content=csv_data)

    def convert_final_data_file_to_csv(self, data):
        output_list = []
        for building_record in data:
            building_list = []
            for nav_dict in building_record:
                for key in building_record[nav_dict].keys():
                    value = building_record[nav_dict][key]
                    building_list.append(str(value))
            building_list.append("\n")
            output_list.append(building_list)
        csv_list = []
        for element in output_list:
            csv_el = "|".join(element)
            csv_list.append(csv_el)
        return "".join(csv_list)

    def csv_pattern(self, data):
        pattern_list = []
        for building_record in data:

            for nav_dict in building_record:
                for key in building_record[nav_dict].keys():
                    pattern_list.append(key)
        return "|".join(pattern_list)

    def save_to_csv(self, file_name, content):
        if type(content) == str:
            with open(file_name, "a", encoding="UTF-8") as fp:
                fp.write(content)
        print("saved to a file: {}".format(file_name))





if __name__ == "__main__":
    # m = Merger()
    # data = open_json_file("datasets/final_data_rm.json")
    # pattern = m.csv_pattern([data[0]])
    # m.save_to_csv(file_name="_pattern.csv", content=pattern)