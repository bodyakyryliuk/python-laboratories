import re

string = '152.32.65.99 - - [18/Oct/2020:00:15:28 +0200] "GET / HTTP/1.1" 301 234 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"'


http_request_pattern = re.compile(r'\(([^;)]+)[;)]')

ip = re.search(http_request_pattern, string)

print(ip)