from requests import get, post, delete, put


def test_jobs_api():
    # Получение всех работ
    print(get('http://localhost:5000/api/v2/jobs').json())
    # Корректное получение одной работы
    print(get('http://localhost:5000/api/v2/job/5').json())

    # Ошибочный запрос на получение одной работы — неверный id
    print(get('http://localhost:5000/api/v2/job/0').json())
    # Ошибочный запрос на получение одной работы — строка
    print(get('http://localhost:5000/api/v2/job/tralala').json())


def test_jobs_post_api():
    # без аргументов
    print(post('http://localhost:5000/api/v2/jobs').json())
    # с некоректнымми аргументами
    print(post('http://localhost:5000/api/v2/jobs',
               json={'team_leader': 1, 'job': 'do_this'}).json())
    # с существующим ключом
    print(post('http://localhost:5000/api/v2/jobs',
               json={'team_leader': 1, 'job': 'do_this',
                     'work_size': 19, 'collaborators': '1,2,3',
                     'is_finished': False, 'id': 4}).json())
    # существует ли жобавленная ранее работа с индексом 4
    print(any(4 == item['id'] for item in get('http://localhost:5000/api/v2/jobs').json()['job']))


def test_jobs_delete_api():
    # добавление работы и ее удаление, проверка на то что она удалилась
    print(post('http://localhost:5000/api/v2/jobs',
               json={'team_leader': 1, 'job': 'do_this',
                     'work_size': 19, 'collaborators': '1,2,3',
                     'is_finished': False, 'id': 7}).json())
    print(any(7 == item['id'] for item in get('http://localhost:5000/api/v2/jobs').json()['job']))
    print(delete('http://localhost:5000/api/v2/job/7'))
    print(any(7 == item['id'] for item in get('http://localhost:5000/api/v2/jobs').json()['job']))

    # удаление несущ. работы
    print(delete('http://localhost:5000/api/v2/jobs/0'))


test_jobs_delete_api()
