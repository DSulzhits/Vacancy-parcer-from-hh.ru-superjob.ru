from abc import ABC, abstractmethod
import requests


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    def get_request(self):
        vacancies = []
        vacancies_dicts = []
        for num in range(1000):
            self.url = 'https://api.hh.ru/vacancies'
            params = {'text': 'python', 'per_page': 20, 'page': num}
            response = requests.get(self.url, params=params)
            info = response.json()
            if 'items' not in info:
                continue
            else:
                for vacancy in range(20):
                    vacancies.append([info['items'][vacancy]['name'], info['items'][vacancy]['apply_alternate_url'],
                                      info['items'][vacancy]['snippet']['requirement'],
                                      info['items'][vacancy]['salary']])
        for vacancy in vacancies:
            vacancy_dict = {}
            vacancy_dict['name'] = vacancy[0]
            vacancy_dict['url'] = vacancy[1]
            vacancy_dict['requirementrl'] = vacancy[2]
            vacancy_dict['salary'] = vacancy[3]
            vacancies_dicts.append(vacancy_dict)

        return vacancies_dicts


# class HH(Engine):
#     def get_request(self):
#         items = []
#
#         i: int
#         for i in range(1000):
#             url = "https://api.hh.ru/vacancies"
#             par = {
#                 'text': 'python',
#                 'areas': 113,
#                 'page': i
#             }
#             self.request = requests.get(url, params=par).json()
#             if self.request == []:
#                 continue
#             for y in range(20):
#                 items.append(self.request['items'][y]['name'])
#                 items.append(self.request['items'][y]['alternate_url'])
#                 items.append(self.request['items'][y]['snippet']['requirement'])
#                 items.append(self.request['items'][y]['salary'])
#         return items




class SuperJob(Engine):
    def get_request(self):
        pass


hh = HH()
print(hh.get_request())
print(len(hh.get_request()))
