
def read_log():
    log_dict = {}
    with open('access_log-20230305.txt', 'r') as f:
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
            log_dict[f"{count}"] = {"ip_address": ip_address,"date": date, "time": time, "method": method, "url": url, "status_code": status_code}

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
        return [ip for ip, occurrence in ip_requests_number().items() if occurrence == max_count]
    else:
        min_count = min(ip_requests_number().values())
        return [ip for ip, occurrence in ip_requests_number().items() if occurrence == min_count]


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


def run():
    print("IP with the most number of occurrences: ", ip_find(True))
    print("IP with the least number of occurrences: ", ip_find(False))
    print("IP with longest request: ", longest_request())
    print("Requests with result code 404: ", non_existent())
    print("Dictionary of IP with it's number of occurrences: ", ip_requests_number())


if __name__ == '__main__':
    run()

