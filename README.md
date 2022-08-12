# where-pay-more
Search salaries in HeadHunter and SuperJob for popular programming languages:

## Environment requirements
Python3.10+

## How to install
```bash
$ pip install -r requirements.txt
```

## Environment variables
Create `.env` file.  
Sign up on https://api.superjob.ru/info/, get `api-key` and paste to `.env` file:  
SUPER_JOB_API_KEY=<`api-key`>  

# How to use
```bash
$ python3 main.py
```

After waiting, you can see salaries statistic from HeadHunter and SuperJob.
```bash
SuperJob
+-------------------------+--------------------+-----------------------+--------------------+
| Язык программирования   |   Вакансий найдено |   Вакансий обработано |   Средняя зарплата |
+=========================+====================+=======================+====================+
| JavaScript              |                 40 |                    24 |             133645 |
+-------------------------+--------------------+-----------------------+--------------------+
| Java                    |                 10 |                     5 |             217800 |
+-------------------------+--------------------+-----------------------+--------------------+
| Python                  |                 24 |                    16 |             177903 |
+-------------------------+--------------------+-----------------------+--------------------+
| Ruby                    |                  4 |                     2 |             264500 |
+-------------------------+--------------------+-----------------------+--------------------+
| PHP                     |                 22 |                    16 |             165270 |
+-------------------------+--------------------+-----------------------+--------------------+
| C#                      |                  6 |                     4 |             210000 |
+-------------------------+--------------------+-----------------------+--------------------+
| C                       |                 15 |                     9 |             145333 |
+-------------------------+--------------------+-----------------------+--------------------+
| Go                      |                  4 |                     2 |             252000 |
+-------------------------+--------------------+-----------------------+--------------------+
HeadHunter
+-------------------------+--------------------+-----------------------+--------------------+
| Язык программирования   |   Вакансий найдено |   Вакансий обработано |   Средняя зарплата |
+=========================+====================+=======================+====================+
| JavaScript              |               2000 |                   813 |             160986 |
+-------------------------+--------------------+-----------------------+--------------------+
| Java                    |               1628 |                   334 |             183734 |
+-------------------------+--------------------+-----------------------+--------------------+
| Python                  |               1368 |                   402 |             177442 |
+-------------------------+--------------------+-----------------------+--------------------+
| Ruby                    |                125 |                    47 |             173716 |
+-------------------------+--------------------+-----------------------+--------------------+
| PHP                     |               1093 |                   522 |             157738 |
+-------------------------+--------------------+-----------------------+--------------------+
| C#                      |                934 |                   283 |             160197 |
+-------------------------+--------------------+-----------------------+--------------------+
| C                       |               1600 |                   595 |             177992 |
+-------------------------+--------------------+-----------------------+--------------------+
| Go                      |                490 |                   147 |             215891 |
+-------------------------+--------------------+-----------------------+--------------------+
```