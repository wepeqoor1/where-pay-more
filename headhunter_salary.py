import requests


def predict_rub_salary(vacancy: dict) -> float | None:
    salary = vacancy.get('salary')
    salary_increase_ratio = 1.2
    salary_reduction_ratio = 0.8
    
    if not salary:
        return None
    if not salary['from']:
        return salary['to'] * salary_reduction_ratio
    if not salary['to']:
        return salary['from'] * salary_increase_ratio
    return (salary['to'] - salary['from']) / 2 + salary['from']


def get_language_vacancies(language: str) -> dict:
    """Получаем вакансии на одной странице"""
    url = 'https://api.hh.ru/vacancies/'
    page = 0
    pages_number = 1
    
    while page < pages_number:
        params = {
        'professional_role': 96,  # Specialization: programmer id
        'area': 1,  # Moscow
        'text': f'Программист {language}',  # Searched text
        'page': page,
    }
        response = requests.get(url, params=params) 
        response.raise_for_status()
        per_page_vacancies: dict = response.json()
        
        pages_number = per_page_vacancies['pages']
        page += 1

        yield from per_page_vacancies['items']

    