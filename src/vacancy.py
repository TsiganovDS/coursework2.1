import re
from datetime import datetime


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = ["title", "published_at", "city", "salary", "description", "url"]

    def __init__(
        self, title, published_at, city: str, salary=None, description=None, url=None
    ):
        self.title = title
        self.published_at = published_at
        self.city = city
        self.salary = salary if salary is not None else "Зарплата не указана"
        self.description = description
        self.url = url
        self.__validate()

    def __validate(self):
        """Метод валидации"""
        if not isinstance(self.title, str) or not self.title:
            raise ValueError("Название вакансии должно быть непустой строкой.")
        if not isinstance(self.url, str) or not self.url.startswith("http"):
            raise ValueError("Ссылка на вакансию должна быть корректной URL.")
        if not isinstance(self.description, str):
            raise ValueError("Описание должно быть строкой.")

    def __lt__(self, other):
        return self.get_salary() < other.get_salary()

    def __gt__(self, other):
        return self.get_salary() > other.get_salary()

    def get_salary(self):
        """Метод ппеобразования  зарплаты в числовой формат"""
        if self.salary is None or not isinstance(self.salary, (int, str)):
            return 0
        if isinstance(self.salary, str):
            salary_value = re.sub(r"[^\d]", "", self.salary)
            return int(salary_value) if salary_value.isdigit() else 0
        return self.salary

    def to_dict(self):
        """Метод возвращает словарь, где ключи соответствуют полям
        вакансии, а значения — данным, хранящимся в атрибутах объекта."""
        return {
            "name": self.title,
            "published_at": self.published_at,
            "city": self.city,
            "salary": {"from": self.salary},
            "snippet": {"requirement": self.description},
            "alternate_url": self.url,
        }

    @staticmethod
    def filter_vacancies_by_keywords(vacancies):
        """Сортирует вакансии по строке поиска"""
        input_string = input("Введите ключевые слова для фильтрации вакансий: ")
        filter_words = [word.strip() for word in input_string.split(" ")]
        filtered_vacancies = []
        for vacancy in vacancies:
            if all(
                word.lower() in vacancy.description.lower() for word in filter_words
            ):
                filtered_vacancies.append(vacancy)
        if not filtered_vacancies:
            print("Нет вакансий по заданной строке поиска.")
        return filtered_vacancies

    @staticmethod
    def get_valid():
        """ВВод данных с клавиатуры"""
        min_salary = Vacancy.get_salary_input("Введите минимальную зарплату: ")
        max_salary = Vacancy.get_salary_input("Введите максимальную зарплату: ")

        while min_salary < 0 or max_salary < 0:
            print("Ошибка: Зарплата не может быть отрицательной. Попробуйте снова.")
            min_salary = Vacancy.get_salary_input("Введите минимальную зарплату: ")
            max_salary = Vacancy.get_salary_input("Введите максимальную зарплату: ")

        while min_salary > max_salary:
            print(
                "Ошибка: Минимальная зарплата не может быть больше максимальной. Попробуйте снова."
            )
            min_salary = Vacancy.get_salary_input("Введите минимальную зарплату: ")
            max_salary = Vacancy.get_salary_input("Введите максимальную зарплату: ")
        return min_salary, max_salary

    @staticmethod
    def get_salary_input(prompt):
        """Проверка входных данных"""
        while True:
            try:
                salary = input(prompt).strip()
                if not salary:
                    raise ValueError("Ввод не должен быть пустым.")
                salary_value = float(salary)
                return salary_value
            except ValueError:
                print("Ошибка: Пожалуйста, введите корректное число.")

    @staticmethod
    def filter_vacancies_by_salary(vacancies):
        """Сортирует вакансии по зарплате"""
        min_salary, max_salary = Vacancy.get_valid()
        filtered_vacancies = []
        for vacancy in vacancies:
            salary = vacancy.salary
            if salary is None:
                continue
            if isinstance(salary, str):
                salary = re.sub(r"[^\d]", "", salary)
                if salary.isdigit():
                    salary = int(salary)
                else:
                    continue
            if isinstance(salary, (int, float)) and min_salary <= salary <= max_salary:
                filtered_vacancies.append(vacancy)

        if not filtered_vacancies:
            print("Нет вакансий в заданном диапазоне зарплат.")
        else:
            print("Вакансии, отсортированные в заданном диапазоне зарплат:")
            Vacancy.print_vacancies(filtered_vacancies)

        return filtered_vacancies

    @staticmethod
    def get_top_n_vacancies(vacancies, n):
        """Формирует список top n вакансий"""
        return sorted(
            vacancies,
            key=lambda x: (
                x.salary
                if isinstance(x.salary, int)
                else (
                    int(x.salary)
                    if isinstance(x.salary, str) and x.salary.isdigit()
                    else 0
                )
            ),
            reverse=True,
        )[:n]

    @staticmethod
    def display_top_n_vacancies(vacancies):
        """Запрашивает количество вакансий для вывода и выводит топ N вакансий."""
        while True:
            try:
                n = int(input("Введите количество вакансий для вывода в топ N: "))
                if n > 0:
                    top_vacancies = Vacancy.get_top_n_vacancies(vacancies, n)
                    print("Топ вакансий по зарплате:")
                    Vacancy.print_vacancies(top_vacancies)
                    break
                else:
                    print("Количество вакансий должно быть положительным числом.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

    @staticmethod
    def print_vacancies(top_vacancies):
        """Функция для вывода вакансий на экран."""
        i = 1
        for v in top_vacancies:
            print(
                f"Вакансия № {i}: {v.title}, Дата: {v.published_at}, г.{v.city}, Зарплата: {v.salary},"
                f"Требования: {v.description}, Ссылка: {v.url}"
            )
            i += 1

    @staticmethod
    def sort_vacancies_by_date(vacancies):
        """Сортирует вакансии по дате публикации"""
        for v in vacancies:
            if isinstance(v.published_at, str):  # Изменено на точечную нотацию
                try:
                    v.published_at = datetime.strptime(v.published_at, "%d.%m.%Y")
                except ValueError:
                    print(f"Неверный формат даты для вакансии: {v.title}. Пропускаем.")
                    v.published_at = None

        sorted_vacancies = sorted(
            vacancies,
            key=lambda v: v.published_at if v.published_at else datetime.min,
            reverse=True,
        )
        print("Вакансии, отсортированные по дате:")
        if sorted_vacancies:
            for i, v in enumerate(sorted_vacancies, start=1):
                title = v.title
                published_at = (
                    v.published_at.strftime("%d.%m.%Y")
                    if isinstance(v.published_at, datetime)
                    else v.published_at
                )
                city = v.city
                salary = v.salary
                description = v.description
                url = v.url

                print(
                    f"Вакансия № {i}: {title}, Дата: {published_at}, г.{city}, Зарплата: {salary}, "
                    f"Требования: {description}, Ссылка: {url}"
                )
        else:
            print("Нет доступных вакансий.")
