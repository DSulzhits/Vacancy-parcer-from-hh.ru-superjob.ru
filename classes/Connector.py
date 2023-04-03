import json
from engine_classes import HH, SuperJob


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """

    # __data_file = None
    # @property
    # def data_file(self):
    #     pass
    #
    # @data_file.setter
    # def data_file(self, value):
    #     # тут должен быть код для установки файла
    #     self.__connect()
    #
    # def __connect(self):
    #     """
    #     Проверка на существование файла с данными и
    #     создание его при необходимости
    #     Также проверить на деградацию и возбудить исключение
    #     если файл потерял актуальность в структуре данных
    #     """
    #     pass

    # def __init__(self, HH, SuperJob):
    #     self.HH = HH
    #     self.SuperJob = SuperJob

    def connect(self):
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

    def select(self):

        hh_info = []
        sj_info = []

        for vacancy in self.vacancies_hh:
            hh_info.append(vacancy)

        for vacancy in self.vacancies_sj:
            sj_info.append(vacancy)

        return hh_info, sj_info

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        pass

# if __name__ == '__main__':
#     df = Connector('df.json')
#
#     data_for_file = {'id': 1, 'title': 'tet'}
#
#     df.insert(data_for_file)
#     data_from_file = df.select(dict())
#     assert data_from_file == [data_for_file]
#
#     df.delete({'id':1})
#     data_from_file = df.select(dict())
#     assert data_from_file == []
#
# con = Connector()
# con.connect()
# hh, sj = con.select()
# print(hh)
# print(sj)
