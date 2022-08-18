import statistics


def get_language_statistic(language_vacancies: list, all_expected_salaries: list, language: str) -> dict:
    """Calculate average salary for the programming language"""
    return {
        'Язык программирования': language,
        'Вакансий найдено': len(language_vacancies),
        'Вакансий обработано': len(all_expected_salaries),
        'Средняя зарплата': int(statistics.mean(all_expected_salaries))
        }


def predict_salary(salary_from, salary_to):
    salary_increase_ratio = 1.2
    salary_reduction_ratio = 0.8
    
    if salary_from == salary_to == 0:
        return None
    if salary_from and salary_to:
        return statistics.mean([salary_from, salary_to])
    if not salary_to:
        return salary_from * salary_increase_ratio
    if not salary_from:
        return salary_to * salary_reduction_ratio