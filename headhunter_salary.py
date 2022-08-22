import requests

from table_statistic_tools import predict_salary


def predict_rub_salary_hh(vacancy: dict):
    salary = vacancy.get("salary")
    if not salary:
        return None
    if salary["currency"] != "RUR":
        return None
    return predict_salary(salary["from"], salary["to"])


def get_language_vacancies_hh(language: str) -> dict:
    url = "https://api.hh.ru/vacancies/"
    page = 0
    pages_number = 1

    while page < pages_number:
        params = {
            "professional_role": 96,  # Specialization: programmer id
            "area": 1,  # Moscow
            "text": f"Программист {language}",  # Searched text
            "page": page,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        per_page_vacancies: dict = response.json()

        pages_number = per_page_vacancies["pages"]
        page += 1

        yield from per_page_vacancies["items"]
