import os
import statistics
from typing import Optional
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


def get_vacancies(url: str, api_key: Optional[str], keyword: str, page: int) -> dict:
    headers = {
        'X-Api-App-Id': api_key,
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


def superjob_predict_rub_salary(vacancy: dict) -> float | None:
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


if __name__ == "__main__":
    load_dotenv()

    sj_url = 'https://api.superjob.ru'
    sj_api_key = os.getenv('SUPER_JOB_API_KEY')
    sj_client_id = os.getenv('SUPER_JOB_CLIENT_ID')
    sj_login = os.getenv('SUPER_JOB_LOGIN')
    sj_password = os.getenv('SUPER_JOB_PASSWORD')

    salary_statistics = dict()

    for programmer_language in PROGRAMMER_LANGUAGES:
        keyword = f'Программист {programmer_language}'
        all_expected_salaries = list()
        all_language_vacancies = list()
        page = 0

        while True:
            try:
                per_page_vacancies = get_vacancies(
                    url=f'{sj_url}/2.0/vacancies/', 
                    api_key=sj_api_key, 
                    # access_token=access_token,
                    keyword=keyword,
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
            expected_salaries = superjob_predict_rub_salary(vacancy=vacancy)

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
    
    statistic_table = generate_statistic_table(salary_statistics)
    print(statistic_table)
    