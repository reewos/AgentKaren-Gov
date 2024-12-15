import requests

class GrokAPI:
    def __init__(self, api_key):
        self.model = "grok-2-1212"   #"grok-beta"
        self.api_key = api_key
        self.url = "https://api.x.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat_response(self, conversation):
        data = {
            "model": self.model,
            "messages": conversation,
            "temperature": 0
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def detect_sentiment(self, historial=[]):  #text='',
        prompt = "You are a sentiment analysis expert. Analyze the previous messages and always respond strictly with this structure: '[Sentiment level], [Topic]' where 'Sentiment level' can be High, Medium, or Low, and 'Topic' summarizes the main subject of the analyzed messages."
        messages =  historial + [
            {"role": "system", "content": prompt}
        ]

        data = {"model": self.model, "messages": messages, "temperature": 0}
        response = requests.post(self.url, headers=self.headers, json=data)
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]
        print(result)
        return result.split(",")