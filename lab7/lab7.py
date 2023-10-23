import logging
import re
import ipaddress

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config():
    try:
        with open('lab.config', 'r', encoding='utf-8') as f:
            header = re.compile(r'\[(.*)]')
            content = re.compile(r'(.+)=(.+)')

            current_section = None
            display_section = {}
            filename = ""
            config = {}

            for line in f:
                line = line.strip()

                match = header.match(line)
                if match:
                    current_section = match.group(1)
                    config[current_section] = {}

                match = content.match(line)
                if match:
                    key, value = match.group(1), match.group(2)
                    config[current_section][key] = value

                    if current_section == "Display":
                        display_section[key] = value

                    elif current_section == "LogFile":
                        filename = value

            default_values(filename, config, display_section)
            logging.basicConfig(filename=filename, level=config['Config']['debug'])

    except FileNotFoundError:
        logger.info("File not found")
        raise SystemExit(1)

    return filename, config, display_section


def default_values(filename, config, display_section):
    if not display_section.get("lines"):
        display_section["lines"] = 5

    if display_section.get("separator"):
        display_section["separator"] = '|'

    if display_section.get("filter"):
        display_section["filter"] = "GET"

    if not filename:
        filename = "default_filename"

    if not config.get('Config'):
        config['Config']['debug'] = "info"


def read_log():
    log_dict = {}
    try:
        with open('access_log-20201025.txt', 'r') as f:
            count = 0
            for line in f:
                ip_address, timestamp, http_request, status_code, response_size, url = parse_line(line)
                log_dict[f"{count}"] = {"ip_address": ip_address, "timestamp": timestamp, "http_request": http_request,
                                        "status_code": status_code, "response_size": response_size, "url": url}
                count += 1
    except FileNotFoundError:
        logger.error("Log file with this name doesn't exist")
        raise SystemExit(1)

    try:
        assert len(log_dict.items()) > 0, "Log file is empty!"
    except AssertionError as e:
        logger.error(e)

    return log_dict


def parse_line(line):
    ip_pattern = re.compile(r"((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}")
    timestamp_pattern = re.compile(r"\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s[+-]\d{4})]")
    http_request_pattern = re.compile(r"(POST|GET)\s/(.*)\sHTTP/\d.\d")
    status_size_pattern = re.compile(r"(\d+)\s(\d+)")

    ip_address, timestamp, status_code, response_size, http_request, url = "", "", 0, 0, "", ""
    ip_address_matcher = re.search(ip_pattern, line)
    timestamp_matcher = re.search(timestamp_pattern, line)
    http_request_matcher = re.search(http_request_pattern, line)
    status_size = re.search(status_size_pattern, line)

    if ip_address_matcher:
        ip_address = ip_address_matcher.group(0)

    if timestamp_matcher:
        timestamp = timestamp_matcher.group(0)

    if http_request_matcher:
        http_request = http_request_matcher.group(0)
        url = http_request_matcher.group(2)

    if status_size:
        status_code = int(status_size.group(1))
        response_size = int(status_size.group(2))

    return ip_address, timestamp, http_request, status_code, response_size, url


def get_requests_from_ip(given_ip):
    mask_length = 267855 % 16 + 8
    subnet = ipaddress.ip_network(given_ip + '/' + str(mask_length))
    requests = []
    count = 0
    lines_to_display = int(load_config()[2]["lines"])
    for key, value in read_log().items():
        request_string = value["url"]
        curr_ip_address = ipaddress.ip_address(value["ip_address"])

        if curr_ip_address in subnet:
            print("ip_address: ", curr_ip_address, " url: \"", request_string, "\"")
            count += 1

        if count == lines_to_display:
            input("Press Enter to continue")
            count = 0

    return requests


def check_ip_in_subnet(ip, subnet):
    if ipaddress.ip_address(ip) in ipaddress.ip_network(subnet):
        return True
    else:
        return False


def get_num_of_bytes():
    defined_type = load_config()[2]["filter"]
    total_bytes = 0
    for key, value in read_log().items():
        if re.search(defined_type, value["http_request"]):
            total_bytes += int(value["response_size"])

    separator = load_config()[2]["separator"]
    print(defined_type, separator, total_bytes)


def run():
    get_num_of_bytes()
    get_requests_from_ip("193.27.228.0")


if __name__ == '__main__':
    run()
