from requests import get, post, delete


print(get('http://127.0.0.1:5000/api/v2/jobs').json())  # корректный запрос
print(get('http://127.0.0.1:5000/api/v2/jobs/2').json())  # корректный запрос
print(get('http://127.0.0.1:5000/api/v2/jobs/ll').json())   # некорректный запрос
print(get('http://127.0.0.1:5000/api/v2/jobs/77').json())   # некорректный запрос
print(post('http://127.0.0.1:5000/api/v2/jobs', json={'job': 'swimming',
                                                      'team_leader': 8, 'work_size': 14,
                                                      'collaborators': '1, 3, 5', 'is_finished': False}).json())
print(post('http://127.0.0.1:5000/api/v2/jobs', json={'job': 'swimming',
                                                      'team_leader': 8, 'work_size': 14,
                                                      'collaborators': '1, 3, 5'}).json())
print(get('http://127.0.0.1:5000/api/v2/jobs').json())
print(delete('http://127.0.0.1:5000/api/v2/jobs/12').json())
print(get('http://127.0.0.1:5000/api/v2/jobs').json())
print(delete('http://127.0.0.1:5000/api/v2/jobs/88').json())
print(delete('http://127.0.0.1:5000/api/v2/jobs/kk').json())
