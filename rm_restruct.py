import json

import re



def open_data(file_name):
    with open(file_name, "r", encoding="UTF-8") as fp:
        data = json.loads(fp.read())

    return data

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
    data = open_data("raw_data_set1.txt")
    print(data[0])

    # check_count(data)
    # check_podnajem(data)

    restructed_data = restruct_data(data)
    print(len(restructed_data))

    check_restructed_all(restructed_data)