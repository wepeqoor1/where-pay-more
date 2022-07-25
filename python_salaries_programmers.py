import requests

from utils import get_vacancies


def predict_rub_salary(vacancy: dict) -> float:
    salary = vacancy.get('salary')
    if not salary:
        return None
    if not salary['from']:
        return salary['to'] * 0.8
    if not salary['to']:
        return salary['from'] * 1.2
    return (salary['to'] - salary['from']) / 2 + salary['from']


if __name__ == '__main__':
    url = 'https://api.hh.ru/vacancies'

    try:
        text = 'Программист Python'
        vacancies=get_vacancies(
            text=text,
            url=url,
            )
        for item in vacancies['items']:
            print(item.get('salary'))   
            print(predict_rub_salary(vacancy=item))
        
    except requests.HTTPError as error:
        print('Что то не получилось')
        
