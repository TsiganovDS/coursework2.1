import json
import os
from abc import abstractmethod, ABC

from src.vacancy import Vacancy

class AbstractFileWorker(ABC):
    @abstractmethod
    def save(self, vacancies):
        """Сохранить вакансии в файл."""
        pass

    @abstractmethod
    def load(self):
        """Загрузить вакансии из файла."""
        pass


class FileWorker:
    def __init__(self, file_name="vacancies.json"):
        self.file_name = file_name

    def save(self, vacancies):
        existing_vacancies = self.load()
        existing_vacancies.extend(vacancies)
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(
                [vacancy.to_dict() for vacancy in existing_vacancies],
                file,
                ensure_ascii=False,
                indent=4,
            )


    def load(self):
        if not os.path.exists(self.file_name) or os.path.getsize(self.file_name) == 0:
            return []
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [
                    Vacancy(
                        item["name"],
                        item["published_at"],
                        item["city"],
                        (item["salary"]["from"] if "salary" in item and "from" in item["salary"] else 0),
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
    def parse_salary(salary):
        if isinstance(salary, str):
            if salary.lower() == "зарплата не указана":
                return 0
            try:
                return int(salary)
            except ValueError:
                return 0
        return salary if salary is not None else 0

    @staticmethod
    def choice_1():
        file_worker = FileWorker()
        vacancies = file_worker.load()
        print(f"Загружено {len(vacancies)} вакансий из файла.")
        Vacancy.function(vacancies)
        Vacancy.filtered(vacancies)
