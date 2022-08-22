from itertools import count
import requests

from table_statistic_tools import predict_salary


def predict_rub_salary_sj(vacancy: dict) -> None | dict:
    if vacancy["currency"] != "rub":
        return None
    return predict_salary(vacancy["payment_from"], vacancy["payment_to"])


def get_language_vacancies_sj(language: str, api_key: str) -> dict:
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": api_key,
    }
    for page in count(0):
        params = {
            "catalogues": 48,  # Specialization: programmer id
            "town": "Москва",
            "count": 100,  # Number vacancies per page
            "currency": "rub",
            "page": page,
            "keyword": f"Программист {language}",
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        vacancy: dict = response.json()["objects"]
        if not vacancy:
            break
        return vacancy
