from config import TOKEN
import requests
import base64


class TextRequest:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.messages = []

    def send(self, text: str, model: str) -> dict:
        self.text = text
        self.model = model
        self.TOKEN = self.api_key
        self.url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }
        self.messages.append({"role": "user", "content": self.text})
        self.data = {
            "model": f"{self.model}",
            "messages": self.messages
        }
        self.response = requests.post(self.url, headers=self.headers, json=self.data)
        if self.response.status_code == 200:
            print(self.response.json()["choices"][0]["message"]["content"])
            self.messages.append({"role": "assistant", "content": self.response.json()["choices"][0]["message"]["content"]})
            print(self.messages)
        else:
            print(self.response.status_code)


class ImageRequest:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def send(self, text: str, image: str, model: str) -> dict:
        self.text = text
        self.image_data = image
        self.model = model
        self.TOKEN = self.api_key
        self.messages = []
        self.url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }
        self.messages.append({"role": "user", "content": [{"type": "text", "text": self.text}, {"type": "image_url", "image_url": self.image_data}]})
        self.data = {
            "model": f"{self.model}",
            "messages": self.messages
        }
        self.response = requests.post(self.url, headers=self.headers, json=self.data)
        if self.response.status_code == 200:
            print(self.response.json()["choices"][0]["message"]["content"])
            self.messages.append({"role": "assistant", "content": self.response.json()["choices"][0]["message"]["content"]})
        else:
            print(self.response.status_code, self.response.text)


class ChatFacade:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
    

    def select_mode(self) -> int:
        self.mode = input("Выберите режим работы: 1 - текст, 2 - текст и изображение: ")
        if self.mode == "1":
            return '1'
        return '2'

    def select_model(self, mode: int) -> str:
        self.models_1 = [
            "mistral-small-latest",
            "open-mistral-nemo",
            "open-codestral-mamba",
        ]
        self.models_2 = [
            "pixtral-12b-2409",
        ]
        print("Выберите модель:")
        if mode == '1':
            for i in range(len(self.models_1)):
                print(f"{i + 1}. {self.models_1[i]}")
            num = input()
            return self.models_1[int(num) - 1]
        else:
            for i in range(len(self.models_2)):
                print(f"{i + 1}. {self.models_2[i]}")
            num = input()
            return self.models_2[int(num) - 1]

    def load_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            self.image_data = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{self.image_data}"

    def ask_question(self, text: str, model: str, image: str = None) -> dict:
        self.text = text
        self.model = model
        self.image = image
        self.api_key = self.api_key
        if self.mode == '1':
            self.text_request = TextRequest(self.api_key)
            self.text_request.send(self.text, self.model)
        else:
            self.image_request = ImageRequest(self.api_key)
            self.image_request.send(self.text, self.image, self.model)

    def get_history(self) -> list[tuple[str, dict]]:
        pass

    def clear_history(self) -> None:
        pass


if __name__ == "__main__":
    api_key = TOKEN
    chat = ChatFacade(api_key)

    # Выбор режима
    mode = chat.select_mode()

    # Выбор модели
    model = chat.select_model(mode)

    # Если выбран режим с изображением, необходимо загрузить изображение
    image_path = None
    if mode == '2':
        print("Введите путь к изображению:")
        image_path = input()
        image_path = chat.load_image(image_path)

    # Отправка запроса
    while True:
        print("Введите текст вопроса (для выхода введите 'стоп'):")
        question = input()
        if question == 'стоп':
            break
        response = chat.ask_question(question, model, image_path)
