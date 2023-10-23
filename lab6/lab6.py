import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingArgumentException(Exception):
    pass


class InvalidLogLevelException(Exception):
    pass


class InvalidLinesNumberException(Exception):
    pass


def read_log():
    log_dict = {}
    try:
        with open('access_log-20230305', 'r') as f:
            count = 0
            for line in f:
                components = line.split()
                count += 1

                ip_address = components[0]
                date = components[3][1:]
                time = components[4][:-7]
                method = components[5][1:]
                url = components[6]
                status_code = components[8]
                log_dict[f"{count}"] = {"ip_address": ip_address, "date": date, "time": time, "method": method,
                                        "url": url,
                                        "status_code": status_code}
    except FileNotFoundError:
        logger.error("Log file with this name doesn't exist")
        raise SystemExit(1)

    try:
        assert len(log_dict.items()) > 0, "Log file is empty!"
    except AssertionError as e:
        logger.error(e)

    return log_dict


def ip_requests_number():
    ip_req_num_dict = {}

    for log_id, log in read_log().items():
        ip = log["ip_address"]
        if ip in ip_req_num_dict:
            ip_req_num_dict[ip] += 1
        else:
            ip_req_num_dict[ip] = 1

    return ip_req_num_dict


def ip_find(most_active):
    if most_active:
        max_count = max(ip_requests_number().values())
        result = [ip for ip, occurrence in ip_requests_number().items() if occurrence == max_count]
    else:
        min_count = min(ip_requests_number().values())
        result = [ip for ip, occurrence in ip_requests_number().items() if occurrence == min_count]

    try:
        assert len(result) > 0, "No IP addresses found !"
    except AssertionError as e:
        logger.info(e)
    return result


def longest_request():
    length = 0

    for log_id, log in read_log().items():
        request_string = log["url"]
        curr_ip_address = log["ip_address"]

        if len(request_string) > length:
            length = len(request_string)
            ip_address = curr_ip_address
            request = request_string

    return ip_address, request


def non_existent():
    not_found = []
    for log_id, log in read_log().items():
        http_code = log["status_code"]
        request_string = log["url"]
        if http_code == "404" and request_string not in not_found:
            not_found.append(request_string)

    return not_found


def default_log():
    input_data = {"log_file": "default log", "ip_address": "192.168.1.1",
                  "logging_level": "info", "num_lines": "3", "my_param": "default parameters"}
    return input_data


def check_missing_arguments(config_settings):
    if not all(key in config_settings for key in ['log_file', 'ip_address', 'logging_level', 'num_lines', 'my_param']):
        raise MissingArgumentException


def set_logging_level():
    logging_level = load_config().get("logging_level")
    try:
        if logging_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise InvalidLogLevelException
        else:
            logger.setLevel(logging_level)
    except InvalidLogLevelException:
        logger.info('Logging level from config file is not acceptable!')


def get_requests_from_ip():
    given_ip = load_config().get("ip_address")
    requests = []
    for log_id, log in read_log().items():
        request_string = log["url"]
        curr_ip_address = log["ip_address"]

        if given_ip == curr_ip_address:
            requests.append(request_string)

    print(requests)
    return requests


def print_requests_by_pause():
    lines_to_display = int(load_config().get("num_lines"))
    method = load_config().get("my_param")
    given_ip = load_config().get("ip_address")
    requests = []

    try:
        assert lines_to_display > 0, "Number of lines can't be less than or equal to 0 \nThe default value is set to 3"
        assert method == "GET" or method == "POST", "Method is incorrect!"
    except AssertionError as e:
        logger.info(e)
        lines_to_display = 3

    for log_id, log in read_log().items():
        request_string = log["url"]
        curr_ip_address = log["ip_address"]
        log_method = log["method"]

        if given_ip == curr_ip_address and method == log_method:
            requests.append(request_string)

    i = 0
    for request in requests:
        print(request)
        i += 1
        if i == lines_to_display:
            input("Press any key to continue")
            i = 0


def get_requests_with_parameter():
    method = load_config().get("my_param")
    requests = []

    try:
        assert method == "GET" or method == "POST", "Method is incorrect!"
    except AssertionError as e:
        logger.info(e)

    for log in read_log().items():
        request_string = log["url"]
        log_method = log["method"]
        if method == log_method:
            requests.append(request_string)
    return requests


def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config_settings = json.load(f)
            check_missing_arguments(config_settings)

    except FileNotFoundError:
        logger.info("File not found")
        config_settings = default_log()

    except json.JSONDecodeError:
        logger.error("configuration file is not a correct JSON file")
        raise SystemExit(1)

    except MissingArgumentException:
        logger.info('Configuration file does not contain all values your application needs')
        config_settings = default_log()

    return config_settings


def run():
    # print("IP with the most number of occurrences: ", ip_find(True))
    # print("IP with the least number of occurrences: ", ip_find(False))
    # print("IP with longest request: ", longest_request())
    # print("Requests with result code 404: ", non_existent())
    # print("Dictionary of IP with it's number of occurrences: ", ip_requests_number())
    # load_config()
    # set_logging_level()
    get_requests_from_ip()
    # print_requests_by_pause()


if __name__ == '__main__':
    run()
