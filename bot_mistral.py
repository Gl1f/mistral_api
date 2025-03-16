from typing import List, Dict, Union, Optional, Any, Tuple
from config import TOKEN
import requests
import base64


class TextRequest:
    """
    Класс для отправки текстовых запросов к API Mistral.
    
    Позволяет отправлять текстовые сообщения и получать ответы от моделей Mistral,
    а также сохраняет историю сообщений.
    """
    
    def __init__(self, api_key: str) -> None:
        """
        Инициализация объекта TextRequest.
        
        Args:
            api_key (str): Ключ API для доступа к сервису Mistral.
        """
        self.api_key: str = api_key
        self.messages: List[Dict[str, str]] = []

    def send(self, text: str, model: str) -> Dict[str, Any]:
        """
        Отправляет текстовый запрос к API Mistral.
        
        Args:
            text (str): Текст запроса.
            model (str): Название модели Mistral для обработки запроса.
            
        Returns:
            Dict[str, Any]: Ответ от API в формате словаря.
        """
        self.text: str = text
        self.model: str = model
        self.TOKEN: str = self.api_key
        self.url: str = "https://api.mistral.ai/v1/chat/completions"
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }
        self.messages.append({"role": "user", "content": self.text})
        self.data: Dict[str, Any] = {"model": f"{self.model}", "messages": self.messages}
        self.response: requests.Response = requests.post(self.url, headers=self.headers, json=self.data)
        if self.response.status_code == 200:
            print(self.response.json()["choices"][0]["message"]["content"])
            self.messages.append(
                {
                    "role": "assistant",
                    "content": self.response.json()["choices"][0]["message"]["content"],
                }
            )
        else:
            print(self.response.status_code)
        
        return self.response.json() if self.response.status_code == 200 else {}


class ImageRequest:
    """
    Класс для отправки запросов с изображениями к API Mistral.
    
    Позволяет отправлять текстовые сообщения вместе с изображениями
    и получать ответы от мультимодальных моделей Mistral.
    """
    
    def __init__(self, api_key: str) -> None:
        """
        Инициализация объекта ImageRequest.
        
        Args:
            api_key (str): Ключ API для доступа к сервису Mistral.
        """
        self.api_key: str = api_key

    def send(self, text: str, image: str, model: str) -> Dict[str, Any]:
        """
        Отправляет запрос с текстом и изображением к API Mistral.
        
        Args:
            text (str): Текст запроса.
            image (str): Изображение в формате base64 или URL.
            model (str): Название мультимодальной модели Mistral.
            
        Returns:
            Dict[str, Any]: Ответ от API в формате словаря.
        """
        self.text: str = text
        self.image_data: str = image
        self.model: str = model
        self.TOKEN: str = self.api_key
        self.messages: List[Dict[str, Any]] = []
        self.url: str = "https://api.mistral.ai/v1/chat/completions"
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }
        self.messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": self.text},
                    {"type": "image_url", "image_url": self.image_data},
                ],
            }
        )
        self.data: Dict[str, Any] = {"model": f"{self.model}", "messages": self.messages}
        self.response: requests.Response = requests.post(self.url, headers=self.headers, json=self.data)
        if self.response.status_code == 200:
            print(self.response.json()["choices"][0]["message"]["content"])
            self.messages.append(
                {
                    "role": "assistant",
                    "content": self.response.json()["choices"][0]["message"]["content"],
                }
            )
        else:
            print(self.response.status_code, self.response.text)
            
        return self.response.json() if self.response.status_code == 200 else {}


class ChatFacade:
    """
    Фасад для взаимодействия с API Mistral.
    
    Предоставляет унифицированный интерфейс для работы с текстовыми
    и мультимодальными моделями Mistral, управления историей сообщений
    и обработки изображений.
    """
    
    def __init__(self, api_key: str) -> None:
        """
        Инициализация объекта ChatFacade.
        
        Args:
            api_key (str): Ключ API для доступа к сервису Mistral.
        """
        self.api_key: str = api_key
        self.mode: str = "1"
        self.text_request: Optional[TextRequest] = None
        self.image_request: Optional[ImageRequest] = None

    def select_mode(self) -> str:
        """
        Выбор режима работы: текст или текст с изображением.
        
        Returns:
            str: "1" для текстового режима, "2" для режима с изображением.
        """
        self.mode = input("Выберите режим работы: 1 - текст, 2 - текст и изображение: ")
        if self.mode == "1":
            return "1"
        return "2"

    def select_model(self, mode: str) -> str:
        """
        Выбор модели Mistral в зависимости от режима работы.
        
        Args:
            mode (str): Режим работы ("1" - текст, "2" - текст с изображением).
            
        Returns:
            str: Название выбранной модели.
        """
        self.models_1: List[str] = [
            "mistral-small-latest",
            "open-mistral-nemo",
            "open-codestral-mamba",
        ]
        self.models_2: List[str] = [
            "pixtral-12b-2409",
        ]
        print("Выберите модель:")
        if mode == "1":
            self.text_request = TextRequest(self.api_key)
            for i in range(len(self.models_1)):
                print(f"{i + 1}. {self.models_1[i]}")
            num = input()
            return self.models_1[int(num) - 1]
        else:
            self.image_request = ImageRequest(self.api_key)
            for i in range(len(self.models_2)):
                print(f"{i + 1}. {self.models_2[i]}")
            num = input()
            return self.models_2[int(num) - 1]

    def load_image(self, image_path: str) -> Optional[str]:
        """
        Загружает изображение из файла и кодирует его в base64.
        
        Args:
            image_path (str): Путь к файлу изображения.
            
        Returns:
            Optional[str]: Закодированное изображение в формате data URL или None в случае ошибки.
        """
        try:
            with open(image_path, "rb") as image_file:
                self.image_data: str = base64.b64encode(image_file.read()).decode("utf-8")
            return f"data:image/jpeg;base64,{self.image_data}"
        except FileNotFoundError:
            print("Файл не найден")
            return None
        except Exception as e:
            print(f"Ошибка: {e}")
            return None

    def ask_question(self, text: str, model: str, image: Optional[str] = None) -> Dict[str, Any]:
        """
        Отправляет запрос к API Mistral в зависимости от выбранного режима.
        
        Args:
            text (str): Текст запроса.
            model (str): Название модели Mistral.
            image (Optional[str]): Изображение в формате data URL (только для режима с изображением).
            
        Returns:
            Dict[str, Any]: Ответ от API в формате словаря.
        """
        self.text: str = text
        self.model: str = model
        self.image: Optional[str] = image
        if self.mode == "1":
            return self.text_request.send(self.text, self.model)
        else:
            return self.image_request.send(self.text, self.image, self.model)

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Получает историю сообщений.
        
        Returns:
            List[Dict[str, Any]]: Список сообщений в формате словарей.
        """
        if self.mode == "1":
            return self.text_request.messages
        else:
            return self.image_request.messages

    def clear_history(self) -> None:
        """
        Очищает историю сообщений.
        """
        if self.mode == "1":
            self.text_request.messages = []
        else:
            self.image_request.messages = []


if __name__ == "__main__":
    api_key: str = TOKEN
    chat: ChatFacade = ChatFacade(api_key)

    # Выбор режима
    mode: str = chat.select_mode()

    # Выбор модели
    model: str = chat.select_model(mode)

    # Если выбран режим с изображением, необходимо загрузить изображение
    image_path: Optional[str] = None
    if mode == "2":
        while not image_path:
            print("Введите путь к изображению:")
            image_path_input: str = input()
            image_path = chat.load_image(image_path_input)

    # Отправка запроса
    while True:
        print("Выберите опцию (для выхода введите 'стоп'):")
        print("1. Отправить запрос")
        print("2. Получить историю")
        print("3. Очистить историю")
        question: str = input()
        if question == "1":
            print("Введите вопрос:")
            question = input()
            response: Dict[str, Any] = chat.ask_question(question, model, image_path)
        elif question == "2":
            print("История:")
            data: List[Dict[str, Any]] = chat.get_history()
            for message in data:
                if message["role"] == "user":
                    print(f"Вы: {message['content']}")
                else:
                    print(f"Бот: {message['content']}")
        elif question == "3":
            chat.clear_history()
        elif question == "стоп":
            break
        else:
            print("Неверный ввод")
            continue
