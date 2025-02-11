from unittest.mock import MagicMock, patch

import pytest

from src.vacancy import Vacancy


@pytest.fixture
def vacancy():
    """Создает тестовую вакансию."""
    return Vacancy(
        title="Программист",
        published_at="2023-01-01",
        city="Москва",
        salary="100000",
        description="Знание Python",
        url="http://example.com/1",
    )


def test_vacancy_initialization(vacancy):
    assert vacancy.title == "Программист"
    assert vacancy.published_at == "2023-01-01"
    assert vacancy.city == "Москва"
    assert vacancy.get_salary() == 100000
    assert vacancy.description == "Знание Python"
    assert vacancy.url == "http://example.com/1"


def test_get_salary_with_string(vacancy):
    vacancy.salary = "150000"
    assert vacancy.get_salary() == 150000


def test_get_salary_with_invalid_string(vacancy):
    vacancy.salary = "abc"
    assert vacancy.get_salary() == 0


def test_get_salary_with_none(vacancy):
    vacancy.salary = None
    assert vacancy.get_salary() == 0


def test_filter_vacancies_by_keywords(vacancy):
    vacancies = [vacancy]
    with pytest.MonkeyPatch.context() as m:
        m.setattr("builtins.input", lambda _: "Python")
        filtered_vacancies = Vacancy.filter_vacancies_by_keywords(vacancies)
        assert len(filtered_vacancies) == 1


def test_filter_vacancies_no_match(vacancy):
    vacancies = [vacancy]
    with pytest.MonkeyPatch.context() as m:
        m.setattr("builtins.input", lambda _: "Java")
        filtered_vacancies = Vacancy.filter_vacancies_by_keywords(vacancies)
        assert len(filtered_vacancies) == 0


def test_vacancy_to_dict(vacancy):
    expected_dict = {
        "name": "Программист",
        "published_at": "2023-01-01",
        "city": "Москва",
        "salary": {"from": "100000"},
        "snippet": {"requirement": "Знание Python"},
        "alternate_url": "http://example.com/1",
    }
    assert vacancy.to_dict() == expected_dict


def test_valid_salary_input(mocker):
    mocker.patch("builtins.input", side_effect=["20000", "30000"])
    min_salary, max_salary = Vacancy.get_valid()
    assert min_salary == 20000
    assert max_salary == 30000


@pytest.fixture
def mock_get_valid():
    """Фикстура для замены метода get_valid."""
    with patch.object(Vacancy, "get_valid", return_value=(30000, 100000)) as mock:
        yield mock


def test_filter_vacancies_by_salary(mock_get_valid):
    """Тест для фильтрации вакансий по зарплате."""

    vacancy1 = MagicMock(salary=35000)
    vacancy2 = MagicMock(salary=25000)
    vacancy3 = MagicMock(salary=45000)
    vacancy4 = MagicMock(salary=None)
    vacancy5 = MagicMock(salary="abc")

    vacancies = [vacancy1, vacancy2, vacancy3, vacancy4, vacancy5]

    with patch("builtins.print") as mock_print:
        filtered_vacancies = Vacancy.filter_vacancies_by_salary(vacancies)
    assert len(filtered_vacancies) == 2
    assert filtered_vacancies[0].salary == 35000
    assert filtered_vacancies[1].salary == 45000
    mock_print.assert_any_call(
        "Вакансии, отсортированные в заданном диапазоне зарплат:"
    )
    assert mock_print.call_count == 3


def test_filter_vacancies_no_valid(mock_get_valid):
    """Тест, когда нет вакансий в заданном диапазоне зарплат."""
    vacancy1 = MagicMock(salary=25000)
    vacancy2 = MagicMock(salary="abc")
    vacancy3 = MagicMock(salary=None)

    vacancies = [vacancy1, vacancy2, vacancy3]

    with patch("builtins.print") as mock_print:
        filtered_vacancies = Vacancy.filter_vacancies_by_salary(vacancies)

    assert len(filtered_vacancies) == 0

    mock_print.assert_any_call("Нет вакансий в заданном диапазоне зарплат.")
    assert mock_print.call_count == 1


def test_get_top_n_vacancies():
    vacancies = [
        Vacancy(
            "Вакансия 1", "01.012023", "Москва", 100000, "Описание 1", "http://url1"
        ),
        Vacancy(
            "Вакансия 2", "01.022023", "Москва", "80000", "Описание 2", "http://url2"
        ),
        Vacancy(
            "Вакансия 3", "01.03.2023", "Москва", 120000, "Описание 3", "http://url3"
        ),
        Vacancy(
            "Вакансия 4", "01.04.2023", "Москва", "50000", "Описание 4", "http://url4"
        ),
    ]

    top_vacancies = Vacancy.get_top_n_vacancies(vacancies, 2)
    assert len(top_vacancies) == 2
    assert top_vacancies[0].title == "Вакансия 3"
    assert top_vacancies[1].title == "Вакансия 1"


@patch("builtins.input", side_effect=["2"])
@patch("builtins.print")
def test_display_top_n_vacancies(mock_print, mock_input):
    vacancies = [
        Vacancy(
            "Вакансия 1", "01.01.2023", "Москва", 100000, "Описание 1", "http://url1"
        ),
        Vacancy(
            "Вакансия 2", "01.02.2023", "Москва", 80000, "Описание 2", "http://url2"
        ),
    ]

    Vacancy.display_top_n_vacancies(vacancies)

    mock_print.assert_any_call("Топ вакансий по зарплате:")
    mock_print.assert_any_call(
        "Вакансия № 1: Вакансия 1, Дата: 01.01.2023, г.Москва, Зарплата: 100000,"
        "Требования: Описание 1, Ссылка: http://url1"
    )
    mock_print.assert_any_call(
        "Вакансия № 2: Вакансия 2, Дата: 01.02.2023, г.Москва, Зарплата: 80000,"
        "Требования: Описание 2, Ссылка: http://url2"
    )


@pytest.fixture
def vacancies():
    return [
        Vacancy(
            "Вакансия 1", "15.01.2023", "Москва", 100000, "Описание 1", "http://url1"
        ),
        Vacancy(
            "Вакансия 2",
            "10.02.2023",
            "Санкт-Петербург",
            80000,
            "Описание 2",
            "http://url2",
        ),
        Vacancy(
            "Вакансия 3", "05.01.2023", "Казань", 120000, "Описание 3", "http://url3"
        ),
        Vacancy(
            "Вакансия 4",
            "неверная_дата",
            "Екатеринбург",
            90000,
            "Описание 4",
            "http://url4",
        ),
        Vacancy(
            "Вакансия 5",
            "20.01.2023",
            "Нижний Новгород",
            95000,
            "Описание 5",
            "http://url5",
        ),
    ]


def test_sort_vacancies_by_date(vacancies):
    Vacancy.sort_vacancies_by_date(vacancies)

    sorted_titles = [v.title for v in vacancies if v.published_at is not None]

    expected_titles = ["Вакансия 1", "Вакансия 2", "Вакансия 3", "Вакансия 5"]

    assert sorted_titles == expected_titles


@pytest.mark.parametrize(
    "salary_input, expected_output",
    [
        (None, 0),
        (100000, 100000),
        ("100000", 100000),
        ("100,000", 100000),
        ("$100000", 100000),
        ("неизвестно", 0),
        ("", 0),
    ],
)
def test_get_salary(salary_input, expected_output):
    vacancy = Vacancy(
        "Вакансия", "01.01.2023", "Москва", salary_input, "Описание", "http://url"
    )
    assert vacancy.get_salary() == expected_output


if __name__ == "__main__":
    pytest.main()
