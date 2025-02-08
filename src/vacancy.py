import re


class Vacancy:
    def __init__(self, title, published_at, city: str, salary=None, description=None, url=None):
        self.title = title
        self.published_at = published_at
        self.city = city
        self.salary = salary if salary is not None else "Зарплата не указана"
        self.description = description
        self.url = url
        self.validate()

    def validate(self):
        if not isinstance(self.title, str) or not self.title:
            raise ValueError("Название вакансии должно быть непустой строкой.")
        if not isinstance(self.url, str) or not self.url.startswith("http"):
            raise ValueError("Ссылка на вакансию должна быть корректной URL.")
        if not isinstance(self.description, str):
            raise ValueError("Описание должно быть строкой.")

    def to_dict(self):
        return {
            "name": self.title,
            "published_at": self.published_at,
            "city": self.city,
            "salary": {"from": self.salary},
            "snippet": {"requirement": self.description},
            "alternate_url": self.url,
        }

    @staticmethod
    def filter_vacancies_by_keywords(vacancies, filter_words):
        filtered_vacancies = []
        for vacancy in vacancies:
            if all(word.lower() in vacancy.description.lower() for word in filter_words):
                filtered_vacancies.append(vacancy)
        return filtered_vacancies

    @staticmethod
    def filter_vacancies_by_salary(vacancies, min_salary, max_salary):
        filtered_vacancies = []

        for vacancy in vacancies:
            salary = vacancy.salary

            if salary is None:
                continue

            if isinstance(salary, str):
                salary = re.sub(r"[^\d]", "", salary)  # Убираем все, кроме цифр
                if salary.isdigit():
                    salary = int(salary)
                else:
                    continue

            if (
                isinstance(salary, (int, float))
                and isinstance(min_salary, (int, float))
                and isinstance(max_salary, (int, float))
            ):
                if min_salary <= salary <= max_salary:
                    filtered_vacancies.append(vacancy)

        return filtered_vacancies

    @staticmethod
    def get_top_n_vacancies(found_vacancies, n):
        return sorted(
            found_vacancies,
            key=lambda x: (
                x.salary
                if isinstance(x.salary, int)
                else (int(x.salary) if isinstance(x.salary, str) and x.salary.isdigit() else 0)
            ),
            reverse=True,
        )[:n]


    @staticmethod
    def print_vacancies(vacancies):
        """Функция для вывода вакансий на экран."""
        i = 1
        for v in vacancies:
            print(
                f"Вакансия № {i}: {v.title}, Дата: {v.published_at}, г.{v.city}, Зарплата: {v.salary}, "
                f"Требования: {v.description}, Ссылка: {v.url}"
            )
            i += 1

    @staticmethod
    def function(vacancies):
        """Вспомогательная функция"""
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
    def filtered(vacancies):
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
        filtered = Vacancy.filter_vacancies_by_keywords(vacancies, filter_words)
        Vacancy.print_vacancies(filtered)
        user_input = input("Введите диапазон зарплат (пример: 100000 150000): ")
        min_salary, max_salary = map(int, user_input.split())
        fil = Vacancy.filter_vacancies_by_salary(vacancies, min_salary, max_salary)
        Vacancy.print_vacancies(fil)
