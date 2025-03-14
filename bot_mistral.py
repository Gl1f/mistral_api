from config import TOKEN
import requests
import base64


class TextRequest:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def send(self, text: str, model: str) -> dict:
        self.text = text
        self.model = model
        self.TOKEN = self.api_key
        self.url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }
        self.data = {
            "model": f'{self.model}',
            "temperature": 0.7,
            "max_tokens": 400,
            "messages": [
                {
                    "role": "user",
                    "content": self.text,
                }
            ],
        }
        self.response = requests.post(self.url, headers=self.headers, json=self.data)
        if self.response.status_code == 200:
            print(self.response.json()["choices"][0]["message"]["content"])
        else:
            print(self.response.status_code)


class ImageRequest:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def send(self, text: str, imahe_path: str, model: str) -> dict:
        self.text = text
        self.image_path = imahe_path
        with open(self.image_path, "rb") as image_file:
            self.image_data = base64.b64encode(image_file.read()).decode("utf-8")
        self.image_data = f"data:image/jpeg;base64,{self.image_data}"
        self.model = model
        self.TOKEN = self.api_key
        self.url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
        }
        self.data = {
            "model": f'{self.model}',
            "temperature": 0.7,
            "max_tokens": 400,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.text},
                        {"type": "image_url", "image_url": self.image_data}
                    ],
                },
            ],
        }
        self.response = requests.post(self.url, headers=self.headers, json=self.data)
        if self.response.status_code == 200:
            print(self.response.json()["choices"][0]["message"]["content"])
        else:
            print(self.response.status_code, self.response.text)


models = [
    "mistral-small-latest",
    "pixtral-12b-2409",
    "open-mistral-nemo",
    "open-codestral-mamba",
]
TOKEN = TOKEN
f = ImageRequest(TOKEN)
print("Привет, вы хотите написать запрос в чат бот Mistral?")
answer = input()
if answer.lower() == "да" or answer.lower() == "yes":
    while True:
        text = input("Введите ваш запрос: ")
        print("Выберите модель:")
        for i in range(len(models)):
            print(f"{i + 1}. {models[i]}")
        num = input()
        f.send(text, "123.jpg", models[int(num) - 1])
        answer = input("Хотите продолжить?")
        if answer.lower() == "да" or answer.lower() == "yes":
            continue
        else:
            break