import statistics
from functools import partial
from itertools import count

import requests
from tabulate import tabulate


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


def get_language_vacancies(api_key: str, language: str) -> dict:
    """Получаем вакансии на одной странице"""
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': api_key,
    }
    for page in count(0):
        params = {
            'catalogues': 48,  # id категории программирование и разработка
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


def get_language_statistic(api_key: str, language: str) -> dict:
    """Вычисляем среднюю зарплату по языку программирования"""
    partial_vacancies_per_page = partial(get_language_vacancies, api_key=api_key)
    language_vacancies = list(partial_vacancies_per_page(language=language))
    all_expected_salaries = list(filter(lambda x: x, map(predict_rub_salary, language_vacancies)))
    return {
        'Язык программирования': language,
        'Вакансий найдено': len(language_vacancies),
        'Вакансий обработано': len(all_expected_salaries),
        'Средняя зарплата': int(statistics.mean(all_expected_salaries))
        }

def get_salary_statistic_table(api_key: str, languages: list) -> str:
    partial_language_salary_statistic = partial(get_language_statistic, api_key)
    table = list(map(partial_language_salary_statistic, languages))
    return tabulate(table, headers='keys', tablefmt="grid")
    