import superjob_salary
import headhunter_salary


if __name__ == '__main__':
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
    print(superjob_salary.start(languages))
    print(headhunter_salary.start(languages))