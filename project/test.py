from requests import get, post, delete


print(get('http://127.0.0.1:5000/api/v2/users').json())  # корректный запрос
print(get('http://127.0.0.1:5000/api/v2/users/2').json())  # корректный запрос
print(get('http://127.0.0.1:5000/api/v2/users/ll').json())   # некорректный запрос
print(get('http://127.0.0.1:5000/api/v2/users/77').json())   # некорректный запрос
print(post('http://127.0.0.1:5000/api/v2/users', json={'name': 'Dima',
                                                          'surname': 'Tor', 'age': 17,
                                                          'position': 'module_2', 'speciality': 'programmer',
                                                          'address': 'Moscow', 'email': 'dim@maes.ru'}).json())
print(post('http://127.0.0.1:5000/api/v2/users', json={'name': 'Dima',
                                                          'surname': 'Tor', 'age': 17,
                                                          'position': 'module_2', 'speciality': 'programmer',
                                                          'address': 'Moscow'}).json())
print(get('http://127.0.0.1:5000/api/v2/users').json())
print(delete('http://127.0.0.1:5000/api/v2/users/9').json())
print(get('http://127.0.0.1:5000/api/v2/users').json())