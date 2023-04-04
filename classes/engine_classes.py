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
    """Класс для доступа к API HeadHunter"""
    vacancies_all = []
    vacancies = []
    vacancies_dicts = []

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def get_request(self):
        """Метод для отправки запроса на HeadHunter проводит необходимые проверки,
        записывает полученную информацию в .json файл,
        возвращает словари для последующей работы с ними.
        """

        for num in range(
                50):  # при значении 50 выбирает из 1000 вакансий те в которых есть информация о З/П и она в RUR
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
                    self.vacancies_all.append(
                        vacancy)  # добавлено для проверки количества полученных вакансий до отбора
                    if info['items'][vacancy]['salary'] is not None \
                            and info['items'][vacancy]['salary']['currency'] == "RUR":
                        self.vacancies.append([info['items'][vacancy]['employer']['name'],
                                               info['items'][vacancy]['name'],
                                               info['items'][vacancy]['apply_alternate_url'],
                                               info['items'][vacancy]['snippet']['requirement'],
                                               info['items'][vacancy]['salary']['from'],
                                               info['items'][vacancy]['salary']['to']])
        for vacancy in self.vacancies:
            vacancy_dict = {'employer': vacancy[0], 'name': vacancy[1], 'url': vacancy[2], 'requirement': vacancy[3],
                            'salary_from': vacancy[4], 'salary_to': vacancy[5]}
            if vacancy_dict['salary_from'] is None:
                vacancy_dict['salary_from'] = 0
            elif vacancy_dict['salary_to'] is None:
                vacancy_dict['salary_to'] = vacancy_dict['salary_from']
            self.vacancies_dicts.append(vacancy_dict)

        with open(f'{self.vacancy}_hh_ru.json', 'w', encoding='UTF-8') as file:
            json.dump(self.vacancies_dicts, file, indent=2, ensure_ascii=False)
        print(f"Отбор осуществляется из {len(self.vacancies_all)} вакансий (проверка обращения к сервису)")
        return self.vacancies_dicts


class SuperJob(Engine):
    """Метод для отправки запроса на SuperJob проводит необходимые проверки,
    записывает полученную информацию в .json файл,
    возвращает словари для последующей работы с ними.
    """
    vacancies = []
    vacancies_dicts = []

    def __init__(self, vacancy):
        self.vacancy = vacancy
        load_dotenv()
        self.api_key = os.getenv('SJ_API_KEY', 'key_error')

    def get_request(self):
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': os.getenv('SJ_API_KEY'),
        }

        params = {
            'keywords': f'{self.vacancy}',
            'per_page': 100,
            'area': 113,
            'page': 0}

        while len(self.vacancies) <= 50:  # указание необходимого количества вакансий в поиске
            response = requests.get(url, headers=headers, params=params)
            response_decode = response.content.decode()
            response.close()
            data = json.loads(response_decode)
            vacancies = data['objects']
            for vacancy in vacancies:
                if vacancy['payment_from'] != 0 and vacancy['payment_to'] != 0 and vacancy['currency'] == 'rub':
                    try:
                        self.vacancies.append(
                            [vacancy['client']['title'], vacancy['profession'],
                             vacancy['link'], vacancy['candidat'],
                             vacancy['payment_from'], vacancy['payment_to']])
                    except KeyError:
                        continue
            params['page'] += 1
        for vacancy in self.vacancies:
            vacancy_dict = {'employer': vacancy[0], 'name': vacancy[1], 'url': vacancy[2], 'requirement': vacancy[3],
                            'salary_from': vacancy[4], 'salary_to': vacancy[5]}
            if vacancy_dict['salary_to'] == 0:
                vacancy_dict['salary_to'] = vacancy_dict['salary_from']
            self.vacancies_dicts.append(vacancy_dict)
        with open(f'{self.vacancy}_sj_ru.json', 'w', encoding='UTF-8') as file:
            json.dump(self.vacancies_dicts, file, indent=2, ensure_ascii=False)

        return self.vacancies_dicts

        # for num in range(500):
        #     headers = {
        #         "X-Api-App-Id": self.api_key
        #     }
        #     params = {
        #         'keywords': self.vacancy,
        #         'page': num,
        #         'count': 1
        #     }
        #     response = requests.get(url, headers=headers, params=params)
        #     info = response.json()
        #     self.vacancies_all.append(info)
        #     if info['objects'] is None:
        #         continue
        #     if info['objects'][0]['payment_from'] is not None and info['objects'][0]['currency'] == "rub":
        #         self.vacancies.append(
        #             [info['objects'][0]['client']['title'], info['objects'][0]['profession'],
        #              info['objects'][0]['link'], info['objects'][0]['candidat'],
        #              info['objects'][0]['payment_from'], info['objects'][0]['payment_to']])
        #
        # for vacancy in self.vacancies:
        #     vacancy_dict = {'employer': vacancy[0], 'name': vacancy[1], 'url': vacancy[2], 'requirement': vacancy[3],
        #                     'salary_from': vacancy[4], 'salary_to': vacancy[5]}
        #     if vacancy_dict['salary_from'] is None:
        #         vacancy_dict['salary_from'] = 0
        #     elif vacancy_dict['salary_to'] == 0:
        #         vacancy_dict['salary_to'] = vacancy_dict['salary_from']
        #     self.vacancies_dicts.append(vacancy_dict)
        #
        # with open(f'{self.vacancy}_sj_ru.json', 'w', encoding='UTF-8') as file:
        #     json.dump(self.vacancies_dicts, file, indent=2, ensure_ascii=False)
        # print(f"Отбор осуществляется из {len(self.vacancies_all)} вакансий (проверка обращения к сервису)")
        # return self.vacancies_dicts
