import json
import os
from abc import ABC, abstractmethod

from config import file_json
from src.vacancy import Vacancy


class AbstractFileWorker(ABC):
    """
    Инициализация класса FileWorker. Работа с json-файлом.

    :param file_json: Путь к JSON-файлу, где будут сохраняться вакансии.
    """

    @abstractmethod
    def save(self, vacancies):
        """Сохранить вакансии в файл."""
        pass

    @abstractmethod
    def load(self):
        """Загрузить вакансии из файла."""
        pass


class FileWorker:
    def __init__(self, file_json):
        self.file_json = file_json

    def save(self, vacancies):
        """
        Метод сохранения вакансий в файл.
        Если вакансии уже существуют, они не будут добавлены.

        :param vacancies: Список вакансий для сохранения.
        """
        existing_vacancies = self.load()
        existing_titles = {vacancy.title for vacancy in existing_vacancies}

        new_vacancies = [
            vacancy for vacancy in vacancies if vacancy.title not in existing_titles
        ]

        existing_vacancies.extend(new_vacancies)

        with open(self.file_json, "w", encoding="utf-8") as file:
            json.dump(
                [vacancy.to_dict() for vacancy in existing_vacancies],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def load(self):
        """
        Метод загрузки вакансий из JSON-файла.

        :return: Список объектов Vacancy, загруженных из файла.
        """
        if not os.path.exists(self.file_json) or os.path.getsize(self.file_json) == 0:
            return []
        try:
            with open(self.file_json, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not data:
                    print(
                        "Файл пуст. Пожалуйста, сделайте API запрос для получения вакансий."
                    )
                return [
                    Vacancy(
                        item["name"],
                        item["published_at"],
                        item["city"],
                        (
                            item["salary"]["from"]
                            if "salary" in item and "from" in item["salary"]
                            else 0
                        ),
                        item["snippet"]["requirement"],
                        item["alternate_url"],
                    )
                    for item in data
                ]
        except KeyError as e:
            print(f"Ошибка: отсутствует необходимый ключ {e} в данных вакансии.")
            return []
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
            return []

    @staticmethod
    def clear_data():
        """
        Удаляет все данные из JSON-файла.
        Запрашивает подтверждение у пользователя перед удалением.
        """
        answer = input("Удалить вакансии (да/нет): ")
        if answer.lower() == "да":
            try:
                with open(file_json, "w", encoding="utf-8") as file:
                    json.dump([], file)
                print("Все данные из файла успешно удалены.")
            except Exception as e:
                print(f"Ошибка при удалении данных: {e}")
        else:
            print("Удаление отменено.")

    @staticmethod
    def parse_salary(salary):
        """
        Метод обработки значения зарплаты.

        :param salary: Значение зарплаты для обработки.
        :return: Целое число, представляющее зарплату или 0, если значение недопустимо.
        """
        if isinstance(salary, str):
            if salary.lower() == "зарплата не указана":
                return 0
            try:
                return int(salary)
            except ValueError:
                return 0
        return salary if salary is not None else 0
