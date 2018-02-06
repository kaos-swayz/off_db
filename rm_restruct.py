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
        item["03.offer_details"]["rent_office"] = get_digit(e[index_rent_off(e)])



        item["09.metadata"] = {}
        item["09.metadata"]["remobile_id"] = e[0]
        item["09.metadata"]["remobile_url"] = e[2]
        item["09.metadata"]["remobile_pic_url"] = e[3]


        output.append(item)
    return output


def get_type(e):
    if "podnajem" in e:
        return "sublease"
    elif "Podnajem" in e:
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
        return "to be confirmed"








def index_rent_off(e):
    # print(e)
    for i in e:
        if type(i) == str:
            if "czynsz wyjściowy za pow. biurową" in i.lower():
                return e.index(i)






def check_count(data):
    len_41 = 0
    len_43 = 0
    len_inne = 0
    for e in data:
        # print(len(e))
        if len(e) == 41:
            len_41 += 1
        elif len(e) == 43:
            len_43 += 1
        else:
            len_inne += 1
            print(len(e))
            print(e)
    print("len 41: {}, lend 43: {}, inne: {}".format(len_41, len_43, len_inne))

def check_podnajem(data):
    podnajem_count = 0
    for e in data:
        if "podnajem" in e[1]:
            podnajem_count += 1
            print(e)
    print("podnajem_count: {}".format(podnajem_count))

def check_restructed_all(r_data):
    for e in r_data:
        print(e)


if __name__ == "__main__":
    data = open_data("raw_data.txt")
    print(data[0])

    # check_count(data)
    # check_podnajem(data)

    restructed_data = restruct_data(data)
    print(len(restructed_data))

    check_restructed_all(restructed_data)