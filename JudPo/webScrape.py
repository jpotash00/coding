import requests
from bs4 import BeautifulSoup

url = 'https://tunebat.com/Info/Happy-Now-Kygo-Sandro-Cavazza/14sOS5L36385FJ3OL8hew4'
data = requests.get(url)

info = []

html = BeautifulSoup(data.text, 'html.parser')

with open('html.txt', 'w') as f:
    for line in html:
        print(line)
