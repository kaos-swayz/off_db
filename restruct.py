from _main import open_json_file, save_json_file

from copy import deepcopy
import re


class Restructor:
    def __init__(self, name_of_set):
        self.name_of_set = name_of_set
        self.raw_data = open_json_file("datasets/st1_raw_data_{}.json".format(self.name_of_set))
        self.restruct_data_output_file = "datasets/st2_restruct_data_{}.json".format(self.name_of_set)



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

        self.translate_dict_bj = {
            "Log in" : "",
            "Leased" : ""
        }


    """ basic functions """
    """ function that can be useful """

    def translate(self, result, translate_dict):
        if result in translate_dict.keys():
            result = translate_dict[result]

        return result


    def return_digit(self, e):
        # gets first digit of the string and returns rest of it
        # usefull to get rents and so on
        match = re.search("\d", e)
        if match:
            return e[match.start():]
        else:
            return ""

    def return_from_index(self, e, index):
        # returns the rest of the string basing on index input
        return e[index:]

    def return_true_if_input(self, e, input):
        for i in e:
            if type(i) == str:
                if input in i.lower():
                    # print(str(e.index(i)))
                    return True
        # print("returned - 1")
        return False

    def return_after_input(self, e, input):
        return self.return_from_index(e[self.get_index_based_on_input(e, input.lower())], len(input))

    def get_index_based_on_input(self, e, input):
        # gets the index number of
        for i in e:
            if type(i) == str:
                if input in i.lower():
                    return e.index(i)
        return -1

    """ specific functions """
    """ to get specific data based on name of set """

    """ 01.main_data """
    # item["01.main_data"]["name"]
    def s_01_name(self, e, set):
        # print(e)
        if set == "rm"  :   return e[1].replace("|", "/")
        elif set == "bj":   return e[1]
        elif set == "oc":   return e[1].strip()
        elif set == "zhand":
            return self.return_after_input(e, "Property name  ")

    # item["01.main_data"]["type"]
    def s_01_type(self, e, set):
        if set in ["rm", "bj", "oc"]  :   return self.get_type(e[1])
        elif set == "zhand":
            return self.get_type(e[0])

    def get_type(self, e):
        if "podnajem" in e.lower():
            return "sublease"
        elif "sublease" in e.lower():
            return "sublease"
        elif "serwisowane" in e.lower():
            return "servised"
        elif "wirtualne" in e.lower():
            return "virtual"
        else:
            return "lease"

    # item["01.main_data"]["source"] = ""
    def s_01_source(self, e, set):
        return set


    """ 02.location_details """
    # item["02.location_details"]["city"]
    def s_02_city(self, e, set):
        if set in ["rm", "bj"]          :   return self.get_city(e[5])
        elif set == "oc"                :   return self.get_city_oc(e[5])
        elif set == "zhand"             :   return self.return_after_input(e, "City ")
    
    def get_city(self, e):
        translation_dict = {
            'Cracow': 'Kraków',
            'Bialystok': 'Białystok',
            'Bydgoszcz': 'Bydgoszcz',
            'Nowy Sacz': 'Nowy Sącz',
            'Rzeszow': 'Rzeszów',
            'Gdansk': 'Gdańsk',
            'Poznan': 'Poznań',
            'Torun': 'Toruń',
            'Wroclaw': 'Wrocław',
            'Zielona Gora': 'Zielona Góra',
            'Lodz': 'Łódź',
            'Warsaw': 'Warszawa',
        }

        city = e[:e.find(",")]

        if city in translation_dict.keys():
            city = translation_dict[city]

        return city

    def get_city_oc(self, e):
        match = "city:"
        return e[e.find(match) + len(match):e.find("#", e.find(match) + len(match))]


    # item["02.location_details"]["district"]
    def s_02_district(self, e, set):
        if set == "rm"          :   return self.get_district_rm(e[3])
        elif set == "bj"        :   return self.get_district_bj(e[5])
        elif set == "oc"        :   return self.get_district_oc(e[5])
        elif set == "zhand"     :   return self.return_after_input(e, "District ")

    
    def get_district_rm(self, e):
        translation_dict = {
            "bemowo": "Bemowo",
            "bialoleka": "Białołęka",
            "bielany": "Bielany",
            "mokotow": "Mokotów",
            "ochota": "Ochota",
            "praga-polnoc": "Praga Północ",
            "praga-poludnie": "Praga Południe",
            "srodmiescie": "Śródmieście",
            "targowek": "Targówek",
            "ursus": "Ursus",
            "ursynow": "Ursynów",
            "wilanow": "Wilanów",
            "wlochy": "Włochy",
            "zoliborz": "Żoliborz"
        }

        if "warszawa" in e:
            dist = e.find("warszawa")
            dist = e[dist + 9:e.find("/", dist)]
            if dist in translation_dict.keys():
                dist = translation_dict[dist]
            return dist
        else:
            return ""

    def get_district_bj(self, e):
        return e[e.find(",") + 2:e.find(",", e.find(",") + 1)]

    def get_district_oc(self, e):
        match = "district:"
        return e[e.find(match) + len(match):e.find(",", e.find(match) + len(match))]

    # item["02.location_details"]["address"]
    def s_02_address(self, e, set):
        if set == "rm"          :   return self.get_address_rm(e[5])
        elif set == "bj"        :   return self.get_address_bj(e[5])
        elif set == "oc"        :   return self.get_address_oc(e[5])
        elif set == "zhand"     :   return self.return_after_input(e, "Address ")
    
    
    def get_address_rm(self, e):
        return e[e.find(",")+2:]
    
    def get_address_bj(self, e):
        # return e[e.rfind(",") + 2:]
        # print(e)
        match = re.search("\d", e)
        # print(bool(match))
        if bool(match) == True:
            raw_address = e[match.start():]
        else:
            raw_address = e
        address = ""

        if "," in raw_address:
            if "Street" in raw_address:
                number = raw_address[:raw_address.find(",")]
                name = raw_address[raw_address.find(",") + 2:]
                name = name.replace("Street", "")
                address = "ul. " + name + number
            elif "Avenue" in raw_address:
                number = raw_address[:raw_address.find(",")]
                name = raw_address[raw_address.find(",") + 2:]
                name = name.replace("Avenue", "")
                address = "Aleja " + name + " " + number
            elif "Square" in raw_address:
                number = raw_address[:raw_address.find(",")]
                name = raw_address[raw_address.find(",") + 2:]
                name = name.replace("Square", "")
                address = "Plac " + name + " " + number
        else:
            address = raw_address
        return address

    def get_address_oc(self, e):
        match = "adress:"
        return e[e.find(match) + len(match):e.find(",", e.find(match) + len(match))]

    # item["03.offer_details"] = {}
    # item["03.offer_details"]["av_office"] = ""
    def s_03_av_office(self, e, set):
        if set == "rm"          :
            return not self.return_true_if_input(e[self.get_index_based_on_input(e, "Total available office area".lower())], input=" 0 ")
        elif set == "bj"        :
            return not self.return_true_if_input(e, input="Leased".lower())
        elif set == "oc":
            return ""
        elif set == "zhand"     :    return ""
    


    # item["03.offer_details"]["av_office_vol"] = ""
    def s_03_av_office_vol(self, e, set):
        if set == "rm"          :
            return self.return_digit(e[self.get_index_based_on_input(e, "Total available office area ".lower())])
        elif set == "bj"        :
            return ""
        elif set == "oc":
            return ""
        elif set == "zhand":
            return ""


    # item["03.offer_details"]["rent_office"]
    def s_03_rent_office(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Asking rent for office space".lower())])
        elif set == "bj"        :
            return ""
        elif set == "oc"        :
            return ""
        elif set == "zhand":
            return "{}{}".format(self.return_after_input(e, "Asking rent Q2 2013 "), e[17].replace("Currency", ""))
    

    
    # item["03.offer_details"]["rent_retail"]
    def s_03_rent_retail(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Asking rent for retail space".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return ""
        elif set == "zhand"     :   return ""
        
        
        
    # item["03.offer_details"]["rent_warehouse"]
    def s_03_rent_warehouse(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Asking rent for industrial space".lower())])
        elif set == "bj"        :    return ""
        elif set == "oc"        :    return ""
        elif set == "zhand"     :    return ""
    
    
    # item["03.offer_details"]["service_charge"]
    def s_03_service_charge(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Service charge".lower())]).replace(" / month", "")
        elif set == "bj":
            return ""
        elif set == "oc":
            return ""
        elif set == "zhand":
            return "{}{}".format(self.return_after_input(e, "Service charge Q2 2013 "), e[19].replace("Currency", ""))
    
    
    # item["03.offer_details"]["cost_parking_surface"]
    def s_03_cost_parking_surface(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Surface parking rent".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return ""
        elif set == "zhand":
            return "{}{}".format(self.return_after_input(e, "naziemne parking fee "), e[22].replace("Currency", ""))

    
    # item["03.offer_details"]["cost_parking_underground"]
    def s_03_cost_parking_underground(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Underground parking rent".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return ""
        elif set == "zhand":
            return "{}{}".format(self.return_after_input(e, "podziemne parking fee "), e[22].replace("Currency", ""))
    
    
    # item["03.offer_details"]["min_space_to_let"]
    def s_03_min_space_to_let(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Minimum office space to let".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return self.return_after_input(e, "Minimalny moduł biurowy ")
        elif set == "zhand":
            return ""
    
    # item["03.offer_details"]["min_lease"]
    def s_03_min_lease(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Minimum lease term".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return self.return_after_input(e, "Minimalny okres najmu ").replace("lata", "years").replace("lat", "years").replace("rok", "year")
        elif set == "zhand":
            return ""
    
    # item["03.offer_details"]["add_on_factor"]
    def s_03_add_on_factor(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Add-on factor".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return self.return_after_input(e, "Współczynnik powierzchni wspólnych")
        elif set == "zhand":
            return self.return_after_input(e, "Add on factor ").replace("brak", "")

    #
    # item["04.building_details"]
    # item["04.building_details"]["building_status"]
    def s_04_building_status(self, e, set):
        translate_dict_status = {
            "Planowany": "Planned",
            "Istniejący": "Existing",
            "W budowie": "Under Construction",
            " cpl": "Existing",
            " pl": "Planned",
            " uc": "Under Construction"
        }

        if set == "rm":
            return self.return_from_index(e[self.get_index_based_on_input(e, "Building status".lower())], 16)
        elif set == "bj":
            return self.return_from_index(e[self.get_index_based_on_input(e, "Building status".lower())],15)
        elif set == "oc":
            return self.translate(result=self.return_after_input(e, "Status budynku"), translate_dict=translate_dict_status)
            # return self.get_matching_item(e, match="Status budynku", translate_dict=translate_dict_status)
        elif set == "zhand":
            self.translate(result=self.return_after_input(e, "Status budynku"), translate_dict=translate_dict_status)
            # return self.return_after_input(e, "Status").replace(" cpl", "Completed").replace(" pl", "Planned").replace(" uc", "Under Construction")


    # item["04.building_details"]["building_class"]
    def s_04_building_class(self, e, set):
        if set == "rm":
            return self.return_from_index(e[self.get_index_based_on_input(e, "Building class".lower())], 15)
        elif set == "bj":
            return ""
        elif set == "oc":
            return self.return_after_input(e, "Klasa budynku")
        elif set == "zhand":
            return self.return_after_input(e, "Class ")
    
    # item["04.building_details"]["total_net_space"]
    def s_04_total_net_space(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Total net office space".lower())])
        elif set == "bj":
            return self.return_digit((e[self.get_index_based_on_input(e, "Total net rentable office".lower())]).replace("m²", "m2"))
        elif set == "oc":
            return self.return_after_input(e, "Powierzchnia biurowa netto budynku")
        elif set == "zhand":
            return "{} m2".format(self.return_after_input(e, "Office rentable ").replace("m2", ""))
    
    # item["04.building_details"]["total_gross_space"]
    def s_04_total_gross_space(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Total gross office space".lower())])
        elif set == "bj":
            return self.return_digit(e[self.get_index_based_on_input(e, "Total building space".lower())]).replace("m²", "m2")
        elif set == "oc":
            return self.return_after_input(e, "Powierzchnia całkowita budynku")
        elif set == "zhand":
            return "{} m2".format(self.return_after_input(e, "Total rentable space ").replace("m2", ""))

    # item["04.building_details"]["completion_date"]
    def s_04_completion_date(self, e, set):
        if set == "rm":
            return self.return_from_index(e[self.get_index_based_on_input(e, "Building completion date".lower())], 25)
        elif set == "bj":
            return self.return_from_index(e[self.get_index_based_on_input(e, "Building completion date".lower())], 24)
        elif set == "oc":
            return self.return_after_input(e, "Rok zakończenia budowy")
        elif set == "zhand":
            return "{} {}".format(self.return_after_input(e, "Completion quater "), self.return_after_input(e, "Completion year "))

    # item["04.building_details"]["ground_floors"]
    def s_04_ground_floors(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Above-ground floors".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return self.return_after_input(e, "Liczba kondygnacji naziemnych")
        elif set == "zhand":
            return ""

    # item["04.building_details"]["underground_floors"]
    def s_04_underground_floors(self, e, set):
        if set == "rm":
            return ""
        elif set == "bj":
            return ""
        elif set == "oc":
            return self.return_after_input(e, "Liczba kondygnacji podziemnych")
        elif set == "zhand":
            return ""


    # item["04.building_details"]["floor_plate"]
    def s_04_floor_plate(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Typical floor size".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return self.return_after_input(e, "Powierzchnia typowego piętra")
        elif set == "zhand":
            return "{} m2".format(self.return_after_input(e, "Floor plate ").replace("m2", ""))

    # item["04.building_details"]["no_surface_parking"]
    def s_04_no_surface_parking(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Number of surface parking spaces".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return self.return_after_input(e, "Liczba miejsc parkingowych naziemnych")
        elif set == "zhand":
            return ""
    
    # item["04.building_details"]["no_underground_parking"]
    def s_04_no_underground_parking(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Number of underground parking spaces".lower())])
        elif set == "bj":
            return ""
        elif set == "oc":
            return self.return_after_input(e, "Liczba miejsc parkingowych podziemnych")
        elif set == "zhand":
            return ""
    
    # item["04.building_details"]["parking_ratio"]
    def s_04_parking_ratio(self, e, set):
        if set == "rm":
            return self.return_digit(e[self.get_index_based_on_input(e, "Parking ratio".lower())]).replace("place ","").replace(" of the leased space","")
        elif set == "bj":
            return self.return_digit(e[self.get_index_based_on_input(e, "Parking ratio".lower())]).replace("/", "per").replace("sq m", "m2")
        elif set == "oc":
            return self.return_after_input(e, "Współczynnik miejsc parkingowych").replace("/", " per ") + " m2"
        elif set == "zhand":
            return self.return_after_input(e, "Parking ratio ")

    # item["04.building_details"]["building_certification"] = ""
    def s_04_building_certification(self, e, set):
        if set == "rm":
            return ""
        elif set == "bj":
            return self.return_from_index(e[self.get_index_based_on_input(e, "Green building".lower())],28).replace("-","")
        elif set == "oc":
            return self.return_after_input(e, "Zielony certyfikat")
        elif set == "zhand":
            return ""
    
    
    # item["05.fitout_standard"] = {}
    # item["05.fitout_standard"]["sprinklers"]
    def s_05_sprinklers(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Smoke detectors".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Tryskacze".lower())
        elif set == "zhand":
            return ""
    
    # item["05.fitout_standard"]["access_control"]
    def s_05_access_control(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Access control".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="BMS".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["computer_cabling"]
    def s_05_computer_cabling(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Computer cabling".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Kable światłowodowe".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["switchboard"]
    def s_05_switchboard(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Telephone cabling".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Kable światłowodowe".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["smoke_detectors"]
    def s_05_smoke_detectors(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Smoke detectors".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Czujniki dymu".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["suspended_ceiling"]
    def s_05_suspended_ceiling(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Suspended ceiling".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Podwieszane sufity".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["openable_windows"]
    def s_05_openable_windows(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Openable windows".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Uchylne okna".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["partition_walls"]
    def s_05_partition_walls(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Wall partitioning".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Podnoszone podłogi".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["backup_power_supply"]
    def s_05_backup_power_supply(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Emergency power supply".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="aaaa".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["telephone_cabling"]
    def s_05_telephone_cabling(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Telephone cabling".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Kable światłowodowe".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["power_cabling"]
    def s_05_power_cabling(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Power cabling".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Kable światłowodowe".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["air_conditioning"]
    def s_05_air_conditioning(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Air conditioning".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Klimatyzacja".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["raised_floor"]
    def s_05_raised_floor(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Raised floor".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Podnoszone podłogi".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["carpeting"]
    def s_05_carpeting(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Carpeting".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["fibre_optic_connections"]
    def s_05_fibre_optic_connections(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="Fiber optics".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="Kable światłowodowe".lower())
        elif set == "zhand":
            return ""

    # item["05.fitout_standard"]["BMS"]
    def s_05_BMS(self, e, set):
        if set == "rm"  :   return True
        elif set == "bj":   return self.return_true_if_input(e, input="BMS".lower())
        elif set == "oc":   return self.return_true_if_input(e, input="BMS".lower())
        elif set == "zhand":
            return ""



    # item["09.metadata"] = {}
    # item["09.metadata"]["rm_id"]
    def s_09_rm_id(self, e, set):
        if set == "rm"  :   return e[0]
        elif set == "bj":   return ""
        elif set == "oc":   return ""
        elif set == "zhand":
            return ""

    # item["09.metadata"]["rm_url"]
    def s_09_rm_url(self, e, set):
        if set == "rm"  :   return e[4]
        elif set == "bj":   return ""
        elif set == "oc":   return ""
        elif set == "zhand":
            return ""

    # item["09.metadata"]["rm_pic_url"]
    def s_09_rm_pic_url(self, e, set):
        if set == "rm"  :   return e[4]
        elif set == "bj":   return ""
        elif set == "oc":   return ""
        elif set == "zhand":
            return ""
    

    # item["09.metadata"]["bj_id"] = ""
    def s_09_bj_id(self, e, set):
        if set == "rm"  :   return ""
        elif set == "bj":   return e[0]
        elif set == "oc":   return ""
        elif set == "zhand":
            return ""

    # item["09.metadata"]["bj_url"] = ""
    def s_09_bj_url(self, e, set):
        if set == "rm"  :   return ""
        elif set == "bj":   return e[3]
        elif set == "oc":   return ""
        elif set == "zhand":
            return ""

    # item["09.metadata"]["bj_pic_url"] = ""
    def s_09_bj_pic_url(self, e, set):
        if set == "rm"  :   return ""
        elif set == "bj":   return e[4]
        elif set == "oc":   return ""
        elif set == "zhand":
            return ""

    # item["09.metadata"]["oc_id"] = ""
    def s_09_oc_id(self, e, set):
        if set == "rm"  :   return ""
        elif set == "bj":   return ""
        elif set == "oc":   return e[0]
        elif set == "zhand":
            return ""

    # item["09.metadata"]["oc_url"] = ""
    def s_09_oc_url(self, e, set):
        if set == "rm"  :   return ""
        elif set == "bj":   return ""
        elif set == "oc":   return e[3]
        elif set == "zhand":
            return ""

    # item["09.metadata"]["oc_pic_url"] = ""
    def s_09_oc_pic_url(self, e, set):
        if set == "rm"  :   return ""
        elif set == "bj":   return ""
        elif set == "oc":   return e[4]
        elif set == "zhand":
            return ""

    # item["09.metadata"]["add_info"] = ""
    def s_09_add_info(self, e, set):
        if set == "rm"  :   return ""
        elif set == "bj":   return ""
        elif set == "oc":   return ""
        elif set == "zhand":
            return ",".join([e[i].replace('"','') for i in range(23, 32)])

    """ RESTRUCTURING DATA """
    """ main function """

    def restruct_data(self, raw_data, set, file_name=None, max_iterations=9999, save_data=True):
        output = {}

        n = 1

        for e in raw_data:
            if e is not None:
                item = deepcopy(self.item_pattern)
                # item = {}

                id = self.set_id(set=set, n=n)


                # item["01.main_data"] = {}
                item["01.main_data"]["name"] = self.s_01_name(e, set)
                item["01.main_data"]["type"] = self.s_01_type(e, set)
                item["01.main_data"]["source"] = self.s_01_source(e, set)
                item["01.main_data"]["id"] = id

                # item["02.location_details"] = {}
                item["02.location_details"]["city"] = self.s_02_city(e, set)
                item["02.location_details"]["district"] = self.s_02_district(e, set)
                item["02.location_details"]["address"] = self.s_02_address(e, set)

                # item["03.offer_details"] = {}
                item["03.offer_details"]["av_office"] = self.s_03_av_office(e, set)
                item["03.offer_details"]["av_office_vol"] = self.s_03_av_office_vol(e, set)
                item["03.offer_details"]["rent_office"] = self.s_03_rent_office(e, set)
                item["03.offer_details"]["rent_retail"] = self.s_03_rent_retail(e, set)
                item["03.offer_details"]["rent_warehouse"] = self.s_03_rent_warehouse(e, set)
                item["03.offer_details"]["service_charge"] = self.s_03_service_charge(e, set)
                item["03.offer_details"]["cost_parking_surface"] = self.s_03_cost_parking_surface(e, set)
                item["03.offer_details"]["cost_parking_underground"] = self.s_03_cost_parking_underground(e, set)
                item["03.offer_details"]["min_space_to_let"] = self.s_03_min_space_to_let(e, set)
                item["03.offer_details"]["min_lease"] = self.s_03_min_lease(e, set)
                item["03.offer_details"]["add_on_factor"] = self.s_03_add_on_factor(e, set)

                # item["04.building_details"] = {}
                item["04.building_details"]["building_status"] = self.s_04_building_status(e, set)
                item["04.building_details"]["building_class"] = self.s_04_building_class(e, set)
                item["04.building_details"]["total_net_space"] = self.s_04_total_net_space(e, set)
                item["04.building_details"]["total_gross_space"] = self.s_04_total_gross_space(e, set)
                item["04.building_details"]["completion_date"] = self.s_04_completion_date(e, set)
                item["04.building_details"]["ground_floors"] = self.s_04_ground_floors(e, set)
                item["04.building_details"]["underground_floors"] = self.s_04_underground_floors(e, set)
                item["04.building_details"]["floor_plate"] = self.s_04_floor_plate(e, set)
                item["04.building_details"]["no_surface_parking"] = self.s_04_no_surface_parking(e, set)
                item["04.building_details"]["no_underground_parking"] = self.s_04_no_underground_parking(e, set)
                item["04.building_details"]["parking_ratio"] = self.s_04_parking_ratio(e, set)
                item["04.building_details"]["building_certification"] = self.s_04_building_certification(e, set)

                # item["05.fitout_standard"] = {}
                item["05.fitout_standard"]["sprinklers"] = self.s_05_sprinklers(e, set)
                item["05.fitout_standard"]["access_control"] = self.s_05_access_control(e, set)
                item["05.fitout_standard"]["computer_cabling"] = self.s_05_computer_cabling(e, set)
                item["05.fitout_standard"]["switchboard"] = self.s_05_switchboard(e, set)
                item["05.fitout_standard"]["smoke_detectors"] = self.s_05_smoke_detectors(e, set)
                item["05.fitout_standard"]["suspended_ceiling"] = self.s_05_suspended_ceiling(e, set)
                item["05.fitout_standard"]["openable_windows"] = self.s_05_openable_windows(e, set)
                item["05.fitout_standard"]["partition_walls"] = self.s_05_partition_walls(e, set)
                item["05.fitout_standard"]["backup_power_supply"] = self.s_05_backup_power_supply(e, set)
                item["05.fitout_standard"]["telephone_cabling"] = self.s_05_telephone_cabling(e, set)
                item["05.fitout_standard"]["power_cabling"] = self.s_05_power_cabling(e, set)
                item["05.fitout_standard"]["air_conditioning"] = self.s_05_air_conditioning(e, set)
                item["05.fitout_standard"]["raised_floor"] = self.s_05_raised_floor(e, set)
                item["05.fitout_standard"]["carpeting"] = self.s_05_carpeting(e, set)
                item["05.fitout_standard"]["fibre_optic_connections"] = self.s_05_fibre_optic_connections(e, set)
                item["05.fitout_standard"]["BMS"] = self.s_05_BMS(e, set)

                translate_dict = {
                    "sprinklers": "sprinklers",
                    "access control": "access_control",
                    "computer cabling": "computer_cabling",
                    "switchboard": "switchboard",
                    "smoke/heat detectors": "smoke_detectors",
                    "suspended ceiling": "suspended_ceiling",
                    "openable windows": "openable_windows",
                    "partition walls": "partition_walls",
                    "backup power supply": "backup_power_supply",
                    "telephone cabling": "telephone_cabling",
                    "power cabling": "power_cabling",
                    "air-conditioning": "air_conditioning",
                    "raised floor": "raised_floor",
                    "carpeting": "carpeting",
                    "fibre optic connection": "fibre_optic_connections",
                    "BMS": "BMS"
                }

                if set == "rm":
                    for fitoout_e in e[-2]:
                        item["05.fitout_standard"][translate_dict[fitoout_e]] = False

                # item["09.metadata"] = {}
                item["09.metadata"]["rm_id"] = self.s_09_rm_id(e, set)
                item["09.metadata"]["rm_url"] = self.s_09_rm_url(e, set)
                item["09.metadata"]["rm_pic_url"] = self.s_09_rm_pic_url(e, set)
                item["09.metadata"]["bj_id"] = self.s_09_bj_id(e, set)
                item["09.metadata"]["bj_url"] = self.s_09_bj_url(e, set)
                item["09.metadata"]["bj_pic_url"] = self.s_09_bj_pic_url(e, set)
                item["09.metadata"]["oc_id"] = self.s_09_oc_id(e, set)
                item["09.metadata"]["oc_url"] = self.s_09_oc_url(e, set)
                item["09.metadata"]["oc_pic_url"] = self.s_09_oc_pic_url(e, set)
                item["09.metadata"]["add_info"] = self.s_09_add_info(e, set)

                output[id] = item

                n += 1
                if n == max_iterations:
                    break

        if save_data == True:
            if file_name == None:
                file_name = self.restruct_data_output_file
            save_json_file(file_name=file_name, content=output)

        return output

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
            print(data[e])
            if n >= max_iterations:
                break

        return data


if __name__ == "__main__":
    r = Restructor("rm")
    print(len(r.raw_data))
    print(r.name_of_set)

    data = r.restruct_data(raw_data=r.raw_data, set=r.name_of_set)

    r.browse_data(data=data)

