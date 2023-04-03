import json


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

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        pass

    def select(self):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """

        HH_info = []
        SJ_info = []
        with open("hh_ru.json", encoding='utf-8') as file:
            vacancies = json.load(file)
            for vacancy in vacancies:
                HH_info.append([vacancy['name'], vacancy['url'], vacancy['requirement'], vacancy['salary_from'],
                                vacancy['salary_to']])

        with open("sj_ru.json", encoding='utf-8') as file:
            vacancies = json.load(file)
            for vacancy in vacancies:
                SJ_info.append([vacancy['name'], vacancy['url'], vacancy['requirement'], vacancy['salary_from'],
                                vacancy['salary_to']])

        return HH_info, SJ_info

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

con = Connector()
print(con.select())
