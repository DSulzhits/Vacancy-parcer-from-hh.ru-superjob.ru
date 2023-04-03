from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os
import requests
import json


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def get_request(self):
        vacancies = []
        vacancies_dicts = []
        for num in range(1):  # при значении 50 выбирает 1000 вакансий
            url = 'https://api.hh.ru/vacancies'
            params = {'text': {self.vacancy}, "areas": 113, 'per_page': 20, 'page': num}
            response = requests.get(url, params=params)
            info = response.json()

            if info is None:
                return "Данные не получены"
            elif 'errors' in info:
                return info['errors'][0]['value']
            elif 'items' not in info:
                return "Нет вакансий"
            else:
                for vacancy in range(20):
                    if info['items'][vacancy]['salary'] is not None \
                            and info['items'][vacancy]['salary']['currency'] == "RUR":
                        vacancies.append([info['items'][vacancy]['employer']['name'],
                                          info['items'][vacancy]['name'], info['items'][vacancy]['apply_alternate_url'],
                                          info['items'][vacancy]['snippet']['requirement'],
                                          info['items'][vacancy]['salary']['from'],
                                          info['items'][vacancy]['salary']['to']])
        for vacancy in vacancies:
            vacancy_dict = {'employer': vacancy[0], 'name': vacancy[1], 'url': vacancy[2], 'requirement': vacancy[3],
                            'salary_from': vacancy[4], 'salary_to': vacancy[5]}
            if vacancy_dict['salary_from'] is None:
                vacancy_dict['salary_from'] = 0
            elif vacancy_dict['salary_to'] is None:
                vacancy_dict['salary_to'] = vacancy_dict['salary_from']
            vacancies_dicts.append(vacancy_dict)

        with open('hh_ru.json', 'w', encoding='UTF-8') as file:
            json.dump(vacancies_dicts, file, indent=2, ensure_ascii=False)
        return vacancies_dicts

        # return info


class SuperJob(Engine):

    def __init__(self, vacancy):
        self.vacancy = vacancy
        load_dotenv()
        self.api_key = os.getenv('SJ_API_KEY', 'key_error')

    def get_request(self):
        vacancies = []
        vacancies_dicts = []
        url = 'https://api.superjob.ru/2.0/vacancies/'
        for num in range(10):
            headers = {
                "X-Api-App-Id": self.api_key
            }
            params = {
                'keywords': self.vacancy,
                'page': num,
                'count': 5
            }
            response = requests.get(url, headers=headers, params=params)
            info = response.json()
            if info['objects'] is None:
                continue
            if info['objects'][0]['payment_from'] is not None and info['objects'][0]['currency'] == "rub":
                vacancies.append(
                    [info['objects'][0]['client']['title'], info['objects'][0]['profession'],
                     info['objects'][0]['link'], info['objects'][0]['candidat'],
                     info['objects'][0]['payment_from'], info['objects'][0]['payment_to']])

        for vacancy in vacancies:
            vacancy_dict = {'employer': vacancy[0], 'name': vacancy[1], 'url': vacancy[2], 'requirement': vacancy[3],
                            'salary_from': vacancy[4], 'salary_to': vacancy[5]}
            if vacancy_dict['salary_from'] is None:
                vacancy_dict['salary_from'] = 0
            elif vacancy_dict['salary_to'] == 0:
                vacancy_dict['salary_to'] = vacancy_dict['salary_from']
            vacancies_dicts.append(vacancy_dict)

        with open('sj_ru.json', 'w', encoding='UTF-8') as file:
            json.dump(vacancies_dicts, file, indent=2, ensure_ascii=False)


hh = HH("Python developer")
hh.get_request()
sj = SuperJob("Python developer")
sj.get_request()
