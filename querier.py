from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class Querier:
    def __init__(self):
        API_KEY = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=API_KEY)
    
    def query(self, prompt):
        assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
        assistant = self.client.beta.assistants.retrieve(assistant_id)
        run = self.client.beta.threads.create_and_run(
            assistant_id=assistant.id,
            thread={
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            }
        )
        while run.status != 'completed':
            run = self.client.beta.threads.runs.retrieve(run_id=run.id, thread_id=run.thread_id)
        messages = self.client.beta.threads.messages.list(run.thread_id)
        response = messages.data[0].content[0].text.value
        return response