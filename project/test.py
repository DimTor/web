from requests import get, post, delete


print(get('http://127.0.0.1:5000/api/v2/users').json())
print(get('http://127.0.0.1:5000/api/v2/users/2').json())
print(get('http://127.0.0.1:5000/api/v2/users/ll').json())
print(get('http://127.0.0.1:5000/api/v2/users/77').json())
# корректный запрос
