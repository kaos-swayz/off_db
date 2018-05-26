from _main import open_json_file, save_json_file

from time import sleep
from copy import deepcopy
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
                'match_rating': ''},
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
        # print(data)
        for item in data:

            print("converting data: {} to csv format: {}".format(item, data[item]))
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

    def convert_data_to_json_format(self, data, separator="|", max_iterations=9999):
        output = {}

        el_dict = {
            0: "name",
            1: "type",
            2: "source",
            3: "id",
            4: "match_id",
            5: "match_level",
            6: "match_address",
            7: "match_a_level",
            8: "match_rating",
            9: "city",
            10: "district",
            11: "address",
            12: "av_office",
            13: "av_office_vol",
            14: "rent_office",
            15: "rent_retail",
            16: "rent_warehouse",
            17: "service_charge",
            18: "cost_parking_surface",
            19: "cost_parking_underground",
            20: "min_space_to_let",
            21: "min_lease",
            22: "add_on_factor",
            23: "building_status",
            24: "building_class",
            25: "total_net_space",
            26: "total_gross_space",
            27: "completion_date",
            28: "ground_floors",
            29: "underground_floors",
            30: "floor_plate",
            31: "no_surface_parking",
            32: "no_underground_parking",
            33: "parking_ratio",
            34: "building_certification",
            35: "sprinklers",
            36: "access_control",
            37: "computer_cabling",
            38: "switchboard",
            39: "smoke_detectors",
            40: "suspended_ceiling",
            41: "openable_windows",
            42: "partition_walls",
            43: "backup_power_supply",
            44: "telephone_cabling",
            45: "power_cabling",
            46: "air_conditioning",
            47: "raised_floor",
            48: "carpeting",
            49: "fibre_optic_connections",
            50: "BMS",
            51: "rm_id",
            52: "rm_url",
            53: "rm_pic_url",
            54: "bj_id",
            55: "bj_url",
            56: "bj_pic_url",
            57: "oc_id",
            58: "oc_url",
            59: "oc_pic_url",
            60: "add_info"
        }

        data = data.split("\n")

        # csv_pattern = data[0].split(separator)
        #
        # print("csv pattern: {}".format(csv_pattern))
        #
        # for index in range(len(csv_pattern)):
        #     print('{}: "{}",'.format(index, csv_pattern[index]))

        n = 1
        for e in data:
            # print(e)
            source_index = data.index(e)
            print("source index: {}".format(source_index))
            if source_index in range(1,len(data)):
                # try:


                source = e.split(separator)
                if len(source) > 5:
                    # print("source: {}".format(source))

                    item = deepcopy(self.item_pattern)

                    id = source[3]
                    # print(item)

                    for i in el_dict.keys():
                        if i in range(0, 9):
                            item["01.main_data"][el_dict[i]] = self.determine_value(source[i])
                        elif i in range(9, 12):
                            item["02.location_details"][el_dict[i]] = self.determine_value(source[i])
                        elif i in range(12, 23):
                            item["03.offer_details"][el_dict[i]] = self.determine_value(source[i])
                        elif i in range(23, 35):
                            item["04.building_details"][el_dict[i]] = self.determine_value(source[i])
                        elif i in range(35, 51):
                            item["05.fitout_standard"][el_dict[i]] = self.determine_value(source[i])
                        elif i in range(51, 61):
                            item["09.metadata"][el_dict[i]] = self.determine_value(source[i])

                    print(item)
                    item["01.main_data"]["id"] = id
                    output[id] = item

                    n += 1
                    if n == max_iterations:
                        break


                # except IndexError as err:
                #     print("Exception {} at {}: {}".format(err, source_index, item))

        return output

    def determine_value(self, raw_value):
        if raw_value.lower() in ["prawda", "true"]:
            new_value = True
        elif raw_value.lower() in ["fałsz", "false"]:
            new_value = False
        else:
            new_value = raw_value

        return new_value

    def set_id(self, n, set):
        mode_value = 1000000
        set_value = 0
        n_value = n

        if set == "rm"      :   set_value = 170000
        elif set == "bj"    :   set_value = 230000
        elif set == "oc"    :   set_value = 840000
        elif set == "zhand" :   set_value = 910000

        id = mode_value + set_value + n_value
        return id

    """ debug """

    def browse_data(self, data=None, file_name=None, max_iterations=9999):
        if file_name == None:
            file_name = self.restruct_data_output_file

        if data == None:
            data = open_json_file(file_name)

        n = 0
        for e in data:
            n += 1
            print(n)
            print("{}: {}".format(e, data[e]))
            if n >= max_iterations:
                break

        return data




if __name__ == "__main__":
    c = Converter()

    c.save_combined_csv(input_file_name="datasets/st6_bug_fixed_data.json", output_file_name="datasets/st6_bug_fixed_data_conv.csv")
    # c.save_pattern_csv(input_file_name="datasets/st3_combined_data.json")

    # c.save_combined_json(input_file_name="datasets/st4_combined_data_to_merge.csv", output_file_name="datasets/st4_to_merge.json")
    # c.browse_data(file_name="datasets/st4_to_merge.json", max_iterations=120)