import json
from abc import ABC, abstractmethod
from website import SuperJobVacancies, HeadHunterVacancies


class OperatingFile(ABC):
    @abstractmethod
    def operate_file(self, keyword):
        pass


class OperatingJSON(OperatingFile):

    @staticmethod
    def json_exemplars(keyword):
        exemplar_1 = SuperJobVacancies()
        exemplar_2 = HeadHunterVacancies()
        data_superjob = exemplar_1.load_vacancies(keyword)
        data_headhunter = exemplar_2.load_vacancies(keyword)
        united_list = data_headhunter + data_superjob
        return united_list

    @classmethod
    def operate_file(cls, keyword: str):

        with open("data.json", "a+", encoding="utf-8") as file:
            json.dump(cls.json_exemplars(keyword), file, ensure_ascii=False)



if __name__ == '__main__':
    foo = OperatingJSON()
    foo.operate_file("Python Разработчик")
