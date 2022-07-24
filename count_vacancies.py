import requests

from utils import get_vacancies


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
    
    programmer_languages_count = {}

    try:
        for programmer_language in programmer_languages:
            text = f'Программист {programmer_language}'
            vacancies=get_vacancies(
                text=text,
                )
            vacancies_count = vacancies['found']
            programmer_languages_count[programmer_language] = vacancies_count

    except requests.HTTPError as error:
        print('Что то не получилось')
        
    print(programmer_languages_count)
