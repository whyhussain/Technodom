import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://zakup.kbtu.kz/zakupki/sposobom-zaprosa-cenovyh-predlozheniy/"

parse_data = dict

answer = list()


def bs(content):
    soup = BeautifulSoup(content, 'html.parser')

    card_list = soup.find_all('div', {'class': 'card'})
    ans_list = list()
    for card in card_list:
        for card_item in card.find_all('div', class_='card-body'):
            ans_list.append(card_item.find('span').text.strip())
            ans_list.append(" ".join(card_item.find('p', class_='card-text').text.strip().split()[:4]))
            ans_list.append(" ".join(card_item.find('p', class_='card-text').text.strip().split()[5:]))
    answer.append(ans_list)
    return soup


def get_data_from_page(url):
    content = requests.get(BASE_URL + url).text
    soup = bs(content)


def get_data(content):
    soup = bs(content)
    pages_hrefs = [i.get('href') for i in soup.findAll("div", class_="row")[6].find_all("a", class_="btn btn-light")]
    for page_url in pages_hrefs:
        get_data_from_page(page_url)
    return answer


def main():
    response = requests.get(BASE_URL)
    l = get_data(response.text)
    with open('kbtu.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in l:
            print(i)
            writer.writerow(i)


if __name__ == '__main__':
    main()