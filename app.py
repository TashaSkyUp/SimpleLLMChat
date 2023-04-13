from config import Config
from flask import Flask, request, jsonify, render_template
import openai
import os
import uuid

# read context.txt file
with open('context.txt', 'r') as file:
    context = file.read()
context_message = {"role": "system", "content": context}
app = Flask(__name__)

openai.organization = Config.organization
openai.api_key = Config.api_key


history = {}


# define chat route
@app.route('/chat', methods=['POST'])
def chat():
    global history
    # get user input message from POST request
    message = request.get_json()['message']
    try:
        id = request.get_json()['id']
        if id not in history:
            raise KeyError("ID not found this shouldn't happen")

    except KeyError:
        id = uuid.uuid4().__str__()
        history[id] = []

    if message == "start" or message == "done":
        history[id] = []

    history[id].append({"role": "user", "content": message})

    out_messages = [context_message]
    for item in history[id]:
        out_messages.append(item)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=out_messages
    )
    gpt_message = response["choices"][0]["message"]["content"].strip()
    history[id].append({"role": "assistant", "content": gpt_message})
    # return AI response to client
    return jsonify({'response': gpt_message, 'id': id})


# define index route
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9443)
