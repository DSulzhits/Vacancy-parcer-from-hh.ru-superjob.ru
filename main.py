from classes.Connector import Connector
from classes.jobs_classes import Vacancy, sorting, get_top
from classes.engine_classes import HH, SuperJob


def main():
    user_input = input("""На каком ресурсе хотите осуществить поиск:
HeadHunter нажмите 1
SuperJob нажмите 2
Выход нажмите 0\n""").lower()
    while user_input not in ["1", "2", "0"]:
        print("Введите 1 для HeadHunter, 2 для  SuperJob, 0 для выхода")
        user_input = input()
    if user_input == "0":
        print("Программа закончила работу")
        quit()
    user_prof = input("""Введите желаемую специальность\n""")
    vacancies = None
    if user_input == "1":
        hh = HH(user_prof)
        try:
            hh.get_request()
        except IndexError:
            print("Cпециальность не найдена")
            quit()
        con = Connector()
        con.connectHH()
        vacancies = con.select_HH()
        print(f"Всего вакансий ")
    elif user_input == "2":
        sj = SuperJob(user_prof)
        try:
            sj.get_request()
        except IndexError:
            print("Cпециальность не найдена")
            quit()
        con = Connector()
        con.connectSJ()
        vacancies = con.select_SJ()
    else:
        print("Благодарим, что воспользовались нашим сервисом")
        quit()
    for vacancy in vacancies:
        vacancy_class = Vacancy(vacancy['employer'], vacancy['name'], vacancy['url'], vacancy['requirement'],
                                vacancy['salary_from'], vacancy['salary_to'])
        print(vacancy_class)
    user_sort = input("\nХотите отсортировать вакансии по зарплате Y/N? ").lower()
    if user_sort == "y":
        for sort in sorting(vacancies):
            print(sort)
        try:
            user_top = int(input("""\nХотите вывести список топ вакансий? 
(Введите количество вакансий) """))
            if user_top:
                for top in get_top(vacancies, user_top):
                    print(top)
        except ValueError:
            print("Благодарим, что воспользовались нашим сервисом")
    else:
        print("Благодарим, что воспользовались нашим сервисом")


if __name__ == "__main__":
    main()
