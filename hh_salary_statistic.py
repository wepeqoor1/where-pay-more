import json
import requests
import statistics


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


def get_vacancies(url: str, text: str, page: int) -> dict:
    params = {
        'professional_role': 96,  # Specialization programmer id
        'area': 1,  # Moscow
        'text': text,  # Searched text
        'page': page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    
    hh_url = 'https://api.hh.ru'
    salary_statistics = {}

    for programmer_language in PROGRAMMER_LANGUAGES:
        all_language_vacancies = []
        all_expected_salaries = []
        page = 0
        pages_number = 1
        
        while page < pages_number:
            print(f'{programmer_language=}, {page=}')
            text = f'Программист {programmer_language}'

            try:
                per_page_vacancies = get_vacancies(url=f'{hh_url}/vacancies', text=text, page=page)
            except requests.HTTPError as error:
                print(error.response.json())

            pages_number = per_page_vacancies['pages']
            page += 1
                
            all_language_vacancies += per_page_vacancies['items']

        for vacancy in all_language_vacancies:
            expected_salaries = predict_rub_salary(vacancy=vacancy)

            if not expected_salaries:
                continue
            
            all_expected_salaries.append(expected_salaries)

        language_salary_statistic = {
            programmer_language: {
                'vacancies_found': per_page_vacancies['found'],
                'vacancies_processed': len(all_expected_salaries),
                'average_salary': int(statistics.mean(all_expected_salaries)),
            }
        }
        salary_statistics.update(language_salary_statistic)

    with open('hh_salary_statistics.json', 'w', encoding='utf-8') as write_file:
        json.dump(salary_statistics, write_file, ensure_ascii=False, indent=4)
