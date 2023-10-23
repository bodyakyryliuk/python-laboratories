import json


def get_user_input():
    log_file = input("Enter the name of the web server log file: ")
    ip_address = input("Enter the IP address to filter by: ")
    logging_level = input("Enter the logging level to use: ")
    num_lines = input("Enter the number of lines to display at once: ")
    my_param = input("Enter your own parameter: ")

    input_data = {"log_file": log_file, "ip_address": ip_address,
                  "logging_level": logging_level, "num_lines": num_lines, "my_param": my_param}
    return input_data


def convert_to_json():
    user_input = get_user_input()
    data = {
        "log_file": user_input["log_file"],
        "ip_address": user_input["ip_address"],
        "logging_level": user_input["logging_level"],
        "num_lines": user_input["num_lines"],
        "my_param": user_input["my_param"]
    }

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    return json


def read_json():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = convert_to_json().load(f)

    print(config)

read_json()