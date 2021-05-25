import requests
import json


base_url = "https://petfriends1.herokuapp.com/"

def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

    headers = {
        'email' : 'abrsmall@mail.ru',
        'password' : 'MastechMY60series',
    }
    res = requests.get(base_url + 'api/key', headers=headers)
    status = res.status_code
    result = ""
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return status, result



def bad_method_update_pet_info(self, auth_key: json, pet_id: str, name: str,
                               animal_type: str, age: int) -> json:
    """Проверяем запрос обновления информации с неправильным методом"""

    headers = {'auth_key': auth_key['key']}
    data = {
        'name': name,
        'age': age,
        'animal_type': animal_type
    }

    res = requests.post(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
    status = res.status_code
    return print(res)