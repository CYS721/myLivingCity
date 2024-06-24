import profanity_check
import subprocess
import json

def generate_sentence(query):
    # Construct the POST data as a dictionary
    data = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": False
    }

    # Convert dictionary to JSON format
    json_data = json.dumps(data)

    # Construct the curl command
    curl_command = [
        'curl',
        'http://192.168.1.124:11434/api/chat',
        '-d', json_data,
        '-H', 'Content-Type: application/json'
    ]

    # Execute the curl command
    process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode == 0:
        return output
    else:
        return f"Error: {error.decode('utf-8')}"

def predict_profanity(comment):

    new_comment_list = []
    new_comment_list.append(comment)
    if profanity_check.predict(new_comment_list)[0] == 1:
        return 'Profane'
    else:
        return 'Not Profane'

def predict_profanity_llm(comment):
    prompt = "Given a sentence, analyze whether it has bad words (profanity checking) or not. You should only return Profane or Not Profane. Don't explain anything!!! The sentence is: "
    query = prompt + comment
    response = generate_sentence(query)
    response_data = json.loads(response)
    response_content = response_data["message"]["content"]
    return response_content

test_comment = "I love this song, it's so good"
print(predict_profanity(test_comment))
test_comment = "I love this song, it's so shit awesome"
print(predict_profanity(test_comment))