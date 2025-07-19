import os
import requests
from flask import Flask
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

app = Flask(__name__)

@app.route("/", methods=["GET"])
def send_quote():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = '1466112298'

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.9, model_name="gpt-4")
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a motivational quote generator."),
        ("human", "Give me one short, powerful motivational quote for the morning in under 20 words. No author needed.")
    ])
    messages = prompt_template.format_messages()
    response = llm(messages)
    quote = response.content.strip()

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🌞 *Morning Motivation*\n\n{quote}",
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

    return f"Quote sent: {quote}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
