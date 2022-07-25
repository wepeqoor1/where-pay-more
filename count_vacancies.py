import requests
import statistics


def predict_rub_salary(vacancy: dict) -> float|None:
    salary = vacancy.get('salary')
    if not salary:
        return None
    if not salary['from']:
        return salary['to'] * 0.8
    if not salary['to']:
        return salary['from'] * 1.2
    return (salary['to'] - salary['from']) / 2 + salary['from']


def get_vacancies(url: str, text: str) -> dict:
    params = {
        "professional_role": 96,  # Specialization programmer id
        "area": 1,  # Moscow
        "text": text  # Searched text
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()


if __name__ == '__main__':
    
    programmer_languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C#',
        'C',
        'Go',
    ]

    url = 'https://api.hh.ru/vacancies'

    one_page_salary_statistics = {}
    
    try:
        for programmer_language in programmer_languages:
            text = f'Программист {programmer_language}'
            vacancies=get_vacancies(
                url = url,
                text=text,
                )
            average_salaries = [predict_rub_salary(vacancy=vacancy) for vacancy in vacancies['items']]
            actual_average_salaries = list(filter(None, average_salaries))
            
            language_salary_statistic = {
                    programmer_language: {
                        "vacancies_found": vacancies['found'],
                        "vacancies_processed": len(actual_average_salaries),
                        "average_salary": int(statistics.mean(actual_average_salaries)),
                    }
                }
            one_page_salary_statistics.update(language_salary_statistic)
            
    except requests.HTTPError as error:
        print('Что то не получилось')
    