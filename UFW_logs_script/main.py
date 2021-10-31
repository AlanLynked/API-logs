import os
import time
import re
import csv


class Date:
    """
    We're using Date objects since we don't have year in a date format. So it's easier to use mew simple class
    with __lt__ method than standard modules e.g. time and datetime
    Restrictions: this way it will work within one month only
    """
    def __init__(self, day, hour, minute, second):
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __lt__(self, other):
        return (self.day * 86400 + self.hour * 3600 + self.minute * 60 + self.second <
                other.day * 86400 + other.hour * 3600 + other.minute * 60 + other.second)


# Regular expressions for extracting data from files
DATE_REGEX = r'(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|' \
             r'Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}'
IP_REGEX = r'(SRC=)(\S*)'
PORT_REGEX = r'(DPT=)(\S*)'

LOW_TIME_BOUNDARY = Date(day=6, hour=9, minute=0, second=0)
HIGH_TIME_BOUNDARY = Date(day=7, hour=9, minute=0, second=0)

dict_ips = {}
dict_ports = {}

file1_path = os.path.join('logs', 'ubuntu-s-1vcpu-1gb-dbl1-01.ufw.log')
file2_path = os.path.join('logs', 'ubuntu-s-1vcpu-1gb-dbl1-01.ufw.log.1')

with open(file1_path, 'r') as file1:
    lines1 = file1.readlines()
with open(file2_path, 'r') as file2:
    lines2 = file2.readlines()

lines_all = lines1 + lines2

# Search for ports and IPs within given time interval
for line in lines_all:
    date = re.search(DATE_REGEX, line)
    ip = re.search(IP_REGEX, line)
    port = re.search(PORT_REGEX, line)
    struct_time = time.strptime(date.group(0), '%b %d %H:%M:%S')
    # Create Date object from string with registered event
    time_from_string = Date(day=struct_time.tm_mday,
                            hour=struct_time.tm_hour,
                            minute=struct_time.tm_min,
                            second=struct_time.tm_sec)
    if LOW_TIME_BOUNDARY < time_from_string < HIGH_TIME_BOUNDARY:
        try:
            dict_ips[ip.group(2)] += 1
        except KeyError:
            dict_ips[ip.group(2)] = 1
    try:
        dict_ports[port.group(2)] += 1
    except KeyError:
        dict_ports[port.group(2)] = 1

twenty_ip = [['IP', 'COUNT']]
twenty_port = [['PORT', 'COUNT']]

"""
Searching for the biggest value in dictionaries and keeping it on according list
Removing from original dictionaries. Repeat 20 times.
"""
for _ in range(20):
    ip_maxvalue_key = max(dict_ips, key=dict_ips.get)
    port_maxvalue_key = max(dict_ports, key=dict_ports.get)
    twenty_ip.append([ip_maxvalue_key, dict_ips.pop(ip_maxvalue_key)])
    twenty_port.append([port_maxvalue_key, dict_ports.pop(port_maxvalue_key)])

with open('out_ip.csv', 'w', newline='') as out_ip:
    writer = csv.writer(out_ip)
    writer.writerows(twenty_ip)
with open('out_port.csv', 'w', newline='') as out_port:
    writer = csv.writer(out_port)
    writer.writerows(twenty_port)
