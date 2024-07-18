import json


def get_list(utm, step, utm_type):
    with open("constructs/api.json", "r") as file:
        if str(step).startswith("reminder"):
            data = json.load(file)
            data_list = data.get(utm).get(step)[0].get(utm_type)
        else:
            data = json.load(file)
            data_list = data.get(utm).get(step).get(utm_type)

        return data_list
