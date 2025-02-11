import os

import pytest

from src.fileworker import FileWorker
from src.vacancy import Vacancy


@pytest.fixture
def setup_file_worker(tmp_path):
    file_path = tmp_path / "test_vacancies.json"
    worker = FileWorker(file_path)
    worker.__init__(file_path)
    yield worker, file_path
    if file_path.exists():
        os.remove(file_path)


def test_save_and_load_vacancies(setup_file_worker):
    worker, file_path = setup_file_worker

    vacancy1 = Vacancy(
        "Программист",
        "2023-01-01",
        "Москва",
        100000,
        "Знание Python",
        "http://example.com/1",
    )
    vacancy2 = Vacancy(
        "Тестировщик",
        "2023-01-02",
        "Санкт-Петербург",
        80000,
        "Знание тестирования",
        "http://example.com/2",
    )

    worker.save([vacancy1, vacancy2])

    loaded_vacancies = worker.load()

    assert len(loaded_vacancies) == 2
    assert loaded_vacancies[0].title == "Программист"
    assert loaded_vacancies[1].title == "Тестировщик"


def test_save_existing_vacancy(setup_file_worker):
    worker, file_path = setup_file_worker

    vacancy1 = Vacancy(
        "Программист",
        "2023-01-01",
        "Москва",
        100000,
        "Знание Python",
        "http://example.com/1",
    )
    vacancy2 = Vacancy(
        "Программист",
        "2023-01-01",
        "Москва",
        100000,
        "Знание Python",
        "http://example.com/1",
    )

    worker.save([vacancy1])
    worker.save([vacancy2])

    loaded_vacancies = worker.load()
    assert len(loaded_vacancies) == 1


def test_clear_data(setup_file_worker, monkeypatch):
    worker, file_path = setup_file_worker

    vacancy = Vacancy(
        "Программист",
        "2023-01-01",
        "Москва",
        100000,
        "Знание Python",
        "http://example.com/1",
    )
    worker.save([vacancy])

    monkeypatch.setattr("builtins.input", lambda _: "да")
    worker.clear_data()

    loaded_vacancies = worker.load()
    assert len(loaded_vacancies) == 1


def test_parse_salary():
    assert FileWorker.parse_salary("50000") == 50000
    assert FileWorker.parse_salary("зарплата не указана") == 0
    assert FileWorker.parse_salary("abc") == 0
    assert FileWorker.parse_salary(None) == 0
    assert FileWorker.parse_salary(60000) == 60000
