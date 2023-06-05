from src.website import HeadHunter, HeadHunterVacancies, SuperJobVacancies, Vacancies
from src.work_with_file import OperatingJSON
from src.user_interface import Interface


def main():
    """
    Главная функция программы
    """
    user_data: tuple = Interface.get_user_data()
    # user_data = ('Python Разработчик', '3', 'Москва', '50000', "10")
    all_vacancies: list[Vacancies] = Interface.get_platforms_data(user_data[1], user_data[0])

    vacancies_list_dict = OperatingJSON.json_exemplars(all_vacancies)
    OperatingJSON.operate_file(vacancies_list_dict)

    OperatingJSON.get_vacancies_by_town(user_data[2])
    final_data = OperatingJSON.get_vacancies_by_salary(user_data[3])

    Interface.output_data(OperatingJSON.get_sorted_vacancies_by_salary(final_data), user_data[4])
    data_to_print = OperatingJSON.get_sorted_vacancies_by_salary(final_data)
    OperatingJSON.print_result_to_file(data_to_print, user_data[4])


if __name__ == '__main__':
    main()
