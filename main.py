from classes.Connector import Connector
from classes.jobs_classes import Vacancy, HHVacancy, SJVacancy, sorting, get_top
from classes.engine_classes import HH, SuperJob


def main():
    user_input = input("""На каком ресурсе хотите осуществить поиск:
    HeadHunter нажмите 1
    SuperJob нажмите 2\n""").lower()
    user_prof = input("""Введите желаемую специальность\n""")
    if user_input == "1":
        hh = HH(user_prof)
        hh.get_request()
        con = Connector()
        con.connectHH()
        con_hh = con.select_HH()












if __name__ == "__main__":
    main()
