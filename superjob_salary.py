import os
import statistics
from itertools import count

import requests


def predict_rub_salary(vacancy: dict) -> float | None:
    salary_increase_ratio = 1.2
    salary_reduction_ratio = 0.8
    if not vacancy['payment_to'] and not vacancy['payment_from']:
        return None
    if not vacancy['payment_from']:
        return vacancy['payment_to'] * salary_reduction_ratio
    return statistics.mean([
        vacancy['payment_to'], vacancy['payment_from']]) \
        if vacancy['payment_to'] \
        else vacancy['payment_from'] * salary_increase_ratio


def get_language_vacancies(language: str) -> dict:
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': os.getenv('SUPER_JOB_API_KEY'),
    }
    for page in count(0):
        params = {
            'catalogues': 48,  # Specialization: programmer id
            'town': 'Москва',
            'count': 100,  # Количество вакансий на странице
            'currency': 'rub',
            'page': page,
            'keyword': f'Программист {language}',
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        vacancy: dict = response.json()['objects']
        if not vacancy:
            break
        yield from vacancy
    