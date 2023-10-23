# IPAddress library documentation: https://docs.python.org/3/library/ipaddress.html
# DateTime https://docs.python.org/3/library/datetime.html

from datetime import datetime

class Line_object:
    def __init__(self, ip, date, path, http_code, bytes_sent, processing_time):
        self.ip = ip
        self.date = date
        self.path = path
        self.http_code = http_code
        self.bytes_sent = bytes_sent
        self.processing_time = processing_time

    def get_ip(self):
        return self.ip

    def get_date(self):
        return self.date

    def get_path(self):
        return self.path

    def get_http_code(self):
        return self.http_code

    def get_bytes_sent(self):
        return self.bytes_sent

    def get_processing_time(self):
        return self.processing_time

    def __str__(self):
        return f"IP: {self.ip}, date: {self.date}, path: {self.path}, HTTP result code: {self.http_code}, " \
               f"bytes sent: {self.bytes_sent}, processing time: {self.processing_time}"


def read_file():
    file = open("access_log_lab4.log", 'r')
    content = file.read()
    lines = content.split('\n')
    return lines


def create_log_entry_object(line):
    entries = line.split(' ')

    line_object_instance = Line_object(entries[0], entries[1], entries[2], entries[3], entries[4], entries[5])
    print(line_object_instance)


def get_log_entries():
    splited_lines = []
    for line in read_file():
        splited_lines.append(line.split(' '))

    for i in range(len(splited_lines)):
        set_datetime_object(splited_lines[i][1])

    return splited_lines


def set_datetime_object(line):
    day, month_abr, year_time = line.split('/')
    year, hour, minute, second = str(year_time).split(':')
    month = datetime.strptime(month_abr, "%b").month
    datetime_object = datetime(int(year), month, int(day), int(hour), int(minute), int(second))

    return datetime_object


def display_requests(start_moment, end_moment):
    if end_moment < start_moment:
        print("End moment can't be earlier than start moment")
        return

    for entry in get_log_entries():
        request_time = set_datetime_object(entry[1])
        if start_moment < request_time < end_moment:
            print(entry)


start_time = datetime.strptime("18/Oct/2020:04:11:00", "%d/%b/%Y:%H:%M:%S")
end_time = datetime.strptime("18/Oct/2020:05:00:00", "%d/%b/%Y:%H:%M:%S")
display_requests(start_time, end_time)

#create_log_entry_object(read_file()[0])

