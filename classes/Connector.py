import json
from classes.engine_classes import HH, SuperJob


class Connector:
    """Класс коннектор для доступа к файлу в .json"""

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def connectHH(self):
        """
        Проверка на существование файла от HeadHunter с данными и
        создание его при необходимости
        """
        try:
            with open(f'{self.vacancy}_hh_ru.json', encoding='utf-8') as file:
                self.vacancies_hh = json.load(file)
        except FileNotFoundError:
            print("Файл не найден создаю новый файл")
            self.vacancies_hh = HH(self.vacancy).get_request()

    def connectSJ(self):
        """
         Проверка на существование файла от SuperJob с данными и
         создание его при необходимости
         """
        try:
            with open(f'{self.vacancy}_sj_ru.json', encoding='utf-8') as file:
                self.vacancies_sj = json.load(file)
        except FileNotFoundError:
            print("Файл не найден создаю новый файл")
            self.vacancies_sj = SuperJob(self.vacancy).get_request()

    def select_HH(self):
        """Изменяет созданный файл для последующей его обработки в main"""
        hh_info = []

        for vacancy in self.vacancies_hh:
            hh_info.append(vacancy)

        return hh_info

    def select_SJ(self):
        """Изменяет созданный файл для последующей его обработки в main"""
        sj_info = []

        for vacancy in self.vacancies_sj:
            sj_info.append(vacancy)

        return sj_info
