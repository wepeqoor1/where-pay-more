from dotenv import load_dotenv

import superjob_salary
import headhunter_salary


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
    print('SuperJob')
    print(superjob_salary.get_salary_statistic_table(languages))
    print('HeadHunter')
    print(headhunter_salary.get_salary_statistic_table(languages))
    