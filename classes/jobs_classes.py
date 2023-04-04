from classes.Connector import Connector


class Vacancy:
    __slots__ = ('employer', 'name', 'url', 'requirement', 'salary_from', 'salary_to')

    def __init__(self, employer=None, name=None, url=None, requirement=None, salary_from=None, salary_to=None):
        self.employer = employer
        self.name = name
        self.url = url
        self.requirement = requirement
        try:
            if "<highlighttext>" and "</highlighttext>" in self.requirement:
                self.requirement = self.requirement.replace("<highlighttext>", "")
                self.requirement = self.requirement.replace("</highlighttext>", "")
        except TypeError:
            self.requirement = requirement
        self.salary_from = salary_from
        self.salary_to = salary_to

    def __str__(self):
        return f"""
        Наниматель: {self.employer}
        Вакансия: {self.name}
        Описание/Требования: {self.requirement}
        Заработная плата от {self.salary_from}, до {self.salary_to}
        Ссылка на вакансию: {self.url}"""


class CountMixin:

    @property
    def get_count_of_vacancy_HH(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        hh = Connector().select_HH()
        return len(hh)

    @property
    def get_count_of_vacancy_SJ(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        sj = Connector().select_SJ()
        return len(sj)


# class HHVacancy(CountMixin, Vacancy):  # add counter mixin
#     """ HeadHunter Vacancy """
#
#     def get_count_of_vacancy_HH(self):
#         return super().get_count_of_vacancy_HH
#
#     def __str__(self):
#         return f'HH: {self.employer}, зарплата от {self.salary_from}, до {self.salary_to} руб/мес'
#
#
# class SJVacancy(CountMixin, Vacancy):  # add counter mixin
#     """ SuperJob Vacancy """
#
#     def get_count_of_vacancy_SJ(self):
#         return super().get_count_of_vacancy_SJ
#
#     def __str__(self):
#         return f'SJ: {self.employer}, зарплата от {self.salary_from}, до {self.salary_to} руб/мес'


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    vacancies_list = []
    vacancies_sort = sorted(vacancies, key=lambda vacancy: vacancy["salary_from"], reverse=True)
    for vacancy in vacancies_sort:
        vacancies_list.append(f"""
        Наниматель: {vacancy['employer']}
        Вакансия: {vacancy['name']}
        Описание/Требования: {vacancy['requirement']}
        Заработная плата от {vacancy['salary_from']}, до {vacancy['salary_to']}
        Ссылка на вакансию: {vacancy['url']}""")
    return vacancies_list


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    top_list = []
    vacancies_sort = sorted(vacancies, key=lambda vacancy: vacancy["salary_from"], reverse=True)
    top_vacancies = vacancies_sort[0:top_count]
    for vacancy in top_vacancies:
        top_list.append(f"""
          Наниматель: {vacancy['employer']}
          Вакансия: {vacancy['name']}
          Описание/Требования: {vacancy['requirement']}
          Заработная плата от {vacancy['salary_from']}, до {vacancy['salary_to']}
          Ссылка на вакансию: {vacancy['url']}""")
    return top_list
