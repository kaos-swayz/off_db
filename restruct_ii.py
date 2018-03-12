from _main import open_json_file, save_json_file

from os import listdir
from difflib import SequenceMatcher
import jellyfish
from time import sleep

class Restructor_ii:
    def __init__(self):
        pass


    """ combining data """

    def save_combined_json_data(self):
        # new structure
        output_file_name = "datasets/combined_data.json"
        output_data = {}

        id = 1
        for file in [f for f in listdir("datasets")]:
            if "final" in file:
                file_data = open_json_file("datasets/{}".format(file))
                for item in file_data:
                    output_data[id] = item
                    output_data[id]["01.main_data"]["id"] = id
                    self.corrections_matching_data(output_data[id])
                    self.corrections_unify_city(output_data[id])
                    id += 1

        save_json_file(file_name=output_file_name, content=output_data)



    """ add new features to the dataset """

    def corrections_matching_data(self, item):
        item["01.main_data"]["match_id"] = ""
        item["01.main_data"]["match_level"] = ""

    def corrections_unify_city(self, item):
        translation_dict = {
            "Bialystok"     : "Białystok",
            "Cracow"        : "Kraków",
            "Gdansk"        : "Gdańsk" ,
            "Lodz"          : "Łódź",
            "Nowy Sacz"     : "Nowy Sącz",
            "Poznan"        : "Poznań",
            "Rzeszow"       : "Rzeszów",
            "Torun"         : "Toruń",
            "Warsaw"        : "Warszawa",
            "Wroclaw"       : "Wrocław",
            "Zielona Gora"  : "Zielona Góra"
        }
        if item["02.location_details"]["city"] in translation_dict.keys():
            item["02.location_details"]["city"] = translation_dict[item["02.location_details"]["city"]]


    def add_matching_data(self, input_file_name="datasets/combined_data.json", output_fle_name="datasets/combined_data_match.json"):
        data = open_json_file(input_file_name)

        self.add_matching_data_procedure(data=data, base_source="bj", target_source="rm", similarity_level_goal=0.75, sleep_val=False)

        self.add_matching_data_procedure(data=data, base_source="bj", target_source="zhand", similarity_level_goal=0.75, sleep_val=False)

        save_json_file(file_name=output_fle_name, content=data)



    """ matching data functions """

    def add_matching_data_procedure(self, data, base_source, target_source, similarity_level_goal, sleep_val=False):
        print("Starting matching data procedure for:\nBase source: {}\nTarget source".format(base_source, target_source))

        for item in data:
            print("***\nFinding match for: {}, id: {}".format(data[item]["01.main_data"]["name"], item))

            if self.cond_set(item=data[item], source=base_source, type="lease") == True:

                data[item]["01.main_data"]["match_id"] = data[item]["01.main_data"]["id"]
                data[item]["01.main_data"]["match_level"] = "self"

                temp_dict = {}

                for comp_item in data:
                    if self.cond_set(data[comp_item], comp_item=data[item], source=target_source, type="lease", city=True) == True:

                        similarity_level = self.similarity(data[item]["01.main_data"]["name"], data[comp_item]["01.main_data"]["name"])

                        if similarity_level > similarity_level_goal:
                            self.store_in_temp_dict(temp_dict, comp_item=data[comp_item], item=data[item], similarity_level=similarity_level)

                self.debug_print_temp_dict(temp_dict=temp_dict)

                self.retrieve_from_temp_dict(temp_dict=temp_dict, data=data)

            if sleep_val == True:
                #sleep for debug purposes
                sleep(0.25)

    def similarity(self, a, b):
        phase_cleanup = lambda x: x.replace("phase","").replace("faza","").replace("Phase","").replace("Faza","").replace(" I"," 1").replace(" II"," 2").replace(" III","3").replace(" IV"," 4")

        a = phase_cleanup(a)
        b = phase_cleanup(b)

        # return SequenceMatcher(None, a, b).ratio()
        # return SequenceMatcher(None, a.replace(" ", "").replace("Business",""), b.replace(" ", "").replace("Business","")).ratio()
        return jellyfish.jaro_distance(a, b)

    def cond_set(self, item, comp_item=None, source=None, type=None, city=False):
        source_bool = True
        type_bool = True
        city_bool = True
        if source != None:
            if isinstance(source, list):
                if item["01.main_data"]["source"] in source:
                    source_bool = True
                else:
                    source_bool = False
            elif isinstance(source, str):
                if item["01.main_data"]["source"] == source:
                    source_bool = True
                else:
                    source_bool = False
        if type != None:
            if item["01.main_data"]["type"] == type:
                type_bool = True
            else:
                type_bool = False
        if city == True:
            if item["02.location_details"]["city"] == comp_item["02.location_details"]["city"]:
                city_bool = True
            else:
                city_bool = False
        return source_bool and type_bool and city_bool == True

    def store_in_temp_dict(self, temp_dict, item, comp_item, similarity_level):
        temp_dict[comp_item["01.main_data"]["id"]] = {}
        temp_dict[comp_item["01.main_data"]["id"]]["name"] = comp_item["01.main_data"]["name"]
        temp_dict[comp_item["01.main_data"]["id"]]["id"] = comp_item["01.main_data"]["id"]
        temp_dict[comp_item["01.main_data"]["id"]]["match_id"] = item["01.main_data"]["id"]
        temp_dict[comp_item["01.main_data"]["id"]]["match_level"] = similarity_level
        
    def retrieve_from_temp_dict(self, temp_dict, data):
        data_override = False
        if len(temp_dict.keys()) > 0:
            max_id = self.highest_match(temp_dict=temp_dict)
            if data[str(max_id)]["01.main_data"]["match_id"] != "":
                match_data1 = float(temp_dict[max_id]["match_level"])
                match_data2 = float(data[str(max_id)]["01.main_data"]["match_level"])
                if match_data1 > match_data2:
                    self.add_highest_match(data=data, temp_dict=temp_dict, max_id=max_id)
                    data_override = True
                else:
                    reason = "not enough match level: {} to {}".format(match_data1, match_data2)
                    pass
            else:
                self.add_highest_match(data=data, temp_dict=temp_dict, max_id=max_id)
                data_override = True
        else:
            reason = "no data to override with."

        if data_override == True:
            print("Data overriden on: {}".format(data[str(max_id)]["01.main_data"]))
        else:
            print("No data were overriden: {}".format(reason))

    def highest_match(self, temp_dict):
        # find the record with highest match level in temp dict and then add it to 
        max_id = max(temp_dict, key=(lambda key: temp_dict[key]["match_level"]))
        # print("max: {}, {}".format(max_id, temp_dict[max_id]["name"]))
        return max_id
        
    def add_highest_match(self, data, temp_dict, max_id):
        data[str(max_id)]["01.main_data"]["match_id"] = temp_dict[max_id]["match_id"]
        data[str(max_id)]["01.main_data"]["match_level"] = temp_dict[max_id]["match_level"]

        # print(data[str(max_id)]["01.main_data"])
        # pass

    def debug_print_temp_dict(self, temp_dict):
        print("Data found:")
        for e in temp_dict:
            print("{} : {}".format(e, temp_dict[e]))



    """ debug features """

    def check_records(self, file_name, iteration_limit=5, no_of_start_rec=1, no_of_end_rec=9999):
        # uses new structure
        data = open_json_file(file_name)

        n = 0
        for key in data:
            if int(key) in range(no_of_start_rec, no_of_end_rec):
                print(data[key])
                n += 1
                if n >= iteration_limit:
                    break



if __name__ == "__main__":
    r = Restructor_ii()
    # r.save_combined_json_data()

    r.add_matching_data()

    # r.check_records(file_name="datasets/combined_data.json", no_of_start_rec=1)

