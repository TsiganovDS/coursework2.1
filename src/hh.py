from datetime import datetime
from typing import Any, Optional

import requests

from abc import ABC, abstractmethod

from src.fileworker import FileWorker
from src.vacancy import Vacancy


class AbstractJobAPI(ABC):

    @abstractmethod
    def get_area_id(self, city: str):
        """Получаем ID региона по названию города"""
        pass

    @abstractmethod
    def find_area_id(self, areas, city: str):
        """Получаем ID города"""
        pass


class HHAPI(AbstractJobAPI):
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "Your User Agent"}
        self.vacancies = []
        self.params = {"text": "", "area": "", "page": 0, "per_page": 20}

        super().__init__()

    def get_area_id(self, city: str) -> Optional[Any]:
        """Получаем ID региона по названию города"""
        url = "https://api.hh.ru/areas"
        response = requests.get(url)

        if response.status_code != 200:
            print("Ошибка при получении данных:", response.status_code)
            return None

        areas = response.json()
        return self.find_area_id(areas, city)

    def find_area_id(self, areas, city: str) -> Optional[Any]:
        """Получаем ID города"""
        for area in areas:
            if isinstance(area, dict):  # Проверяем, что это словарь
                if area["name"].lower() == city.lower():
                    return area["id"]
                if area.get("areas"):
                    found_id = self.find_area_id(area["areas"], city)
                    if found_id is not None:  # Проверяем на None
                        return found_id
        return None

    def fetch_and_save_vacancies(self, keyword: str, city: str):
        self.params["text"] = keyword
        self.params["area"] = self.get_area_id(city)
        found_vacancies = []
        while self.params["page"] < 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            if response.status_code == 200:
                vacancies = response.json().get("items", [])
                for item in vacancies:
                    if item is None:
                        continue

                    name_contains_query = keyword.lower() in item["name"].lower()
                    requirement_contains_query = (
                        item["snippet"].get("requirement")
                        and keyword.lower() in item["snippet"]["requirement"].lower()
                    )

                    if name_contains_query or requirement_contains_query:
                        salary_info = item.get("salary")
                        salary_value = salary_info.get("from", 0) if salary_info else 0

                        description = item["snippet"].get("requirement", "")
                        if not isinstance(description, str):
                            description = ""

                        published_at_raw = item.get("published_at", "")
                        if published_at_raw:
                            try:
                                published_at = datetime.strptime(published_at_raw, "%Y-%m-%dT%H:%M:%S%z").strftime(
                                    "%d.%m.%Y"
                                )
                            except ValueError:
                                published_at = None
                        else:
                            published_at = None

                        vacancy = Vacancy(
                            title=item["name"],
                            published_at=published_at,
                            city=item.get("area", {}).get("name"),
                            salary=salary_value,
                            description=description,
                            url=item["alternate_url"],
                        )
                        found_vacancies.append(vacancy)

                self.params["page"] += 1
            else:
                print(f"Ошибка запроса: {response.status_code}")
                break

        storage = FileWorker()
        storage.save(found_vacancies)

        if found_vacancies:
            print(
                f"Найдено {len(found_vacancies)} вакансий по запросу '{keyword.capitalize()}'"
                f" в г. {city.capitalize()}.\n"
                f"Они успешно сохранены."
            )
        else:
            print("Нет вакансий по запросу.")

        return found_vacancies

    @staticmethod
    def choice_2():
        city = input("Город: ")
        query = input("Вакансия: ")
        hhapi_instance = HHAPI()
        vacancies = hhapi_instance.fetch_and_save_vacancies(query, city)
        if vacancies:
            file_worker = FileWorker()
            file_worker.save(vacancies)
        Vacancy.function(vacancies)
        Vacancy.filtered(vacancies)
