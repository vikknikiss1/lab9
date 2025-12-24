import requests
import pytest
import json

# Базовый URL API
BASE_URL = "https://jsonplaceholder.typicode.com"

# ====== ФУНКЦИИ ДЛЯ ОТПРАВКИ ЗАПРОСОВ ======

def get_user(user_id):
    """GET-запрос для получения пользователя по ID"""
    url = f"{BASE_URL}/users/{user_id}"
    response = requests.get(url)
    return response

def create_user(user_data):
    """POST-запрос для создания пользователя"""
    url = f"{BASE_URL}/users"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=user_data, headers=headers)
    return response

def update_user(user_id, user_data):
    """PUT-запрос для обновления пользователя"""
    url = f"{BASE_URL}/users/{user_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=user_data, headers=headers)
    return response

# ====== ТЕСТЫ ДЛЯ GET-ЗАПРОСА ======

class TestGetUser:
    """Тестирование GET /users/{id}"""
    
    def test_status_code(self):
        """Тест 1: Проверка кода статуса (должен быть 200)"""
        response = get_user(1)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    
    def test_response_structure(self):
        """Тест 2: Проверка структуры JSON (наличие обязательных полей)"""
        response = get_user(1)
        user_data = response.json()
        
        # Проверяем, что это словарь
        assert isinstance(user_data, dict), "Ответ должен быть JSON-объектом"
        
        # Проверяем наличие обязательных полей верхнего уровня
        required_fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']
        for field in required_fields:
            assert field in user_data, f"Отсутствует обязательное поле: {field}"
        
        # Проверяем структуру вложенного объекта address
        address_fields = ['street', 'suite', 'city', 'zipcode', 'geo']
        for field in address_fields:
            assert field in user_data['address'], f"Отсутствует поле address.{field}"
    
    def test_user_id_correct(self):
        """Тест 3: Проверка, что ID пользователя корректен (должен быть 1)"""
        response = get_user(1)
        user_data = response.json()
        assert user_data['id'] == 1, f"Ожидался id=1, получен id={user_data['id']}"
    
    def test_email_format(self):
        """Тест 4: Проверка формата email (должен содержать '@')"""
        response = get_user(1)
        user_data = response.json()
        assert '@' in user_data['email'], f"Email {user_data['email']} не содержит символ '@'"

# ====== ТЕСТЫ ДЛЯ POST-ЗАПРОСА ======

class TestCreateUser:
    """Тестирование POST /users"""
    
    @pytest.fixture
    def new_user_data(self):
        """Фикстура: данные для создания нового пользователя"""
        return {
            "name": "Viks Nikishina",
            "username": "vikknikiss",
            "email": "v.nikishina58@mail.ru"
        }
    
    def test_status_code_created(self, new_user_data):
        """Тест 1: Проверка кода статуса (должен быть 201 Created)"""
        response = create_user(new_user_data)
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
    
    def test_response_structure_post(self, new_user_data):
        """Тест 2: Проверка структуры ответа (должны быть id, name, username, email)"""
        response = create_user(new_user_data)
        user_data = response.json()
        
        required_fields = ['id', 'name', 'username', 'email']
        for field in required_fields:
            assert field in user_data, f"Отсутствует поле: {field}"
    
    def test_data_matches_request(self, new_user_data):
        """Тест 3: Проверка, что данные в ответе совпадают с отправленными"""
        response = create_user(new_user_data)
        created_user = response.json()
        
        assert created_user['name'] == new_user_data['name']
        assert created_user['username'] == new_user_data['username']
        assert created_user['email'] == new_user_data['email']
    
    def test_id_is_numeric(self, new_user_data):
        """Тест 4: Проверка, что id является числом и был присвоен сервером"""
        response = create_user(new_user_data)
        user_data = response.json()
        
        assert isinstance(user_data['id'], int), "Поле id должно быть целым числом"
        assert user_data['id'] > 0, "ID должен быть положительным числом"

# ====== ТЕСТЫ ДЛЯ PUT-ЗАПРОСА ======

class TestUpdateUser:
    """Тестирование PUT /users/{id}"""
    
    @pytest.fixture
    def updated_user_data(self):
        """Фикстура: данные для обновления пользователя"""
        return {
            "name": "Updated Name",
            "username": "updated_user",
            "email": "updated.email@example.com"
        }
    
    def test_status_code_ok(self, updated_user_data):
        """Тест 1: Проверка кода статуса (должен быть 200 OK)"""
        response = update_user(1, updated_user_data)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    
    def test_response_structure_put(self, updated_user_data):
        """Тест 2: Проверка структуры ответа после обновления"""
        response = update_user(1, updated_user_data)
        user_data = response.json()
        
        required_fields = ['id', 'name', 'username', 'email']
        for field in required_fields:
            assert field in user_data, f"Отсутствует поле: {field}"
    
    def test_updated_id_correct(self, updated_user_data):
        """Тест 3: Проверка, что ID обновленного пользователя корректен (должен быть 1)"""
        response = update_user(1, updated_user_data)
        user_data = response.json()
        assert user_data['id'] == 1, f"Ожидался id=1, получен id={user_data['id']}"
    
    def test_data_matches_updated(self, updated_user_data):
        """Тест 4: Проверка, что данные в ответе совпадают с обновленными данными"""
        response = update_user(1, updated_user_data)
        updated_user = response.json()
        
        assert updated_user['name'] == updated_user_data['name']
        assert updated_user['username'] == updated_user_data['username']
        assert updated_user['email'] == updated_user_data['email']
    
    def test_updated_email_format(self, updated_user_data):
        """Тест 5: Проверка формата email после обновления"""
        response = update_user(1, updated_user_data)
        user_data = response.json()
        assert '@' in user_data['email'], f"Email {user_data['email']} не содержит символ '@'"

if __name__ == "__main__":
    # Запуск тестов напрямую из файла (альтернатива pytest в терминале)
    pytest.main(["-v", __file__])