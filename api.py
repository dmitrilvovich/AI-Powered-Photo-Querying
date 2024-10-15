from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/search', methods=['GET'])
def search_images():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    openai.api_key = os.getenv('OPENAI_API_KEY')
    directory = #insert text descriptions directory
    file_contents = []

    #retrieving the text descriptions of the images
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                content = file.read()
                file_contents.append(f"Filename: {filename}\nContent:\n{content}")

    #getting the matching file names from OpenAI
    response = openai.chat.completions.create(
        model='gpt-4o', 
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Give the file names that best matches this query: " + query},
                    {"type": "text", "text": "\n\n".join(file_contents)}
                ],
            }
        ],
        max_tokens=4000,
    )

    #filtering and outputting OpenAI's response 
    output = response.choices[0].message.content
    matched_images = list(set(re.findall(r'\d{13}\.txt', output)))
    jpg_files = [file.replace('.txt', '.jpg') for file in matched_images] 
    print(output)
    print(jpg_files)
    return jsonify(jpg_files)

if __name__ == '__main__':
    app.run()
