import pytest
import requests
#Создание переменной с сылкой для удобства написания
link = "https://jsonplaceholder.typicode.com/posts/"
class TestPosts:
    #Класс для эндпоинта /posts
    @pytest.fixture(scope="class")
    def session(self):
        #Фикстура для создания и закрытия сессии
        session = requests.Session()
        yield session
        session.close()

    class TestGet:
        #Тесты для GET-запросов

        @pytest.mark.parametrize("post_id", [10, 35, 100])
        def test_get_post_by_id_returns_200_and_valid_structure(self, session, post_id):
            #Позитивный тест: получение поста по валидному ID
            response = session.get(f"{link}{post_id}")
            
            assert response.status_code == 200
            data = response.json()
            
            # Проверка структуры JSON
            assert all(key in data for key in ["userId", "id", "title", "body"])
            assert isinstance(data["userId"], int)
            assert isinstance(data["id"], int)
            assert isinstance(data["title"], str)
            assert isinstance(data["body"], str)

        def test_get_non_existent_post_returns_404(self, session):
            #Негативный тест: получение несуществующего поста
            response = session.get(f"{link}9999")
            assert response.status_code == 404

        def test_get_all_posts_returns_200_and_list(self, session):
            #Позитивный тест: получение всех постов
            response = session.get(link)
            
            assert response.status_code == 200
            data = response.json()
            
            assert isinstance(data, list)
            assert len(data) > 0
            assert all("id" in post for post in data)

    class TestPost:
        #Тесты для POST-запросов

        @pytest.mark.parametrize("user_id, title, body", [
            (1, "Test Title", "Test Body"),
            (999, "Another Title", "Another Body")
        ])
        def test_create_post_returns_201_and_valid_data(self, session, user_id, title, body):
            #Позитивный тест: создание нового поста
            payload = {
                "userId": user_id,
                "title": title,
                "body": body
            }
            response = session.post(
                link,
                json=payload
            )
            
            assert response.status_code == 201
            data = response.json()
            
            # Проверка полученных данных
            assert data["userId"] == user_id
            assert data["title"] == title
            assert data["body"] == body
            assert "id" in data

    class TestPut:
        #Тесты для PUT-запросов

        @pytest.mark.parametrize("post_id, user_id, title, body", [
            (1, 1, "Updated Title", "Updated Body"),
            (1, 999, "New Title", "New Body")
        ])
        def test_update_post_returns_200_and_valid_data(self, session, post_id, user_id, title, body):
            #Позитивный тест: обновление существующего поста
            payload = {
                "userId": user_id,
                "title": title,
                "body": body
            }
            response = session.put(
                f"{link}{post_id}",
                json=payload
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Проверка обновленных данных
            assert data["userId"] == user_id
            assert data["title"] == title
            assert data["body"] == body
            assert data["id"] == post_id

    class TestDelete:
        #Тесты для DELETE-запросов

        def test_delete_post_returns_200(self, session):
            #Позитивный тест: удаление поста
            response = session.delete(f"{link}10")
            assert response.status_code == 200
