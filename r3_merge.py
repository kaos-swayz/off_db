from _main import open_json_file, save_json_file

from time import sleep
from copy import deepcopy
from os import listdir
from difflib import SequenceMatcher

class Merger:
    def __init__(self):
        self.merged_data_output_file = "datasets/st5_merged_data.json"

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




    def merge_data(self, input_file_name=None, outut_file_name=None, save_data=True, max_iterations=9999):
        if input_file_name == None:
            raise Exception("No input file")

        if outut_file_name == None:
            outut_file_name = self.merged_data_output_file

        data = open_json_file(input_file_name)

        output = self.merging_function(data, max_iterations=max_iterations)

        if save_data == True:
            save_json_file(file_name=outut_file_name, content=output)

        return output


    def merging_function(self, data, max_iterations=9999):
        output = {}
        fake_output = []

        skip_list = []

        n = 0
        for item in data:
            temp_list = []

            new_item = deepcopy(self.item_pattern)
            id = self.set_new_id(n)
            # print("before update: {}".format(new_item))

            if item not in skip_list:
                if data[item]["01.main_data"]["match_rating"] == "to merge":
                    if data[item]["01.main_data"]["id"] == data[item]["01.main_data"]["match_id"]:
                        temp_list.append(data[item])
                        skip_list.append(item)

                        for item2 in data:
                            if item2 not in skip_list:
                                if item == data[item2]["01.main_data"]["match_id"]:
                                    temp_list.append(data[item2])
                                    skip_list.append(item2)

                else:
                    temp_list.append(data[item])
                    skip_list.append(item)

                print("temp_list len: {}".format(len(temp_list)))
                print("temp_list: {}".format(temp_list))
                fake_output.append(temp_list)

                source_list = []
                merged_ids_list = []

                for item in reversed(temp_list):
                    for section in item:
                        for key in item[section]:
                            if key == "source":
                                source_list.append(item[section][key])
                            elif key == "id":
                                merged_ids_list.append(item[section][key])
                            elif section == "05.fitout_standard" and "rm" in source_list and item["01.main_data"]["source"] != "rm":
                                pass
                            elif item[section][key] != "":
                                new_item[section][key] = item[section][key]
                    new_item["01.main_data"]["id"] = id
                    new_item["01.main_data"]["source"] = " ".join(reversed(source_list))
                    new_item["01.main_data"]["match_id"] = " ".join(reversed(merged_ids_list))
                # print("after update: {}".format(new_item))

                output[id] = new_item

            n += 1
            if n >= max_iterations:
                break

        return output





    def set_new_id(self, n):
        mode_value = 2000000
        set_value = 0
        n_value = n

        id = mode_value + set_value + n_value
        return id

    """ debug """

    def browse_data(self, data=None, file_name=None, max_iterations=9999):
        if file_name == None:
            file_name = self.merged_data_output_file

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
    m = Merger()
    merged_data = m.merge_data(input_file_name="datasets/st4_to_merge.json")
    # m.browse_data(data=merged_data)