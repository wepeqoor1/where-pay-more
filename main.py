from dotenv import load_dotenv
from table_statistic import get_salary_statistic_table


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
    print(get_salary_statistic_table(languages))
    print('HeadHunter')
    print(get_salary_statistic_table(languages))
    