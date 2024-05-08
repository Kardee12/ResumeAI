class ParsingFunctions:
    def init(self):
        self.HF_TOKEN = config('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')
        self.API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.headers = {"Authorization": f"Bearer {self.HF_TOKEN}"}
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    def query(self, payload):
        try:
            response = requests.post(self.API_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.RequestException as e:
            print(f"Request exception occurred: {e}")
        except Exception as e:
            print(f"Some other error occurred: {e}")
        return []
