#!/usr/bin/python3
# Get keenetic info telnet
# Used for Zabbix Scripts
# parametr 2 == command desc or link or SSID
# parametr 1 == ip


from scrapli.driver import GenericDriver
from scrapli.exceptions import ScrapliException
import re
import sys

MY_DEVICE = {
    "host": "0",
    "auth_username": "user",
    "auth_password": "passwd",
    "auth_strict_key": False,
    "transport": "telnet",
    "port": 23,
}

MY_DEVICE["host"] = str(sys.argv[1])


def send_show(comm):
    try:
        with GenericDriver(**MY_DEVICE, timeout_socket=10, ) as conn:
            result = conn.send_command("show interface WifiMaster0/WifiStation0")
            output = re.search(comm, str(result.result))
            if output is None:
                return output
            else:
                return output.group()
    except ScrapliException as error:
        return str(error) + ' ' + MY_DEVICE["host"] + '\n'
    except Exception as err:
        return f"Unexpected {err=}, {type(err)=}+ '\n'"


if sys.argv[2] == "desk":
    print(send_show(r'description: (.*)'))

if sys.argv[2] == "link":
    print(send_show(r'link: (.*)'))

if sys.argv[2] == "SSID":
    print(send_show(r'SSID: (.*)'))
