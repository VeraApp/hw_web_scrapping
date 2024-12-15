import requests
import bs4
import json

def writefile(parsed_data):
    with open('result.json', 'w') as file:
        json.dump(parsed_data, file)

def main():
    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

    payload = {}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Referer': 'https://github.com/netology-code/py-homeworks-advanced/tree/new_hw_scrapping/6.Web-scrapping'
    }

    keywords = ["Django", "Flask"]
    main_response = requests.request("GET", url, headers=headers, data=payload)
    main_html = main_response.text
    main_soup = bs4.BeautifulSoup(main_html, features="lxml")

    vacancies = main_soup.find( class_='vacancy-serp-content')
    vacancies_tags = vacancies.find_all(class_='magritte-redesign')
    parsed_date = []
    for vacancie_tag in vacancies_tags:
        h2_tag = vacancie_tag.find("h2", class_="bloko-header-section-2")
        a_tag = h2_tag.find("a")
        vacancie_link = a_tag["href"]

        company_tag = vacancie_tag.find(class_="magritte-text___pbpft_3-0-19 magritte-text_style-primary___AQ7MW_3-0-19 magritte-text_typography-label-3-regular___Nhtlp_3-0-19")
        company = company_tag.text.strip()

        vacancie_response = requests.request("GET", vacancie_link, headers=headers, data=payload)
        vacancie_html = vacancie_response.text
        vacancie_soup = bs4.BeautifulSoup(vacancie_html, features="lxml")

        city_tag = vacancie_soup.find(class_="bloko-gap bloko-gap_bottom")
        city_time = city_tag.find("p", class_="vacancy-creation-time-redesigned").text

        if 'Москв' in city_time:
            city = 'Москва'
        elif 'Сакнкт-Петерб' in city_time:
            city = 'Санкт-Петербург'

        salary_tag = vacancie_soup.find(class_="magritte-text___pbpft_3-0-19 magritte-text_style-primary___AQ7MW_3-0-19 magritte-text_typography-paragraph-2-regular___VO638_3-0-19")
        if salary_tag:
            salary = salary_tag.text.strip()
        else:
            salary = "ЗП не указана"

        description_tag = vacancie_soup.find(class_='g-user-content')
        if description_tag:
            description = description_tag.text
        else:
            description = "Описание не указано"
        if any(keyword.lower() in description.lower() for keyword in keywords):
            vacancy_info = {
                'link': vacancie_link,
                'salary': salary,
                'company': company,
                'city': city

            }
            parsed_date.append(vacancy_info)
    writefile(parsed_date)

main()