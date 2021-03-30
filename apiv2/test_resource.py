from requests import get, post, delete, put


def test_users_api():
    # Получение всех работ
    print(get('http://localhost:5000/api/v2/users').json())
    # Корректное получение одной работы
    print(get('http://localhost:5000/api/v2/user/4').json())

    # Ошибочный запрос на получение одной работы — неверный id
    print(get('http://localhost:5000/api/v2/user/0').json())
    # Ошибочный запрос на получение одной работы — строка
    print(get('http://localhost:5000/api/v2/user/tralala').json())


def test_users_post_api():
    # без аргументов
    print(post('http://localhost:5000/api/v2/users').json())
    # с некоректнымми аргументами
    print(post('http://localhost:5000/api/v2/users',
               json={'team_leader': 1, 'user': 'do_this'}).json())
    # с существующим ключом
    print(post('http://localhost:5000/api/v2/users',
               json={'team_leader': 1, 'user': 'do_this',
                     'work_size': 19, 'collaborators': '1,2,3',
                     'is_finished': False, 'id': 4}).json())
    # существует ли жобавленная ранее работа с индексом 4
    print(any(4 == item['id'] for item in get('http://localhost:5000/api/v2/users').json()['user']))


def test_users_delete_api():
    # добавление работы и ее удаление, проверка на то что она удалилась
    print(post('http://localhost:5000/api/v2/users',
               json={'id': 7, 'surname': 'Volotov', 'name': 'Volodya', 'age': 18}).json())
    print(any(7 == item['id'] for item in get('http://localhost:5000/api/v2/users').json()['user']))
    print(delete('http://localhost:5000/api/v2/user/7'))
    print(any(7 == item['id'] for item in get('http://localhost:5000/api/v2/users').json()['user']))

    # удаление несущ. работы
    print(delete('http://localhost:5000/api/v2/users/0'))


test_users_api()
