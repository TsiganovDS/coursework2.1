from config import file_json
from src.fileworker import FileWorker
from src.hh import HHAPI
from src.vacancy import Vacancy


def main():
    """Функция взаимодействия с пользователем"""
    file_worker = FileWorker(file_json)
    file_worker.load()
    while True:
        choice = input(
            "1. Смотреть вакансии из файла\n"
            "2. Добавить вакансии\n"
            "3. Просмотреть топ - вакансии\n"
            "4. Удалить вакансии\n"
            "5. Вакансии в заданном диапазоне зарплат\n"
            "6. Сортировка вакансий по строке поиска\n"
            "7. Сортировка вакансий по дате\n"
            "8. Выход\n"
            "Выберите действие: "
        )
        if choice == "1":
            file_worker = FileWorker(file_json)
            vacancies = file_worker.load()
            Vacancy.print_vacancies(vacancies)
        elif choice == "2":
            hhapi_instance = HHAPI()
            hhapi_instance.fetch_and_save_vacancies()
        elif choice == "3":
            file_worker = FileWorker(file_json)
            vacancies = file_worker.load()
            Vacancy.display_top_n_vacancies(vacancies)
        elif choice == "4":
            FileWorker.clear_data()
        elif choice == "5":
            file_worker = FileWorker(file_json)
            vacancies = file_worker.load()
            Vacancy.filter_vacancies_by_salary(vacancies)
        elif choice == "6":
            file_worker = FileWorker(file_json)
            vacancies = file_worker.load()
            filtered_vacancies = Vacancy.filter_vacancies_by_keywords(vacancies)
            Vacancy.print_vacancies(filtered_vacancies)
        elif choice == "7":
            file_worker = FileWorker(file_json)
            vacancies = file_worker.load()
            Vacancy.sort_vacancies_by_date(vacancies)
        elif choice == "8":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
