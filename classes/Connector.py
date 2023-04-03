import json
from engine_classes import HH, SuperJob


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """

    def connectHH(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        try:
            with open("hh_ru.json", encoding='utf-8') as file:
                self.vacancies_hh = json.load(file)
        except FileNotFoundError:
            print("Файл не найден создаю новый файл")
            HH("python").get_request()

    def connectSJ(self):
        try:
            with open("sj_ru.json", encoding='utf-8') as file:
                self.vacancies_sj = json.load(file)
        except FileNotFoundError:
            print("Файл не найден создаю новый файл")
            SuperJob("python").get_request()

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        pass

    def select_HH(self):
        hh_info = []

        for vacancy in self.vacancies_hh:
            hh_info.append(vacancy)

        return hh_info

    def select_SJ(self):
        sj_info = []

        for vacancy in self.vacancies_sj:
            sj_info.append(vacancy)

        return sj_info
