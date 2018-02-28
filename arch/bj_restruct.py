from _main import open_json_file, save_json_file

import re



def restruct_data_bj(data):
    output = []


    for e in data:
        # print(e)

        try:
            item = {}

            item["01.main_data"] = {}
            item["01.main_data"]["name"] = e[1]
            item["01.main_data"]["type"] = get_type(e[1])

            item["02.location_details"] = {}
            item["02.location_details"]["city"] = get_city(e[4])
            item["02.location_details"]["district"] = get_district(e[4])
            item["02.location_details"]["address"] = get_address(e[4])

            item["03.offer_details"] = {}
            item["03.offer_details"]["rent_office"] = get_index(e[index_by_input(e, "Availability".lower())],12).replace("Log in", "")
            item["03.offer_details"]["rent_retail"] = get_index(e[index_by_input(e, "Availability".lower())],12).replace("Log in", "")
            item["03.offer_details"]["rent_warehouse"] = get_index(e[index_by_input(e, "Availability".lower())],12).replace("Log in", "")
            item["03.offer_details"]["service_charge"] = get_index(e[index_by_input(e, "Availability".lower())],12).replace("Log in", "")
            item["03.offer_details"]["cost_parking_surface"] = get_index(e[index_by_input(e, "Availability".lower())],12).replace("Log in", "")
            item["03.offer_details"]["cost_parking_underground"] = get_index(e[index_by_input(e, "Availability".lower())],12).replace("Log in", "")
            item["03.offer_details"]["min_space_to_let"] = get_index(e[index_by_input(e, "Availability".lower())],12).replace("Log in", "")
            item["03.offer_details"]["min_lease"] = get_index(e[index_by_input(e, "Availability".lower())],12).replace("Log in", "")
            item["03.offer_details"]["add_on_factor"] = get_index(e[index_by_input(e, "Availability".lower())],12).replace("Log in", "")

            item["04.building_details"] = {}
            item["04.building_details"]["building_status"] = get_index(e[index_by_input(e, "Building status".lower())],15)
            item["04.building_details"]["building_class"] = ""
            item["04.building_details"]["total_net_space"] = get_digit(e[index_by_input(e, "Total net rentable office".lower())]).replace("m²", "m2")
            item["04.building_details"]["total_gross_space"] = get_digit(e[index_by_input(e, "Total building space".lower())]).replace("m²", "m2")
            item["04.building_details"]["completion_date"] = get_index(e[index_by_input(e, "Building completion date".lower())],24)
            item["04.building_details"]["ground_floors"] = ""
            item["04.building_details"]["floor_plate"] = ""
            item["04.building_details"]["no_surface_parking"] = ""
            item["04.building_details"]["no_underground_parking"] = ""
            item["04.building_details"]["parking_ratio"] = get_digit(e[index_by_input(e, "Parking ratio".lower())]).replace("/", "per").replace("sq m", "m2")
            item["04.building_details"]["building_certification"] =  get_index(e[index_by_input(e, "Green building".lower())],28).replace("-","")

            item["05.fitout_standard"] = {}
            item["05.fitout_standard"]["sprinklers"] = true_if_input(e, "Smoke detectors".lower())
            item["05.fitout_standard"]["access_control"] = true_if_input(e, "Access control".lower())
            item["05.fitout_standard"]["computer_cabling"] = true_if_input(e, "Computer cabling".lower())
            item["05.fitout_standard"]["switchboard"] = true_if_input(e, "Telephone cabling".lower())
            item["05.fitout_standard"]["smoke_detectors"] = true_if_input(e, "Smoke detectors".lower())
            item["05.fitout_standard"]["suspended_ceiling"] = true_if_input(e, "Suspended ceiling".lower())
            item["05.fitout_standard"]["openable_windows"] = true_if_input(e, "Openable windows".lower())
            item["05.fitout_standard"]["partition_walls"] = true_if_input(e, "Wall partitioning".lower())
            item["05.fitout_standard"]["backup_power_supply"] = true_if_input(e, "Emergency power supply".lower())
            item["05.fitout_standard"]["telephone_cabling"] = true_if_input(e, "Telephone cabling".lower())
            item["05.fitout_standard"]["power_cabling"] =  true_if_input(e, "Power cabling".lower())
            item["05.fitout_standard"]["air_conditioning"] = true_if_input(e, "Air conditioning".lower())
            item["05.fitout_standard"]["raised_floor"] = true_if_input(e, "Raised floor".lower())
            item["05.fitout_standard"]["carpeting"] = true_if_input(e, "Carpeting".lower())
            item["05.fitout_standard"]["fibre_optic_connections"] = true_if_input(e, "Fiber optics".lower())
            item["05.fitout_standard"]["BMS"] = true_if_input(e, "BMS".lower())
            #
            # translate_dict = {
            #     "sprinklers": "sprinklers",
            #     "access control": "access_control",
            #     "computer cabling": "computer_cabling",
            #     "switchboard": "switchboard",
            #     "smoke/heat detectors": "smoke_detectors",
            #     "suspended ceiling": "suspended_ceiling",
            #     "openable windows": "openable_windows",
            #     "partition walls": "partition_walls",
            #     "backup power supply": "backup_power_supply",
            #     "telephone cabling": "telephone_cabling",
            #     "power cabling": "power_cabling",
            #     "air-conditioning": "air_conditioning",
            #     "raised floor": "raised_floor",
            #     "carpeting": "carpeting",
            #     "fibre optic connection": "fibre_optic_connections",
            #     "BMS": "BMS"
            # }
            #
            # for fitoout_e in e[-2]:
            #     item["05.fitout_standard"][translate_dict[fitoout_e]] = False
            #
            item["09.metadata"] = {}
            item["09.metadata"]["bj_id"] = e[0]
            item["09.metadata"]["bj_url"] = e[2]
            item["09.metadata"]["bj_pic_url"] = e[3]
            item["09.metadata"]["rc_id"] = ""
            item["09.metadata"]["rc_url"] = ""
            item["09.metadata"]["rc_pic_url"] = ""


            output.append(item)
        except:
            print("error: {}")

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
    # if "warszawa" in e:
    #     loc = e.find("warszawa")
    #     return e[loc+9:e.find("/",loc)]
    # else:
    #     return ""
    return e[e.find(",") + 2:e.find(",", e.find(",") + 1)]

def get_address(e):
    # return e[e.rfind(",") + 2:]
    match = re.search("\d", e)
    raw_address = e[match.start():]

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
    else:
        address = raw_address
    return address

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
                # print(str(e.index(i)))
                return e.index(i)
    # print("returned - 1")
    return -1

def true_if_input(e, input):
    for i in e:
        if type(i) == str:
            if input in i.lower():
                # print(str(e.index(i)))
                return True
    # print("returned - 1")
    return False




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
            # print(len(e))
            # print(e)
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


def save_csv_file(file_name, content):
    output = []
    # pattern = []
    # for dict in content[0]:
    #     for key in content[0][dict]:
    #         pattern.append(key)
    # output.append(";".join(pattern))

    for list in content:
        single_item = []
        for dict in list:
            # print(list[dict].values())
            for key in list[dict]:
                single_item.append(str(list[dict][key]))
        single_item.append("\n")
        output.append(";".join(single_item))
        # print("".join(single_item))
    with open(file_name, "w", encoding="UTF8") as f:
        f.write("".join(output))
    print("saved to file: {}".format(file_name))




if __name__ == "__main__":
    data = open_json_file("raw_data_set_dominanta.json")
    print(data[0])

    check_count(data)
    check_podnajem(data)

    restructed_data = restruct_data_bj(data)

    check_restructed_all(restructed_data)
    print(len(restructed_data))




    # save_json_file("final_data_set1b.json", restructed_data)
    # save_csv_file("final_data_set_dominanta.csv",restructed_data)