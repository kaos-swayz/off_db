import json

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
        item["01.main_data"]["type"] = get_sublease(e[1])

        item["09.metadata"] = {}
        item["09.metadata"]["remobile_id"] = e[0]
        item["09.metadata"]["remobile_url"] = e[2]
        item["09.metadata"]["remobile_pic_url"] = e[3]

        # raw version
        item["02.location_details"] = {}
        item["02.location_details"]["city"] = e[4]
        item["02.location_details"]["district"] = e[2]
        item["02.location_details"]["city"] = e[4]


        output.append(item)
    return output

def get_sublease(e):
    if "podnajem" in e:
        return "sublease"
    elif "Podnajem" in e:
        return "sublease"
    else:
        return "lease"



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