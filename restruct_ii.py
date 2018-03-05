from _main import open_json_file, save_json_file

from os import listdir
from difflib import SequenceMatcher
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
                    output_data[id]["01.main_data"]["match_id"] = ""
                    output_data[id]["01.main_data"]["match_level"] = ""
                    id += 1

        save_json_file(file_name=output_file_name, content=output_data)



    """ add new features to the dataset """


    def add_matching_data(self, input_file_name="datasets/combined_data.json", output_fle_name="datasets/combined_data_match.json"):
        data = open_json_file(input_file_name)

        n = 0
        for item in data:
            print(" *** ")
            print(data[item]["01.main_data"]["name"])

            data[item]["01.main_data"]["match_id"] = data[item]["01.main_data"]["id"]
            data[item]["01.main_data"]["match_level"] = "self"

            if data[item]["01.main_data"]["source"] == "bj" and data[item]["01.main_data"]["type"] == "lease":

                m = 0
                for com_item in data:
                    if data[com_item]["01.main_data"]["source"] != "bj":
                        similarity_level = self.similarity(data[item]["01.main_data"]["name"].replace(" ", "").replace("Business",""), data[com_item]["01.main_data"]["name"].replace(" ", "").replace("Business",""))
                        if similarity_level > 0.7:


                            if data[com_item]["01.main_data"]["match_id"] == "":
                                data[com_item]["01.main_data"]["match_id"] = data[item]["01.main_data"]["match_id"]
                                data[com_item]["01.main_data"]["match_level"] = similarity_level
                            else:
                                if data[com_item]["01.main_data"]["match_level"] < similarity_level:
                                    data[com_item]["01.main_data"]["match_id"] = data[item]["01.main_data"]["match_id"]
                                    data[com_item]["01.main_data"]["match_level"] = similarity_level
                                else:
                                    pass

                            # print(data[com_item]["01.main_data"])
                            # print(similarity_level)

                            # m += 1
                            # if m >= 5:
                            #     break
            # sleep(0.025)

        save_json_file(file_name=output_fle_name, content=data)

    # def add_match_data(self, file_name, output_file):
    #     output_data = []
    #
    #     file_data = open_json_file(file_name)
    #
    #     n = 0
    #     for item in file_data:
    #         if item["01.main_data"]["source"] == "bj":
    #
    #             item["01.main_data"]["match_id"] = item["01.main_data"]["id"]
    #
    #             print("   ***   ")
    #             print(item["01.main_data"]["name"])
    #             # output_data.append(building_record["01.main_data"]["name"])
    #
    #             for com_item in file_data:
    #                 if com_item["01.main_data"]["source"] != "bj":
    #                     similarity = self.similarity(item["01.main_data"]["name"].replace(" ", ""), com_item["01.main_data"]["name"].replace(" ", ""))
    #                     if similarity > 0.8:
    #                         if com_item["01.main_data"]["name"] != "":
    #                             if similarity > int(com_item["01.main_data"]["name"]):
    #                         else:
    #                             com_item["01.main_data"]["name"]
    #
    #                 # if com_item["01.main_data"]["source"] != "bj":
    #                 #     if self.similarity(item["01.main_data"]["name"], com_item["01.main_data"]["name"]) > 0.85:
    #                 #         print("similarity for '{}', '{}':".format(item["01.main_data"], com_item["01.main_data"]))
    #                 #         print(self.similarity(item["01.main_data"]["name"], com_item["01.main_data"]["name"]))
    #             n += 1
    #             if n == 5:
    #                 break

    def similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()


    """ debug features """

    def check_records(self, file_name, iteration_limit=5, no_of_start_rec=1, no_of_end_rec=9999):
        # uses new structure
        data = open_json_file(file_name)

        n = 0
        for key in data:
            if int(key) in range(no_of_start_rec, no_of_end_rec):
                print(data[key]['01.main_data'])
                n += 1
                if n >= iteration_limit:
                    break



if __name__ == "__main__":
    r = Restructor_ii()
    # r.save_combined_json_data()

    r.add_matching_data()

    # r.check_records(file_name="datasets/combined_data.json", no_of_start_rec=2400)

