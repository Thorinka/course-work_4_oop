from src.website import Vacancies, HeadHunterVacancies, SuperJobVacancies


class Interface:
    @staticmethod
    def get_user_data():
        """
        Получение от пользователя информации:
        vacancy - название вакансии
        platform - платформа
        city - город
        salary - зарплата
        quantity - количество вакансий для отображения
        :return: tuple(vacancy, platform, city, salary, quantity)
        """
        print("Привет!")
        while True:
            vacancy = input("Введите название вакансии: ")
            if vacancy.isdigit():
                print("Введите вакансию корректно")
                continue
            else:
                break
        while True:
            platform = input("Введите площадку: \n"
                             "1 - HeadHunter \n"
                             "2 - SuperJob \n"
                             "3 - HeadHunter и Superjob: ")
            if platform not in "123":
                print("Введите цифру от 1 до 3")
                continue
            else:
                break
        while True:
            city = input("Введите город/населённый пункт: ")
            if city.isdigit():
                print("Введите корректное название города")
                continue
            else:
                break
        while True:
            salary = input("Введите минимальный желаемый оклад: ")
            if salary.isalpha():
                print("Введите корректное значение з/п")
                continue
            else:
                break
        while True:
            quantity = input("Введите желаемое количество вакансий для отображения (макс. 50): ")
            if quantity.isalpha():
                print("Введите корректное значение")
            elif int(quantity) > 50:
                print("Значение не должно быть больше 50")
            else:
                break
        print("Обработка данных. Результат также будет записан в файле results.txt")
        return vacancy, platform, city, salary, quantity

    @staticmethod
    def output_data(list_of_vacancies: list[dict], quantity: str):
        """
        Выдаёт список подходящих вакансий (лучшие 10)
        :param quantity: количество вакансий
        :param list_of_vacancies: полный список вакансий, подходящий под параметры, заданные пользователем
        """
        print("Список подходящих вакансий: \n")
        for vacancy in list_of_vacancies[:int(quantity)]:
            print(f"Наименование: {vacancy['name']} \n"
                  f"Минимальная з/п: {vacancy['salary']}{vacancy['salary_currency']} \n"
                  f"Опыт работы: {vacancy['experience']} \n"
                  f"Ссылка на вакансию: {vacancy['url']} \n")

    @staticmethod
    def get_platforms_data(user_required_platform: str, keyword: str) -> list[Vacancies]:
        """
        Получает из ввода пользователя номер платформы (от 1 до 3) и привязывает ответ пользователя к соответствующему
        списку вакансий по платформам, получает вакансии в виде экземпляров класса с соответствующих платформ
        :param user_required_platform: номер платформы из ввода
        :param keyword: ключевое слово для работы с загрузкой вакансий по ключевому слову (наименование вакансии)
        :return:
        """
        platforms = {"1": (HeadHunterVacancies,), "2": (SuperJobVacancies,),
                     "3": (HeadHunterVacancies, SuperJobVacancies)}
        required_platforms_data = []
        if user_required_platform == "1":
            required_platforms = platforms["1"]
        elif user_required_platform == "2":
            required_platforms = platforms["2"]
        else:
            required_platforms = platforms["3"]

        for platform in required_platforms:
            required_platforms_data.extend(platform().load_vacancies(keyword))

        return required_platforms_data


