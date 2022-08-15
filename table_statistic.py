import statistics
from tabulate import tabulate

from headhunter_salary import get_language_vacancies, predict_rub_salary
from superjob_salary import get_language_vacancies, predict_rub_salary


def get_language_statistic(language: str) -> dict:
    """Вычисляем среднюю зарплату по языку программирования"""
    language_vacancies = list(get_language_vacancies(language=language))
    all_expected_salaries = list(filter(lambda x: x, map(predict_rub_salary, language_vacancies)))
    return {
        'Язык программирования': language,
        'Вакансий найдено': len(language_vacancies),
        'Вакансий обработано': len(all_expected_salaries),
        'Средняя зарплата': int(statistics.mean(all_expected_salaries))
        }

def get_salary_statistic_table(languages: list) -> str:
    table = list(map(get_language_statistic, languages))
    return tabulate(table, headers='keys', tablefmt="grid")
