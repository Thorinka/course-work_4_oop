import json
from abc import ABC, abstractmethod
from pprint import pprint

from src.website import SuperJobVacancies, HeadHunterVacancies, Vacancies


class OperatingFile(ABC):
    """
    Абстрактный класс для работы с файлом
    """
    @staticmethod
    @abstractmethod
    def operate_file(keyword):
        pass


class OperatingJSON(OperatingFile):
    """
    Класс для работы с JSON (наследуется от OperatingFile)
    """
    @staticmethod
    def json_exemplars(united_list: list[Vacancies]) -> list[dict]:
        """
        Метод для конвертации списка вакансий в виде списка экземпляров класса в список словарей dict
        :param united_list:
        :return:
        """
        list_dicts = []
        for a in united_list:
            list_dicts.append(a.__dict__)
        return list_dicts

    @staticmethod
    def operate_file(list_dict):
        """
        Метод для загрузки списка словарей в JSON файл
        :param list_dict:
        :return:
        """

        with open("data.json", "w+", encoding="utf-8") as file:
            json.dump(list_dict, file, ensure_ascii=False)

    @staticmethod
    def get_vacancies_by_town(town: str):
        """
        Метод для фильтрации вакансий из файла JSON по ключевому слову (город) и возвращения их обратно в файл
        :param town: город поиска вакансий
        """
        with open("data.json", "r", encoding="utf-8") as file:
            read_file = json.load(file)
            filtered_list = []
            for string in read_file:
                if string["town"] == town:
                    filtered_list.append(string)
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(filtered_list, file, ensure_ascii=False)

    @staticmethod
    def get_vacancies_by_salary(salary: str) -> list[dict]:
        """
        Метод для фильтрации вакансий из файла JSON по размеру зарплаты (минимальной) и возвращения их обратно в файл
        :param salary: минимальная желаемая зарплата
        """
        with open("data.json", "r", encoding="utf-8") as file:
            read_file = json.load(file)
            filtered_list = []
            for string in read_file:
                if string["salary"] is None:
                    continue
                elif string["salary"] >= int(salary):
                    filtered_list.append(string)
        return filtered_list

    @staticmethod
    def get_sorted_vacancies_by_salary(filtered_list: list[dict]) -> list[dict]:
        """
        Метод для сортировки вакансий по зарплате (от большего к меньшему)
        :param filtered_list: отфильтрованный список вакансий по зп
        :return: отсортированный список вакансий по зп
        """
        sorted_list = sorted(filtered_list, key=lambda x: x["salary"], reverse=True)
        return sorted_list

    @staticmethod
    def print_result_to_file(result: list[dict], quantity: str):
        """
        Метод для выгрузки вакансий в TXT-файл
        :param quantity: количество вакансий для выгрузки
        :param result: результат для выгрузки
        """
        with open("results.txt", "w", encoding="utf-8") as file:
            for index in result[:int(quantity)]:
                for k, v in index.items():
                    file.write(f"{k}: {v} \n")
                file.write("\n")

