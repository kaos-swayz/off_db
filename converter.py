from _main import open_json_file, save_json_file

from os import listdir
from difflib import SequenceMatcher

class Converter:
    def __init__(self):
        pass


    """ JSON to CSV """

    """ main converter functions """

    def save_combined_csv(self, input_file_name="datasets/combined_data_match.json", output_file_name="datasets/combined_data_match.csv"):
        self.data_to_csv(function=self.convert_data_to_csv_format,input_file_name=input_file_name, output_file_name=output_file_name)

    def save_pattern_csv(self, input_file_name="datasets/combined_data_match.json", output_file_name="datasets/_pattern.csv"):
        self.data_to_csv(function=self.convert_data_to_csv_pattern,input_file_name=input_file_name, output_file_name=output_file_name)

    """ component converter functions """

    def data_to_csv(self, function, input_file_name, output_file_name):
        data = open_json_file(input_file_name)

        csv_data = function(data)

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

    def open_csv(self, file_name):
        with open(file_name, "r", encoding="UTF-8") as fp:
            data = fp.read()
        print("read from a file: {}".format(file_name))
        return data


    """ JSON to CSV """

    """ main converter functions """

    def save_combined_json(self, input_file_name="datasets/combined_data_match_fix_to_merge.csv", output_file_name="datasets/combined_data_to_merge.json"):
        self.data_to_json(function=self.convert_data_to_json_format, input_file_name=input_file_name, output_file_name=output_file_name)

    """ component converter functions """

    def data_to_json(self, function, input_file_name, output_file_name):
        data = self.open_csv(file_name=input_file_name)

        json_data = function(data)

        save_json_file(file_name=output_file_name, content=json_data)

    def convert_data_to_json_format(self, data):
        output = {}

        data = data.split("\n")

        # print(data[0])

        el_dict = {
            0: "name",
            1: "type",
            2: "source",
            3: "id",
            4: "match_id",
            5: "match_level",
            6: "record_rating",
            7: "city",
            8: "district",
            10: "address",
            11: "av_office",
            12: "av_office_vol",
            13: "rent_office",
            14: "rent_retail",
            15: "rent_warehouse",
            16: "service_charge",
            17: "cost_parking_surface",
            18: "cost_parking_underground",
            19: "min_space_to_let",
            20: "min_lease",
            21: "add_on_factor",
            22: "building_status",
            23: "building_class",
            24: "total_net_space",
            25: "total_gross_space",
            26: "completion_date",
            27: "ground_floors",
            28: "floor_plate",
            29: "no_surface_parking",
            30: "no_underground_parking",
            31: "parking_ratio",
            32: "building_certification",
            33: "sprinklers",
            34: "access_control",
            35: "computer_cabling",
            36: "switchboard",
            37: "smoke_detectors",
            38: "suspended_ceiling",
            39: "openable_windows",
            40: "partition_walls",
            41: "backup_power_supply",
            42: "telephone_cabling",
            43: "power_cabling",
            44: "air_conditioning",
            45: "raised_floor",
            46: "carpeting",
            47: "fibre_optic_connections",
            48: "BMS",
            49: "rm_id",
            50: "rm_url",
            51: "rm_pic_url",
            52: "bj_id",
            53: "bj_url",
            54: "bj_pic_url",
            55: "add_info"
        }

        for e in data:
            item_index = data.index(e)
            if item_index in range(1,len(data)):
                try:
                    item = e.split("|")
                    output[item_index] = {}

                    output[item_index]["01.main_data"] = {}
                    output[item_index]["02.location_details"] = {}
                    output[item_index]["03.offer_details"] = {}
                    output[item_index]["04.building_details"] = {}
                    output[item_index]["05.fitout_standard"] = {}
                    output[item_index]["09.metadata"] = {}

                    for i in el_dict.keys():
                        if i in range(0, 7):
                            output[item_index]["01.main_data"][el_dict[i]] = self.determine_value(item[i])
                        elif i in range(7, 11):
                            output[item_index]["02.location_details"][el_dict[i]] = self.determine_value(item[i])
                        elif i in range(11, 22):
                            output[item_index]["03.offer_details"][el_dict[i]] = self.determine_value(item[i])
                        elif i in range(22, 33):
                            output[item_index]["04.building_details"][el_dict[i]] = self.determine_value(item[i])
                        elif i in range(33, 49):
                            output[item_index]["05.fitout_standard"][el_dict[i]] = self.determine_value(item[i])
                        elif i in range(49, 56):
                            output[item_index]["09.metadata"][el_dict[i]] = self.determine_value(item[i])
                except IndexError as err:
                    print("Exception {} at {}: {}".format(err, item_index, item))

        return output

    def determine_value(self, raw_value):
        if raw_value == "PRAWDA":
            new_value = True
        elif raw_value == "FAŁSZ":
            new_value = False
        else:
            new_value = raw_value

        return new_value







if __name__ == "__main__":
    c = Converter()

    c.save_combined_json()
