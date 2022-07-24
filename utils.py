import requests


def get_vacancies(text: str) -> dict:
    url = 'https://api.hh.ru/vacancies'
    params = {
        "professional_role": 96,  # Specialization programmer id
        "area": 1,  # Moscow
        "text": text  # Searched text
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()
