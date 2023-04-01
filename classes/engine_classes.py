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
                    vacancies.append([info['items'][vacancy]['name'], info['items'][vacancy]['apply_alternate_url'],
                                      info['items'][vacancy]['snippet']['requirement'],
                                      info['items'][vacancy]['salary']])
        for vacancy in vacancies:
            vacancy_dict = {'name': vacancy[0], 'url': vacancy[1], 'requirement': vacancy[2], 'salary': vacancy[3]}
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
        pass


# hh = HH("Python разработчик")
# print(hh.get_request())
sj = SuperJob("Python разработчик")
print(sj.api_key)
print(os.getenv("SJ_API_KEY"))