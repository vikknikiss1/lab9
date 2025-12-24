import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


class TestRegistration:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        print("Запуск браузера")
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        print("Браузер запущен")
        
        file_path = os.path.abspath("logpo3.html")
        self.driver.get(f"file:///{file_path}")
        print("Страница открыта")
        time.sleep(3)
        
        yield
        
        self.driver.quit()
        print("Браузер закрыт")
    
    def test1(self):
        """Тест успешной регистрации"""
        # Ввод данных
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys("test@example.com")
        
        phone_input = self.driver.find_element(By.ID, "phone")
        phone_input.send_keys("+79123456789")
        
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("StrongPass123!")
        
        confirm_password_input = self.driver.find_element(By.ID, "confirmPassword")
        confirm_password_input.send_keys("StrongPass123!")
        
        # Ожидание активации кнопки
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "submitBtn"))
        )
        
        # Нажатие кнопки регистрации
        submit_btn.click()
        
        # Проверка успешной регистрации
        success_message = self.driver.find_element(By.ID, "successMessage")
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of(success_message)
        )
        
        assert success_message.is_displayed()
        assert success_message.text == "Регистрация прошла успешно!"
        print("Тест успешной регистрации пройден")
    
    def test_invalid_email(self):
        """Тест с некорректным вводом почты"""
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys("invalid-email")
        
        # Проверка отображения ошибки
        email_error = self.driver.find_element(By.ID, "emailError")
        assert email_error.is_displayed()
        assert email_error.text == "Введите корректный email адрес"
        
        # Проверка что кнопка заблокирована
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        assert not submit_btn.is_enabled()
        print("Тест с некорректным email пройден")
    
    def test_password_mismatch(self):
        """Тест с несовпадающими паролями"""
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("Password123")
        
        confirm_password_input = self.driver.find_element(By.ID, "confirmPassword")
        confirm_password_input.send_keys("DifferentPassword")
        
        # Проверка отображения ошибки
        confirm_password_error = self.driver.find_element(By.ID, "confirmPasswordError")
        assert confirm_password_error.is_displayed()
        assert confirm_password_error.text == "Пароли не совпадают"
        
        # Проверка что кнопка заблокирована
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        assert not submit_btn.is_enabled()
        print("Тест с несовпадающими паролями пройден")
    
    def test_weak_password(self):
        """Тест со слабым паролем"""
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys("123")
        
        # Проверка отображения ошибки
        password_error = self.driver.find_element(By.ID, "passwordError")
        assert password_error.is_displayed()
        assert password_error.text == "Пароль должен содержать минимум 8 символов"
        
        # Проверка индикатора сложности пароля
        password_strength = self.driver.find_element(By.ID, "passwordStrength")
        assert "strength-weak" in password_strength.get_attribute("class")
        print("Тест со слабым паролем пройден")


# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v"])