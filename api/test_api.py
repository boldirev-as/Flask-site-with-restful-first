from requests import get, post, delete, put


def test_users_api():
    # Получение всех работ
    print(get('http://localhost:5000/api/users').json())
    # Корректное получение одной работы
    print(get('http://localhost:5000/api/user/4').json())

    # Ошибочный запрос на получение одной работы — неверный id
    print(get('http://localhost:5000/api/user/0').json())
    # Ошибочный запрос на получение одной работы — строка
    print(get('http://localhost:5000/api/user/tralala').json())


def test_users_post_api():
    # без аргументов
    print(post('http://localhost:5000/api/users').json())
    # с некоректнымми аргументами
    print(post('http://localhost:5000/api/users',
               json={'team_leader': 1, 'user': 'do_this'}).json())
    # с существующим ключом
    print(post('http://localhost:5000/api/users',
               json={'team_leader': 1, 'user': 'do_this',
                     'work_size': 19, 'collaborators': '1,2,3',
                     'is_finished': False, 'id': 4}).json())
    # существует ли жобавленная ранее работа с индексом 4
    print(any(4 == item['id'] for item in get('http://localhost:5000/api/users').json()['user']))


def test_users_delete_api():
    # добавление работы и ее удаление, проверка на то что она удалилась
    print(post('http://localhost:5000/api/users',
               json={'team_leader': 1, 'user': 'do_this',
                     'work_size': 19, 'collaborators': '1,2,3',
                     'is_finished': False, 'id': 4}).json())
    print(any(4 == item['id'] for item in get('http://localhost:5000/api/users').json()['users']))
    print(delete('http://localhost:5000/api/users/4'))
    print(any(4 == item['id'] for item in get('http://localhost:5000/api/users').json()['users']))

    # удаление несущ. работы
    print(delete('http://localhost:5000/api/users/0'))


def test_users_put_api():
    print(post('http://localhost:5000/api/users',
               json={'team_leader': 1, 'user': 'do_this',
                     'work_size': 19, 'collaborators': '1,2,3',
                     'is_finished': False, 'id': 4}).json())
    print(put('http://localhost:5000/api/users/4',
              json={'team_leader': 1, 'user': 'do_this',
                    'work_size': 19, 'collaborators': '1,2,3',
                    'is_finished': True}).json())
    print(get('http://localhost:5000/api/user/4').json()['users'])

    print(put('http://localhost:5000/api/users/0',
              json={'team_leader': 1, 'user': 'do_this',
                    'work_size': 19, 'collaborators': '1,2,3',
                    'is_finished': True}).json())


test_users_api()
