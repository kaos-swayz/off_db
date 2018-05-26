from _main import open_json_file, save_json_file

import operator
from os import listdir
from difflib import SequenceMatcher
import jellyfish
from time import sleep

class Combiner:
    def __init__(self):
        self.combined_data_file_name = "datasets/st3_combined_data.json"

    """ COMBINING FUNCTION """

    def combine_data(self, file_name=None, save_data=True):
        if file_name == None:
            file_name = self.combined_data_file_name

        output = {}

        for file in [f for f in listdir("datasets")]:
            if "st2" in file:
                print(file)
                file_data = open_json_file("datasets/{}".format(file))
                for item in file_data:
                    output[item] = file_data[item]

        if save_data == True:
            save_json_file(file_name=file_name, content=output)

        return output

    """ MATCHING FUNCTIONS """

    def find_matching_data(self, data=None, file_name=None, save_data=True, max_iterations=9999):
        if data == None:
            data = open_json_file(self.combined_data_file_name)

        n = 0
        for item in data:
            print("***\nFinding match for: {}, id: {}".format(data[item]["01.main_data"]["name"], item))
            if self.cond_set(item=data[item], source="bj", type="lease") == True:
                print("requirements test passed")

                self.matching_procedure(operand=data[item], data=data, target_source="rm")
                self.matching_procedure(operand=data[item], data=data, target_source="oc")
                self.matching_procedure(operand=data[item], data=data, target_source="zhand")

                self.matching_procedure(operand=data[item], data=data, target_source="rm", match_method="address")
                self.matching_procedure(operand=data[item], data=data, target_source="oc", match_method="address")
                self.matching_procedure(operand=data[item], data=data, target_source="zhand", match_method="address")


            else:
                print("requirements not met")
            n += 1
            if n >= max_iterations:
                break


        if save_data == True:
            if file_name == None:
                file_name = self.combined_data_file_name
            save_json_file(file_name=file_name, content=data)

    """ matching """

    def matching_procedure(self, operand, data, target_source, match_method="names"):
        op_name = operand["01.main_data"]["name"]
        op_city = operand["02.location_details"]["city"]
        op_address = operand["02.location_details"]["address"]

        temp_results = {}

        for item in data:
            if self.cond_set(item=data[item], source=target_source, type="lease", city=op_city) == True:
                if match_method == "names":
                    item_name = data[item]["01.main_data"]["name"]
                    similarity = self.similarity(a=op_name, b=item_name, match_method=match_method)
                    if self.check_similarity(similarity=similarity) == True:
                        temp_results[item] = similarity
                elif match_method == "address":
                    item_address = data[item]["02.location_details"]["address"]
                    similarity = self.similarity(a=op_address, b=item_address, match_method=match_method)
                    if self.check_similarity(similarity=similarity) == True:
                        temp_results[item] = similarity
                else:
                    raise Exception("match method not met")

        if len(temp_results.keys()) > 0:
            # debug
            self.print_possible_matches(temp_results=temp_results, data=data, match_method=match_method)

            match, match_level = self.highest_match(temp_dict=temp_results)
            self.add_match_data(operand=operand, match=match, match_level=match_level, data=data, match_method=match_method)




    def highest_match(self, temp_dict):
        # find the record with highest match level in temp dict and then add it to
        max_id = max(temp_dict, key=(lambda key: temp_dict[key]))
        # print("max: {}, {}".format(max_id, temp_dict[max_id]["name"]))
        return (max_id, temp_dict[max_id])

    def add_match_data(self, operand, match, match_level, data, match_method):
        # print(data[match]["01.main_data"])

        if match_method == "names":
            if type(data[match]["01.main_data"]["match_level"]) == float and data[match]["01.main_data"]["match_level"] > match_level:
                pass
            else:
                operand["01.main_data"]["match_id"] = operand["01.main_data"]["id"]
                operand["01.main_data"]["match_level"] = "self"

                data[match]["01.main_data"]["match_id"] = operand["01.main_data"]["id"]
                data[match]["01.main_data"]["match_level"] = match_level
        elif match_method == "address":
            if type(data[match]["01.main_data"]["match_a_level"]) == float and data[match]["01.main_data"][
                "match_a_level"] > match_level:
                pass
            else:
                operand["01.main_data"]["match_address"] = operand["01.main_data"]["id"]
                operand["01.main_data"]["match_a_level"] = "self"

                data[match]["01.main_data"]["match_address"] = operand["01.main_data"]["id"]
                data[match]["01.main_data"]["match_a_level"] = match_level

    def city_translate(self, city_name):
        return city_name.replace("Gdańsk", "Trójmiasto").replace("Gdynia", "Trójmiasto").replace("Sopot", "Trójmiasto")


    """ similarity functions """

    def check_similarity(self, similarity, desired_similarity=0.7):
        if similarity >= desired_similarity:
            return True
        else:
            return False

    def similarity_old(self, a, b):
        phase_cleanup = lambda x: x.replace("phase","").replace("faza","").replace("Phase","").replace("Faza","").replace(" I"," 1").replace(" II"," 2").replace(" III","3").replace(" IV"," 4")

        a = phase_cleanup(a)
        b = phase_cleanup(b)

        # return SequenceMatcher(None, a, b).ratio()
        # return SequenceMatcher(None, a.replace(" ", "").replace("Business",""), b.replace(" ", "").replace("Business","")).ratio()
        return jellyfish.jaro_distance(a, b)

    def similarity(self, a, b, match_method="names"):
        if len(a) > 0 and len(b) > 0:
            a = a.lower()
            b = b.lower()
        else:
            return 0

        similarity_count = 0
        similarity_base = 0

        # list for match methods
        deconstruct_list_names = [
            'park',
            'business',
            'office',
            '-',
            'center',
            'centrum',
            '/',
            'building',
            'tower',
            'house',
            'phase',
            'point',
            'plaza',
            'biuro',
            'biurowe',
            'centre',
            'biznesu',
            'budynek',
            "i",
            "ii",
            "iii",
            "iv",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "1",
            "2",
            "3",
            "4",
            "5",
        ]
        deconstruct_list_address = [
            "Aleja",
            "ul.",
            "Street",
            "Plac",
            "Cracow",
            "Warsaw",
            "al.",
            "Al.",
            "pl.",
            "Aleje"
        ]

        if match_method == "names":
            deconstruct_list = deconstruct_list_names
        elif match_method == "address":
            deconstruct_list = deconstruct_list_address
        else:
            raise Exception("error setting match_method")

        def deconstruct(name, deconstruct_list):
            input = name.lower().split()
            name_list = []
            type_list = []

            for e in input:
                if e in deconstruct_list:
                    type_list.append(e)
                else:
                    name_list.append(e)

            name_list = " ".join(name_list)
            # print("name: {}, type: {}".format(name_list, type_list))
            return name_list, type_list

        a_own, a_type = deconstruct(a, deconstruct_list=match_method)
        b_own, b_type = deconstruct(b, deconstruct_list=match_method)

        # sequence count on own name
        def sequence_count_my(a_own, b_own, similarity_count, similarity_base):
            for i in range(len(a_own) - 1):
                seq = (a_own[i] + a_own[i + 1])
                similarity_base += 1
                if seq in b_own:
                    similarity_count += 1

            return similarity_count, similarity_base

        def sequence_count_jaro(a_own, b_own, similarity_count, similarity_base):
            similarity_count += jellyfish.jaro_distance(a_own, b_own) * len(a_own)
            similarity_base += len(a_own)

            return similarity_count, similarity_base

        if match_method == "names":
            similarity_count, similarity_base = sequence_count_my(a_own, b_own, similarity_count, similarity_base)
        elif match_method == "address":
            similarity_count, similarity_base = sequence_count_jaro(a_own, b_own, similarity_count, similarity_base)
        else:
            raise Exception("match method error")

        # seqence count on type_name
        for e in a_type:
            if e in b_type:
                similarity_count += 1
                similarity_base += 1
            else:
                similarity_base += 1

        similarity_ratio = similarity_count / similarity_base
        # print("similarity ration between '{}' and '{}' = {}".format(a, b, similarity_ratio))
        return similarity_ratio

    """ condition set """

    def cond_set(self, item, source=None, type=None, city=None):
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
                if source in item["01.main_data"]["source"]:
                    source_bool = True
                else:
                    source_bool = False

        if type != None:
            if item["01.main_data"]["type"] == type:
                type_bool = True
            else:
                type_bool = False

        if city != None:
            if item["02.location_details"]["city"] == city:
                city_bool = True
            elif city in ["Gdynia", "Gdańsk", "Sopot"] and item["02.location_details"]["city"] == "Trójmiasto":
                city_bool = True
            elif city == "Trójmiasto" and item["02.location_details"]["city"] in ["Gdynia", "Gdańsk", "Sopot"]:
                city_bool = True
            else:
                city_bool = False

        return source_bool and type_bool and city_bool == True

    """ DEBUG """

    def print_possible_matches(self, temp_results, data, match_method):
        print("possible matches for {} test:".format(match_method))
        for item in temp_results.keys():
            print("{}: {}".format(data[item]["01.main_data"]["name"], temp_results[item]))

    def browse_data(self, data=None, file_name=None, max_iterations=9999):
        if file_name == None:
            file_name = self.combined_data_file_name

        if data == None:
            data = open_json_file(file_name)

        outcome_dict = {}

        n = 0
        n1 = 0
        for e in data:

            # if True == True:
            #     print(data[e])
                # for e in data[e]['02.location_details']['address'].split():
                #     if e not in outcome_dict.keys():
                #         outcome_dict[e] = 1
                #     else:
                #         outcome_dict[e] += 1
            if data[e]['01.main_data']['source'] == "rm" and n <= max_iterations:
                print(data[e])
                n += 1

            if data[e]['01.main_data']['source'] == "zhand":
                print(data[e])
                n1 += 1


            if n1 >= max_iterations:
                break

        return outcome_dict
        # return data


if __name__ == "__main__":
    c = Combiner()

    data = c.combine_data(save_data=False)
    #
    c.find_matching_data(data=data, save_data=True)

    c.browse_data(data=data, max_iterations=10)
    # data = c.browse_data(file_name="datasets/st3_combined_data.json", max_iterations=9999)
    # for e in data.keys():
    #     if data[e] > 10:
    #         print("{} : {}".format(e, data[e]))
