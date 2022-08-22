import os
from dotenv import load_dotenv
from tabulate import tabulate
from functools import partial

from table_statistic_tools import get_language_statistic
from superjob_salary import get_language_vacancies_sj, predict_rub_salary_sj
from headhunter_salary import get_language_vacancies_hh, predict_rub_salary_hh


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("SUPER_JOB_API_KEY")

    languages = [
        "JavaScript",
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C#",
        "C",
        "Go",
    ]

    table_statistic_hh = []
    table_statistic_sj = []

    for language in languages:
        language_vacancies_hh = list(get_language_vacancies_hh(language))
        all_expected_salaries_hh = list(
            filter(lambda x: x, map(predict_rub_salary_hh, language_vacancies_hh))
        )
        table_hh: dict = get_language_statistic(
            language_vacancies_hh, all_expected_salaries_hh, language
        )
        table_statistic_hh.append(table_hh)

        language_vacancies_sj = list(get_language_vacancies_sj(language, api_key))
        all_expected_salaries_sj = list(
            filter(lambda x: x, map(predict_rub_salary_sj, language_vacancies_sj))
        )
        table_sj: dict = get_language_statistic(
            language_vacancies_sj, all_expected_salaries_sj, language
        )
        table_statistic_sj.append(table_sj)

    print("SuperJob")
    print(tabulate(table_statistic_sj, headers="keys", tablefmt="grid"))

    print("HeadHunter")
    print(tabulate(table_statistic_hh, headers="keys", tablefmt="grid"))
