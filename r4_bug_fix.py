from _main import open_json_file, save_json_file

from re import search as re_search


class BugFixer:
    def __init__(self):
        self.bug_fixed_data_output_file = "datasets/st6_bug_fixed_data.json"


    def bug_fixing(self, input_file_name=None, outut_file_name=None, save_data=True, max_iterations=9999):
        if input_file_name == None:
            raise Exception("No input file")

        if outut_file_name == None:
            outut_file_name = self.bug_fixed_data_output_file

        data = open_json_file(input_file_name)

        data = self.fixing_completion_date_bug(data, max_iterations=max_iterations)
        data = self.fixing_parking_ratio_bug(data, max_iterations=max_iterations)
        data = self.fixing_address_bug(data, max_iterations=max_iterations)


        if save_data == True:
            save_json_file(file_name=outut_file_name, content=data)

        return data


    """ fixing completion data """

    def fixing_completion_date_bug(self, data, max_iterations=9999):

        n = 0
        for item in data:
            if data[item]['04.building_details']['completion_date']:
                completion_date = data[item]['04.building_details']['completion_date']
                print("completion_data for {}: {}".format(item, completion_date))

                if self.has_digits(completion_date) == False:
                    data[item]['04.building_details']['completion_date'] = ""
                else:
                    completion_date = "".join(completion_date.split())

                    year_range = [str(e) for e in range(2000, 2031)]

                    for year in year_range:
                        if year in completion_date:
                            leftovers = completion_date[0:completion_date.find(year)]
                            if self.has_digits(leftovers) == True:
                                new_completion_date = "0{}.{}".format(leftovers, year).strip()
                            else:
                                new_completion_date = "{} {}".format(leftovers, year).strip()
                            data[item]['04.building_details']['completion_date'] = new_completion_date
                            print(new_completion_date)

            n += 1
            if n >= max_iterations:
                break

        return data

    def has_digits(self, input):
        return bool(re_search(r'\d', input))

    """ parking ratio """

    def fixing_parking_ratio_bug(self, data, max_iterations=9999):

        n = 0
        for item in data:
            if data[item]['04.building_details']['parking_ratio']:
                parking_ratio = data[item]['04.building_details']['parking_ratio']
                # print("parking_ratio for {}: {}".format(item, parking_ratio))

                if parking_ratio == " m2":
                    print("parking_ratio for {}: {}".format(item, parking_ratio))

                    data[item]['04.building_details']['parking_ratio'] = ""


            n += 1
            if n >= max_iterations:
                break

        return data


    """  """

    def fixing_address_bug(self, data, max_iterations=9999):

        n = 0
        for item in data:
            if data[item]['02.location_details']['address']:
                address = data[item]['02.location_details']['address']
                # print("address for {}: {}".format(item, address))

                eng_names = {
                    "street" : "ul.",
                    "st.": "ul.",
                    "avenue": "Al.",
                    "square": "Plac"
                }

                for name in eng_names.keys():
                    if name in address.lower() and " / " not in address and "Kard." not in address:
                        print("address for {}: {}".format(item, address))

                        address_list = address.split()
                        new_address = "{} {} {}".format(eng_names[name], address[len(address_list[0]) + 1 : address.lower().find(name) - 1], address_list[0])

                        print("new address for {}: {}".format(item, new_address))

            n += 1
            if n >= max_iterations:
                break

        return data



    """ debug """

    def browse_data(self, data=None, file_name=None, max_iterations=9999):
        if file_name == None:
            file_name = self.bug_fixed_data_output_file

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
    bf = BugFixer()
    data = bf.bug_fixing(input_file_name="datasets/st5_merged_data.json")
    bf.browse_data(data=data, max_iterations=80)