from _main import open_json_file, save_json_file

import re



def restruct_data(data):
    output = []
    for e in data:
        item = {}

        item["01.main_data"] = {}
        item["01.main_data"]["name"] = e[1]
        item["01.main_data"]["type"] = get_type(e[1])

        item["02.location_details"] = {}
        item["02.location_details"]["city"] = get_city(e[4])
        item["02.location_details"]["district"] = get_district(e[2])
        item["02.location_details"]["address"] = get_address(e[4])

        item["03.offer_details"] = {}
        item["03.offer_details"]["rent_office"] = get_digit(e[index_by_input(e, "Asking rent for office space".lower())])
        item["03.offer_details"]["rent_retail"] = get_digit(e[index_by_input(e, "Asking rent for retail space".lower())])
        item["03.offer_details"]["rent_warehouse"] = get_digit(e[index_by_input(e, "Asking rent for industrial space".lower())])
        item["03.offer_details"]["service_charge"] = get_digit(e[index_by_input(e, "Service charge".lower())]).replace(" / month","")
        item["03.offer_details"]["cost_parking_surface"] = get_digit(e[index_by_input(e, "Surface parking rent".lower())])
        item["03.offer_details"]["cost_parking_underground"] = get_digit(e[index_by_input(e, "Underground parking rent".lower())])
        item["03.offer_details"]["min_space_to_let"] = get_digit(e[index_by_input(e, "Minimum office space to let".lower())])
        item["03.offer_details"]["min_lease"] = get_digit(e[index_by_input(e, "Minimum lease term".lower())])
        item["03.offer_details"]["add_on_factor"] = get_digit(e[index_by_input(e, "Add-on factor".lower())])

        item["04.building_details"] = {}
        item["04.building_details"]["building_status"] = get_index(e[index_by_input(e, "Building status".lower())],16)
        item["04.building_details"]["building_class"] = get_index(e[index_by_input(e, "Building class".lower())],15)
        item["04.building_details"]["total_net_space"] = get_digit(e[index_by_input(e, "Total net office space".lower())])
        item["04.building_details"]["total_gross_space"] = get_digit(e[index_by_input(e, "Total gross office space".lower())])
        item["04.building_details"]["completion_date"] = get_index(e[index_by_input(e, "Building completion date".lower())],25)
        item["04.building_details"]["ground_floors"] = get_digit(e[index_by_input(e, "Above-ground floors".lower())])
        item["04.building_details"]["floor_plate"] = get_digit(e[index_by_input(e, "Typical floor size".lower())])
        item["04.building_details"]["no_surface_parking"] = get_digit(e[index_by_input(e, "Number of surface parking spaces".lower())])
        item["04.building_details"]["no_underground_parking"] = get_digit(e[index_by_input(e, "Number of underground parking spaces".lower())])
        item["04.building_details"]["parking_ratio"] = get_digit(e[index_by_input(e, "Parking ratio".lower())]).replace("place ", "").replace(" of the leased space","")

        item["05.fitout_standard"] = {}
        item["05.fitout_standard"]["sprinklers"] = True
        item["05.fitout_standard"]["access_control"] = True
        item["05.fitout_standard"]["computer_cabling"] = True
        item["05.fitout_standard"]["switchboard"] = True
        item["05.fitout_standard"]["smoke_detectors"] = True
        item["05.fitout_standard"]["suspended_ceiling"] = True
        item["05.fitout_standard"]["openable_windows"] = True
        item["05.fitout_standard"]["partition_walls"] = True
        item["05.fitout_standard"]["backup_power_supply"] = True
        item["05.fitout_standard"]["telephone_cabling"] = True
        item["05.fitout_standard"]["power_cabling"] = True
        item["05.fitout_standard"]["air_conditioning"] = True
        item["05.fitout_standard"]["raised_floor"] = True
        item["05.fitout_standard"]["carpeting"] = True
        item["05.fitout_standard"]["fibre_optic_connections"] = True
        item["05.fitout_standard"]["BMS"] = True

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

        for fitoout_e in e[-2]:
            item["05.fitout_standard"][translate_dict[fitoout_e]] = False

        item["09.metadata"] = {}
        item["09.metadata"]["remobile_id"] = e[0]
        item["09.metadata"]["remobile_url"] = e[2]
        item["09.metadata"]["remobile_pic_url"] = e[3]


        output.append(item)
    return output


def get_type(e):
    if "podnajem" in e.lower():
        return "sublease"
    elif "sublease" in e.lower():
        return "sublease"
    else:
        return "lease"


def get_city(e):
    return e[:e.find(",")]

def get_district(e):
    if "warszawa" in e:
        loc = e.find("warszawa")
        return e[loc+9:e.find("/",loc)]
    else:
        return ""

def get_address(e):
    return e[e.find(",") + 2:]


def get_digit(e):
    # usefull to get rents and so on
    match = re.search("\d", e)
    if match:
        return e[match.start():]
    else:
        return ""

def get_index(e, index):
    return e[index:]






def index_by_input(e, input):
    # print(e)
    for i in e:
        if type(i) == str:
            if input in i.lower():
                return e.index(i)
    return -1






def check_count(data):
    len_41 = 0
    len_43 = 0
    len_inne = 0
    for e in data:
        # print(len(e))
        if len(e) == 42:
            len_41 += 1
        elif len(e) == 44:
            len_43 += 1
        else:
            len_inne += 1
            print(len(e))
            print(e)
    print("len 41: {}, lend 43: {}, inne: {}".format(len_41, len_43, len_inne))

def check_podnajem(data):
    podnajem_count = 0
    for e in data:
        if "sublease" in e[1].lower():
            podnajem_count += 1
            print(e)
        elif "podnajem" in e[1].lower():
            podnajem_count += 1
            print(e)
    print("podnajem_count: {}".format(podnajem_count))

def check_restructed_all(r_data):
    for e in r_data:
        print(e)


if __name__ == "__main__":
    data = open_json_file("raw_data_set1.txt")
    print(data[0])

    # check_count(data)
    # check_podnajem(data)

    restructed_data = restruct_data(data)
    print(len(restructed_data))

    check_restructed_all(restructed_data)