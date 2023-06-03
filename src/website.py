import json
from abc import ABC, abstractmethod
from pprint import pprint

import requests


class Website(ABC):

    @abstractmethod
    def get_vacancies(self, page: int, keyword: str):
        pass


class HeadHunter(Website):
    params = []

    def get_vacancies(self, page: int, keyword: str):
        params = {
            "text": keyword,
            "page": page,
            "per_page": 100
        }
        response = requests.get("https://api.hh.ru/vacancies", params=params)
        response.close()
        return response.content

    def json_vacancies(self, keyword: str):
        js_list = []

        for page in range(0, 20):
            js_obj = json.loads(self.get_vacancies(page, keyword))
            js_list.extend(js_obj['items'])
            if js_obj['pages'] - page <= 1:
                break
        return js_list


class SuperJob(Website):
    API = "v3.r.137581409.57abcbb029118ca90d805beaf6f5a56a99325625.130bce891e059b0dbc588320ddc041f34547d097"

    def __init__(self):
        pass

    def get_vacancies(self, page: int, keyword: str):
        header = {
            "Host": "api.superjob.ru",
            "X-Api-App-Id": SuperJob.API,
            "Authorization": "Bearer r.000000010000001.example.access_token",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
            "keyword": keyword,
            "town ": "",
            "count": "100",
            "period": "3",
            "page": page
        }
        response = requests.get("https://api.superjob.ru/2.0/vacancies/", params=params, headers=header)
        response.close()
        return response.content

    def json_vacancies(self, keyword: str):
        js_list = []

        for page in range(0, 20):
            js_obj = json.loads(self.get_vacancies(page, keyword))
            js_list.extend(js_obj["objects"])
        return js_list


class Vacancies:
    def __init__(self, name=None, salary=None, salary_to=None, salary_currency=None,
                 town=None, experience=None, url=None):
        self.name = name
        self.salary = salary
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.town = town
        self.experience = experience
        self.url = url

    def __repr__(self):
        return (f"Vacancy(name={self.name}, salary={self.salary}, salary_to={self.salary_to}, "
                f"salary_currency={self.salary_currency}, town={self.town},"
                f"experience={self.experience}, url={self.url}")

    def __str__(self):
        return (f"Вакансия: {self.name}. Зарплата от {self.salary} до {self.salary_to} {self.salary_currency}. "
                f"Город/страна: {self.town}"
                f"Ссылка на вакансию: {self.url}"
                f"Опыт работы:{self.experience}")

    def __ge__(self, other):
        return int(self.salary) >= int(other.salary)

    def __gt__(self, other):
        return int(self.salary) > int(other.salary)

    def __le__(self, other):
        return int(self.salary) <= int(other.salary)

    def __lt__(self, other):
        return int(self.salary) < int(other.salary)

    def __eq__(self, other):
        return int(self.salary) == int(other.salary)


class SuperJobVacancies(Vacancies, SuperJob):
    def load_vacancies(self, keyword: str):
        list_vacancies = []
        for vacancy in SuperJob.json_vacancies(self, keyword):
            new_vacancy = SuperJobVacancies(name=vacancy["profession"],
                                            salary=vacancy["payment_from"],
                                            salary_to=vacancy["payment_to"],
                                            salary_currency=vacancy["currency"],
                                            town=vacancy["town"]["title"],
                                            experience=vacancy["experience"]["title"],
                                            url=vacancy["link"])
            list_vacancies.append(new_vacancy)

        return list_vacancies


class HeadHunterVacancies(Vacancies, HeadHunter):
    def load_vacancies(self, keyword: str):
        list_vacancies = []
        for vacancy in HeadHunter.json_vacancies(self, keyword):
            try:
                new_vacancy = HeadHunterVacancies(name=vacancy["name"],
                                                  salary=vacancy["salary"]["from"],
                                                  salary_to=vacancy["salary"]["to"],
                                                  salary_currency=vacancy["salary"]["currency"],
                                                  town=vacancy["area"]["name"],
                                                  experience=vacancy["experience"]["name"],
                                                  url=vacancy["url"])
                list_vacancies.append(new_vacancy)
            except TypeError:
                new_vacancy = HeadHunterVacancies(name=vacancy["name"],
                                                  salary=None,
                                                  town=vacancy["area"]["name"],
                                                  experience=vacancy["experience"]["name"],
                                                  url=vacancy["url"])
                list_vacancies.append(new_vacancy)

        return list_vacancies


if __name__ == '__main__':
    foo = SuperJobVacancies()
    pprint(foo.load_vacancies("Python Разработчик"))
