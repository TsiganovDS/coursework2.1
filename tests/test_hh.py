from unittest.mock import patch

import pytest

from src.hh import HHAPI


@pytest.fixture
def hh_api():
    return HHAPI()


def test_get_area_id_success(hh_api):
    mock_response = [
        {"id": 1, "name": "Москва"},
        {"id": 2, "name": "Санкт-Петербург"},
    ]

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        area_id = hh_api.get_area_id("Москва")
        assert area_id == 1


def test_find_area_id_success(hh_api):
    areas = [
        {"id": 1, "name": "Москва", "areas": []},
        {"id": 2, "name": "Санкт-Петербург", "areas": []},
    ]
    assert hh_api.find_area_id(areas, "Москва") == 1
    assert hh_api.find_area_id(areas, "Санкт-Петербург") == 2


def test_get_valid_input(mocker):
    mocker.patch("builtins.input", side_effect=["Москва", "разработчик"])
    city, keyword = HHAPI().get_valid_input()
    assert city == "Москва"
    assert keyword == "разработчик"


def test_fetch_and_save_vacancies(mocker, hh_api):
    mocker.patch("builtins.input", side_effect=["Москва", "Разработчик"])

    with patch.object(hh_api, "get_area_id", return_value=1):
        mock_response = {
            "items": [
                {
                    "name": "Разработчик Python",
                    "snippet": {"requirement": "Опыт работы с Python"},
                    "salary": {"from": 100000},
                    "area": {"name": "Москва"},
                    "alternate_url": "http://example.com",
                    "published_at": "2023-09-01T10:00:00+0300",
                }
            ]
        }
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response

            vacancies = hh_api.fetch_and_save_vacancies()

            assert len(vacancies) == 20
            assert vacancies[0].title == "Разработчик Python"
            assert vacancies[0].salary == 100000
            assert vacancies[0].city == "Москва"
            assert vacancies[0].url == "http://example.com"
