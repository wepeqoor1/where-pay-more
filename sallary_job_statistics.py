import os
import statistics
import numpy as np
import requests

from dotenv import load_dotenv
from terminaltables import SingleTable


PROGRAMMER_LANGUAGES = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C#',
        'C',
        'Go',
    ]
    
    
SUPERJOB_URL = 'https://api.superjob.ru'
SUPERJOB_API_KEY = os.getenv('SUPER_JOB_API_KEY')
SUPERJOB_CLIENT_ID = os.getenv('SUPER_JOB_CLIENT_ID')
SUPERJOB_LOGIN = os.getenv('SUPER_JOB_LOGIN')
SUPERJOB_PASSWORD = os.getenv('SUPER_JOB_PASSWORD')
    

def get_authorize_superjob(url: str, client_id: int, login: str, password: str, api_key: str ) -> dict:
    params = {
        'client_id': client_id,
        'login': login,
        'password': password,
        'client_secret': api_key,
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()


def get_vacancies_superjob(url: str, api_key: str, access_token: str, keyword: str, page: int) -> dict:
    headers = {
        'X-Api-App-Id': api_key,
        'Authorization': f'Bearer {access_token}',
    }
    params = {
        'catalogues': 48,
        'town': 'Москва',
        'count': 100,
        'page': page,
        'keyword': keyword,
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    return response.json()


def predict_rub_salary_superjob(vacancy: dict) -> float | None:
    salary_increase_ratio = 1.2
    salary_reduction_ratio = 0.8

    if not vacancy['payment_to'] and not vacancy['payment_from']:
        return None
    if not vacancy['payment_from']:
        return vacancy['payment_to'] * salary_reduction_ratio
    if not vacancy['payment_to']:
        return vacancy['payment_from'] * salary_increase_ratio
    return (vacancy['payment_to'] - vacancy['payment_from']) / 2 + vacancy['payment_from']


def generate_statistic_table(statistic: dict) -> str:
    # Собираем двухмерную матрицу из словаря
    column_titles = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    table_values = np.array([list(item.values()) for item in statistic.values()])
    programmer_languages = np.transpose([list(statistic)])
    np_array_values = np.hstack((programmer_languages, table_values))
    table = np.vstack((column_titles, np_array_values)).tolist()
    
    # Генерируем таблицу со статистикой
    title = 'SuperJob Moscow'
    table_instance = SingleTable(table, title)
    table_instance.justify_columns[2] = 'right'
    
    return table_instance.table


def get_statistic_superjob(url: str, api_key: str, client_id: int, login: str, password: str) -> dict:
    try:
        authorization = get_authorize_superjob(
            url=f'{url}/2.0/oauth2/password/',
            client_id=client_id,
            login=login,
            password=password,
            api_key=api_key
            )
    except requests.HTTPError as error:
        print(f'Запрос Авторизации не отработал: \n {error.response.json()}')
        exit(1)

    access_token = authorization['access_token']
    salary_statistics = {}

    for programmer_language in PROGRAMMER_LANGUAGES:
        searched_text = f'Программист {programmer_language}'
        all_expected_salaries = []
        all_language_vacancies = []
        page = 0

        while True:
            try:
                per_page_vacancies = get_vacancies_superjob(
                    url=f'{SUPERJOB_URL}/2.0/vacancies/',
                    api_key=SUPERJOB_API_KEY,
                    access_token=access_token,
                    keyword=searched_text,
                    page = page,
                    )
            except requests.HTTPError as error:
                print(f'Запрос на получение вакансий не отработал: \n {error.response.json()}')
                exit(1)

            all_language_vacancies += per_page_vacancies['objects']

            if per_page_vacancies['more']:
                page += 1
            else:
                break

        for vacancy in all_language_vacancies:
            expected_salaries = predict_rub_salary_superjob(vacancy=vacancy)

            if not expected_salaries:
                continue
            
            all_expected_salaries.append(expected_salaries)

        language_salary_statistic = {
            programmer_language: {
                'vacancies_found': per_page_vacancies['total'],
                'vacancies_processed': len(all_expected_salaries),
                'average_salary': int(statistics.mean(all_expected_salaries)),
            }
        }
        salary_statistics.update(language_salary_statistic)
    
    return salary_statistics


if __name__ == "__main__":
    load_dotenv()
    
    superjob_statistic = get_statistic_superjob(
        url=SUPERJOB_URL,
        api_key=SUPERJOB_API_KEY,
        client_id=SUPERJOB_CLIENT_ID,
        login=SUPERJOB_LOGIN,
        password=SUPERJOB_PASSWORD
        )
    
    print(generate_statistic_table(superjob_statistic))
    
    
    