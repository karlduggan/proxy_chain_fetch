# ProxyScrape2.py

"""
Scraping the latest update of proxy from https://spys.one/en/
creating a list of the top 6 working proxies.
Had an issue with a response 503 but found the soultion below to include the header.
https://stackoverflow.com/questions/47910854/http-503-error-while-using-python-requests-module
"""
from bs4 import BeautifulSoup as bs4
import requests
import time
import socket


def _check_port_is_open(ip, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (ip, port)
    a_socket.settimeout(3)
    result_of_check = a_socket.connect_ex(location)
    a_socket.settimeout(None)

    # if the port works then we get 0
    try:
        if result_of_check == 0:
            a_socket.close()
            return True
    except:
        a_socket.close()
        return False


def find_port(ip_list):
    working_ip_port_list = []
    # Proxy Type HTTP
    common_port = [8080, 3128, 3129, 1080,
                   4145, 8975, 1976, 999, 9090, 10101, ]
    for ip in ip_list[0]:
        for port in common_port:
            try:
                if _check_port_is_open(ip, port) == True:
                    print(ip, port)
                    working_ip_port_list.append((ip, port))
            except:
                pass
    print(">> The number of active proxies are: " +
          str(len(working_ip_port_list)))
    return working_ip_port_list


def top_proxies(array):
    top_proxies = []
    best = 100
    while len(top_proxies) < 15:
        index = 0
        for row in array:
            percent = int(row[4].replace('%', ''))
            if percent >= best:
                if row not in top_proxies:
                    top_proxies.append(row)
                    array.pop(index)
                    best = percent
            else:
                best -= 1
            index += 1
    print(">> Top Proxies Result: " + str(len(top_proxies)))
    return top_proxies


def proxy_scraper():
    tmp_proxy_list = []
    clean_proxy_list = []

    url = "https://spys.one/en/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
    r = requests.get(url, headers=headers)
    soup = bs4(r.text, features="html.parser")

    # These are the table row that need to be scraped
    arr1 = soup.find_all(class_='spy1x')
    arr2 = soup.find_all(class_='spy1xx')

    for row in arr1:
        row.find_all(class_='spy14')
        string = row.get_text('/')
        string_split = string.split('/')
        tmp_row = string_split[1:]
        # Clean up of data and add it to the proxy list
        for i in range(len(tmp_row) - 1):
            if tmp_row[i] == ' ':
                tmp_row.pop(i)
        for i in range(len(tmp_row) - 1):
            if tmp_row[i] == '-':
                tmp_row.pop(i)
        for i in range(len(tmp_row) - 1):
            if tmp_row[i] == '+':
                tmp_row.pop(i)
        tmp_proxy_list.append(tmp_row)

    for row in arr2:
        row.find_all(class_='spy14')
        string = row.get_text('/')
        string_split = string.split('/')
        tmp_row = string_split[1:]
        # Clean up of data and add it to the proxy list
        for i in range(len(tmp_row) - 1):
            if tmp_row[i] == ' ':
                tmp_row.pop(i)
        for i in range(len(tmp_row) - 1):
            if tmp_row[i] == '-':
                tmp_row.pop(i)
        for i in range(len(tmp_row) - 1):
            if tmp_row[i] == '+':
                tmp_row.pop(i)
        tmp_proxy_list.append(tmp_row)
    # print(tmp_proxy_list)
    # Now cleaning the tmp_proxy_list for any unessaray data
    for row in tmp_proxy_list:
        if len(row) == 8:
            if row[2] != 'S':
                clean_proxy_list.append(row)
    return clean_proxy_list


proxy_list = proxy_scraper()
# Get the random top 5 proxies scraped from the website.
topFive = top_proxies(proxy_list)
li = find_port(topFive)
