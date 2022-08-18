from dotenv import load_dotenv
from tabulate import tabulate

from table_statistic_tools import get_language_statistic
from superjob_salary import get_language_vacancies_sj, predict_rub_salary_sj
from headhunter_salary import get_language_vacancies_hh, predict_rub_salary_hh


if __name__ == '__main__':
    load_dotenv()
    languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C#',
        'C',
        'Go',
    ]
    
    table_statistic_sj = []
    table_statistic_hh = []
    
    for language in languages:
        language_vacancies = list(get_language_vacancies_sj(language))
        all_expected_salaries = list(filter(lambda x: x, map(predict_rub_salary_sj, language_vacancies)))
        table: dict = get_language_statistic(language_vacancies, all_expected_salaries, language)
        table_statistic_sj.append(table)
        
    for language in languages:
        language_vacancies = list(get_language_vacancies_hh(language))
        all_expected_salaries = list(filter(lambda x: x, map(predict_rub_salary_hh, language_vacancies)))
        table: dict = get_language_statistic(language_vacancies, all_expected_salaries, language)
        table_statistic_hh.append(table)
        
    print('SuperJob')
    print(tabulate(table_statistic_sj, headers='keys', tablefmt="grid"))
        
    print('HeadHunter')
    print(tabulate(table_statistic_hh, headers='keys', tablefmt="grid"))
