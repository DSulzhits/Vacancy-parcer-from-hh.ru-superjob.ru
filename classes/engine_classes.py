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
            print(info)
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
        for num in range(1):
            headers = {
                "X-Api-App-Id": self.api_key
            }
            params = {
                'keywords': self.vacancy,
                'page': num,
                'count': 1
            }
            response = requests.get(url, headers=headers, params=params)
            info = response.json()
            if info['objects'][0]['payment_from'] is not None and info['objects'][0]['currency'] == "rub":
                vacancies.append(
                    [info['objects'][0]['client']['title'], info['objects'][0]['profession'],
                     info['objects'][0]['link'], info['objects'][0]['candidat'],
                     info['objects'][0]['payment_from'], info['objects'][0]['payment_to']])

        for vacancy in vacancies:
            vacancy_dict = {'employer': vacancy[0], 'name': vacancy[1], 'url': vacancy[2], 'requirement': vacancy[3],
                            'salary_from': vacancy[4], 'salary_to': vacancy[5]}
            vacancies_dicts.append(vacancy_dict)

        with open('sj_ru.json', 'w', encoding='UTF-8') as file:
            json.dump(vacancies_dicts, file, indent=2, ensure_ascii=False)


# {'objects': [
#     {'canEdit': False, 'is_closed': False, 'id': 46060205, 'id_client': 4446329, 'payment_from': 60000, 'payment_to': 0,
#      'date_pub_to': 1682771631, 'date_archived': 0, 'date_published': 1680266031,
#      'address': 'Свердловская область, Екатеринбург, Родонитовая улица, 18Б', 'profession': 'Математик-программист',
#      'work': None, 'compensation': None,
#      'candidat': 'В перспективный стартап ищем в команду программиста-математика для исследования и разработки математических алгоритмов в области нейро-нечетких сетей (neuro-fuzzy networks) для задач управления инженерным оборудованием. \nОбязанности:\n\n• Моделирование математических алгоритмов адаптивного управления в Matlab ANFIS.\n• Разработка ПО на языке Python для встраиваемых систем для процессора Allwinner.\n• Изучение различных моделей нейронных сетей Мамдами, Сугено и пр.\n• Изучение научных статей на английском языке.\nТребования:\n• Отличное знание Matlab ANFIS.\n• Опыт разработки ПО на Python.\nУсловия:\n• \nОфициальное трудоустройство, официальные условия по оплате, соблюдение гарантий ТК РФ на полный рабочий день или удаленно совместительство, трудовой договор. \n\n• \nЗаработная плата достойного уровня по результатам собеседования (оклад+ премии за результативную работу).\n\n• \nВозможность работы по совместительству.\n• \nВозможность работы на удаленке. \n• \nКомфортный офис в ботаническом районе г. Екатеринбурга.',
#      'metro': [], 'currency': 'rub',
#      'vacancyRichText': '<p>В перспективный стартап ищем в команду программиста-математика для исследования и разработки математических алгоритмов в области нейро-нечетких сетей (neuro-fuzzy networks) для задач управления инженерным оборудованием. </p><p><b>Обязанности:</b><br /></p><ul><li>Моделирование математических алгоритмов адаптивного управления в Matlab ANFIS.</li><li>Разработка ПО на языке Python для встраиваемых систем для процессора Allwinner.</li><li>\nИзучение различных моделей нейронных сетей Мамдами, Сугено и пр.</li><li>Изучение научных статей на английском языке.</li></ul><b>Требования:</b><ul><li>Отличное знание Matlab ANFIS.</li><li>Опыт разработки ПО на Python.</li></ul><b>Условия:</b><ul><li><p>Официальное трудоустройство, официальные условия по оплате, соблюдение гарантий ТК РФ на полный рабочий день или удаленно совместительство, трудовой договор. <br /></p></li><li><p>Заработная плата достойного уровня по результатам собеседования  (оклад+ премии за результативную работу).<br /></p></li><li><p>Возможность работы по совместительству.</p></li><li><p>Возможность работы на удаленке. </p></li><li><p>Комфортный офис в ботаническом районе г. Екатеринбурга.</p></li></ul><p><br /></p>',
#      'covid_vaccination_requirement': {'id': 1, 'title': 'Не важно'}, 'moveable': True, 'agreement': False,
#      'anonymous': False, 'is_archive': False, 'is_storage': False,
#      'type_of_work': {'id': 10, 'title': 'Неполный рабочий день'},
#      'place_of_work': {'id': 2, 'title': 'Удалённая работа (на дому)'}, 'education': {'id': 2, 'title': 'Высшее'},
#      'experience': {'id': 2, 'title': 'От 1 года'}, 'maritalstatus': {'id': 0, 'title': 'Не имеет значения'},
#      'children': {'id': 0, 'title': 'Не имеет значения'}, 'client': {'id': 4446329, 'title': 'ДАВТЕХ',
#                                                                      'link': 'https://www.superjob.ru/clients/davteh-4446329/vacancies.html',
#                                                                      'industry': [],
#                                                                      'description': 'Программное обеспечение',
#                                                                      'vacancy_count': 2, 'staff_count': 'менее 50',
#                                                                      'client_logo': None, 'address': None,
#                                                                      'addresses': [], 'url': 'http://www.3divi.com',
#                                                                      'short_reg': False, 'is_blocked': False,
#                                                                      'registered_date': 1678941676,
#                                                                      'town': {'id': 33, 'title': 'Екатеринбург',
#                                                                               'declension': 'в Екатеринбурге',
#                                                                               'hasMetro': True,
#                                                                               'genitive': 'Екатеринбурга'}},
#      'languages': [], 'driving_licence': [], 'catalogues': [
#         {'id': 33, 'title': 'IT, Интернет, связь, телеком', 'key': 33,
#          'positions': [{'id': 48, 'title': 'Разработка, программирование', 'key': 48},
#                        {'id': 503, 'title': 'Внедрение и сопровождение ПО', 'key': 503}]},
#         {'id': 270, 'title': 'Наука, образование, повышение квалификации', 'key': 270,
#          'positions': [{'id': 273, 'title': 'Внешкольное образование', 'key': 273},
#                        {'id': 278, 'title': 'НИИ, КБ', 'key': 278},
#                        {'id': 281, 'title': 'Среднее специальное образование', 'key': 281}]}],
#      'agency': {'id': 1, 'title': 'прямой работодатель'},
#      'town': {'id': 33, 'title': 'Екатеринбург', 'declension': 'в Екатеринбурге', 'hasMetro': True,
#               'genitive': 'Екатеринбурга'}, 'already_sent_on_vacancy': False, 'rejected': False, 'response_info': [],
#      'phone': '+7 (903) 08634XX', 'phones': [{'number': '790308634XX', 'additionalNumber': None}], 'fax': None,
#      'faxes': None, 'client_logo': None, 'highlight': False, 'age_from': 0, 'age_to': 0,
#      'gender': {'id': 0, 'title': 'Не имеет значения'}, 'firm_name': 'ДАВТЕХ',
#      'firm_activity': 'Программное обеспечение',
#      'link': 'https://ekaterinburg.superjob.ru/vakansii/matematik-programmist-46060205.html', 'latitude': 56.792233,
#      'longitude': 60.623974}], 'total': 2365, 'more': True, 'subscription_id': 0, 'subscription_active': False}

hh = HH("Python разработчик")
hh.get_request()
sj = SuperJob("Python разработчик")
# print(sj.api_key)
sj.get_request()

# {'items': [{'id': '78473911', 'premium': False, 'name': 'Разработчик Python', 'department': None, 'has_test': False,
#             'response_letter_required': False,
#             'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'},
#             'salary': {'from': 200000, 'to': 250000, 'currency': 'RUR', 'gross': False},
#             'type': {'id': 'open', 'name': 'Открытая'}, 'address': {'city': 'Москва',
#                                                                     'street': 'Западный административный округ, Можайский район, Инновационный центр Сколково, Большой бульвар',
#                                                                     'building': '42с1', 'lat': 55.692318,
#                                                                     'lng': 37.347485, 'description': None,
#                                                                     'raw': 'Москва, Западный административный округ, Можайский район, Инновационный центр Сколково, Большой бульвар, 42с1',
#                                                                     'metro': None, 'metro_stations': [],
#                                                                     'id': '12747719'}, 'response_url': None,
#             'sort_point_distance': None, 'published_at': '2023-04-01T18:26:21+0300',
#             'created_at': '2023-04-01T18:26:21+0300', 'archived': False,
#             'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=78473911',
#             'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/78473911?host=hh.ru',
#             'adv_response_url': None, 'alternate_url': 'https://hh.ru/vacancy/78473911', 'relations': [],
#             'employer': {'id': '9580359', 'name': 'Нетопия', 'url': 'https://api.hh.ru/employers/9580359',
#                          'alternate_url': 'https://hh.ru/employer/9580359',
#                          'logo_urls': {'original': 'https://hhcdn.ru/employer-logo-original/1058924.png',
#                                        '90': 'https://hhcdn.ru/employer-logo/5856337.png',
#                                        '240': 'https://hhcdn.ru/employer-logo/5856338.png'},
#                          'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=9580359', 'trusted': True},
