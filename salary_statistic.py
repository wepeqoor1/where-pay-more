import json
import requests
import statistics


URL_HEAD_HUNTER_VACANCIES = "https://api.hh.ru/vacancies"


def predict_rub_salary(vacancy: dict) -> float | None:
    salary = vacancy.get("salary")
    if not salary:
        return None
    if not salary["from"]:
        return salary["to"] * 0.8
    if not salary["to"]:
        return salary["from"] * 1.2
    return (salary["to"] - salary["from"]) / 2 + salary["from"]


def get_vacancies(url: str, text: str, page: int) -> dict:
    params = {
        "professional_role": 96,  # Specialization programmer id
        "area": 1,  # Moscow
        "text": text,  # Searched text
        "page": page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":

    programmer_languages = [
        "JavaScript",
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C#",
        "C",
        "Go",
    ]

    salary_statistics = {}

    for programmer_language in programmer_languages:
        all_language_vacancies = []
        all_average_salaries = []

        for page in range(10):
            text = f"Программист {programmer_language}"

            try:
                vacancies = get_vacancies(
                    url=URL_HEAD_HUNTER_VACANCIES,
                    text=text,
                    page=page
                )
            except requests.HTTPError as error:
                if error.response.status_code == 400:
                    break
            all_language_vacancies += vacancies
        
        for vacancy in all_language_vacancies:
            average_salaries = list(
                filter(
                    None,
                    [predict_rub_salary(vacancy=vacancy) for vacancy in vacancies['items']],
                )
            )
            if not average_salaries:
                continue
            
            all_average_salaries += average_salaries
            
            language_salary_statistic = {
                programmer_language: {
                    "vacancies_found": vacancies["found"],
                    "vacancies_processed": len(all_average_salaries),
                    "average_salary": int(statistics.mean(all_average_salaries)),
                }
            }
            salary_statistics.update(language_salary_statistic)

    print(salary_statistics)
