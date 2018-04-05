from _main import open_json_file, save_json_file

from os import listdir
from difflib import SequenceMatcher

class Converter:
    def __init__(self):

        self.item_pattern = {
            '01.main_data': {
                'name': '',
                'type': '',
                'source': '',
                'id': '',
                'match_id': '',
                'match_level': '',
                'match_address': '',
                'match_a_level': '',
                'record_rating': ''},
            '02.location_details': {
                'city': '',
                'district': '',
                'address': ''},
            '03.offer_details': {
                'av_office': '',
                'av_office_vol': '',
                'rent_office': '',
                'rent_retail': '',
                'rent_warehouse': '',
                'service_charge': '',
                'cost_parking_surface': '',
                'cost_parking_underground': '',
                'min_space_to_let': '',
                'min_lease': '',
                'add_on_factor': ''},
            '04.building_details': {
                'building_status': '',
                'building_class': '',
                'total_net_space': '',
                'total_gross_space': '',
                'completion_date': '',
                'ground_floors': '',
                'underground_floors': '',
                'floor_plate': '',
                'no_surface_parking': '',
                'no_underground_parking': '',
                'parking_ratio': '',
                'building_certification': ''},
            '05.fitout_standard': {
                'sprinklers': '',
                'access_control': '',
                'computer_cabling': '',
                'switchboard': '',
                'smoke_detectors': '',
                'suspended_ceiling': '',
                'openable_windows': '',
                'partition_walls': '',
                'backup_power_supply': '',
                'telephone_cabling': '',
                'power_cabling': '',
                'air_conditioning': '',
                'raised_floor': '',
                'carpeting': '',
                'fibre_optic_connections': '',
                'BMS': ''},
            '09.metadata': {
                'rm_id': '',
                'rm_url': '',
                'rm_pic_url': '',
                'bj_id': '',
                'bj_url': '',
                'bj_pic_url': '',
                'oc_id': '',
                'oc_url': '',
                'oc_pic_url': '',
                'add_info': ''}
        }


    """ CSV manipulations: save & open """

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

    def save_combined_csv(self, input_file_name, output_file_name):
        self.data_to_csv(function=self.convert_data_to_csv_format,input_file_name=input_file_name, output_file_name=output_file_name)

    def save_pattern_csv(self, input_file_name, output_file_name="datasets/_pattern.csv"):
        self.data_to_csv(function=self.convert_data_to_csv_pattern,input_file_name=input_file_name, output_file_name=output_file_name)

    """ component converter functions """

    def data_to_csv(self, function, input_file_name, output_file_name):
        data = open_json_file(input_file_name)

        csv_data = function(data)

        self.save_to_csv(file_name=output_file_name, content=csv_data)

    def convert_data_to_csv_format(self, data):
        output_list = []
        print(data)
        for item in data:

            print(item)
            building_list = []
            for nav_dict in data[item].keys():
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
                # print(key)
                pattern_list.append(key)

        return "|".join(pattern_list)







    """ CSV to JSON """

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
            9: "address",
            10: "av_office",
            11: "av_office_vol",
            12: "rent_office",
            13: "rent_retail",
            14: "rent_warehouse",
            15: "service_charge",
            16: "cost_parking_surface",
            17: "cost_parking_underground",
            18: "min_space_to_let",
            19: "min_lease",
            20: "add_on_factor",
            21: "building_status",
            22: "building_class",
            23: "total_net_space",
            24: "total_gross_space",
            25: "completion_date",
            26: "ground_floors",
            27: "floor_plate",
            28: "no_surface_parking",
            29: "no_underground_parking",
            30: "parking_ratio",
            31: "building_certification",
            32: "sprinklers",
            33: "access_control",
            34: "computer_cabling",
            35: "switchboard",
            36: "smoke_detectors",
            37: "suspended_ceiling",
            38: "openable_windows",
            39: "partition_walls",
            40: "backup_power_supply",
            41: "telephone_cabling",
            42: "power_cabling",
            43: "air_conditioning",
            44: "raised_floor",
            45: "carpeting",
            46: "fibre_optic_connections",
            47: "BMS",
            48: "rm_id",
            49: "rm_url",
            50: "rm_pic_url",
            51: "bj_id",
            52: "bj_url",
            53: "bj_pic_url",
            54: "add_info"
        }

        for e in data:
            item_index = data.index(e)
            if item_index in range(1,len(data)):
                # try:
                item = e.split("|")
                if len(item) > 5:
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
                # except IndexError as err:
                #     print("Exception {} at {}: {}".format(err, item_index, item))

        return output

    def determine_value(self, raw_value):
        if raw_value.lower() in ["prawda", "true"]:
            new_value = True
        elif raw_value.lower() in ["fałsz", "false"]:
            new_value = False
        else:
            new_value = raw_value

        return new_value







if __name__ == "__main__":
    c = Converter()

    c.save_combined_csv(input_file_name="datasets/st3_combined_data.json", output_file_name="datasets/st3_combined_data_conv.csv")
    # c.save_pattern_csv(input_file_name="datasets/st3_combined_data.json")

