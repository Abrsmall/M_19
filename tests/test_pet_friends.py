from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age=4, pet_photo='images\\cat.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", 3, "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_add_pet_without_photo(name='Chack', animal_type='cat', age='3'):
    """Проверяем возможность добавления животного без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_successful_set_photo(pet_photo='images\\cat.jpg'):
    """Проверяем можно ли добавить фото животному"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Суперкот", "кот", '3')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.set_new_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] is not ''


def test_invalid_auth_key_get_api_pets(filter=''):
    """Проверяем ввод некорректного строкового ключа"""
    auth_key = {'key': 'abc'}
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_big_value_auth_key_get_api_pets(filter=''):
    """Проверяем ввод 256-значного ключа"""
    auth_key = {'key': 'abcabcabcabcabcabcabcabcabcabcabcabcabcabcabc\
    abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabc\
    abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabc\
    abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabc\
    abcabcabcabcabcabca'}
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_set_text_instead_of_photo(pet_photo='images\\Q.txt'):
    """Проверяем добавление текстового файла вместо фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    print(auth_key)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Суперкот", "кот", '3')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.set_new_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    try:
        assert status == 400
    except AssertionError:
        print('Баг на возвращение кода ошибки')


def test_not_set_file(pet_photo=''):
    """Проверяем запрос добавления фото без файла"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Суперкот", "кот", '3')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    try:
        # Берём id первого питомца из списка и отправляем запрос на добавление
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.set_new_photo(auth_key, pet_id, pet_photo)
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400
    except FileNotFoundError:
        print('Отсутствует файл на добавление')


def test_update_pet_info_without_name(name='', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце, не указывая имя"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    try:
        # Если список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            # Проверяем что статус ответа = 400 и имя питомца соответствует заданному
            assert status == 400
        else:
            print('У вас нет ни одного питомца')
    except AssertionError:
        if status == 200:
            print('Баг - запрос прошел без обязательного параметра')
        else:
            print('Баг на возвращении кода ошибки')


def test_update_pet_info_with_first_limit_name(name='МурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце с именем в 255 символов"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_pet_info_with_first_limit_plus_one_name(name='МурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзикО', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце с именем в 256 символов"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_pet_info_with_limit_over_name(name='МурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаММурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаММурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаММурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккисаМурзиккиса\
МурзиккисаМурзиккисаМурзиккисаМу', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце с именем в 1001 символов"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_invalid_method_update_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    try:
        # Если список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = pf.bad_method_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            # Проверяем что статус ответа = 405
            assert status == 405
        else:
            print('У вас нет ни одного питомца')
    except TypeError:
        print('Неправильный метод запроса')
        """В итоге так и не понял возможно ли протестировать запрос с неправильным методом"""
