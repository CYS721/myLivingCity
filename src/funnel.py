import numpy as np
import pandas as pd
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

funnel_prompt = "Given a sentence, analyze its tone as either 'Positive', 'Negative', or 'Neutral' and summarize the top keywords. Make sure Format your output as follows: 0. [Tone] | 1. [Attitude(present tense base form verb)] | 2. [Keyword1] | 3. [Keyword2] | 4. [Keyword3] | 5. [Keyword4] | 6. [Keyword5]\n Ensure that the keywords are relevant and capture the essence of the sentence. Make sure only use the singular form for noun and unchanged form for adjectives. Try to identify the agents (action initiators) and patients (action recipients) in keywords. Do not explain or give any other content! Just seven tag! You only only only need to give me the tags. The sentence is: "

# read the file line by line
# create a dataframe with the new comment and the new comment words
comment_tags_df = pd.DataFrame(columns=['comment', 'tone', 'attitude', 'keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5'])
with open('../Youtube_dataset/GBcomments.csv') as f:
    lines = f.readlines()
    # skip the first line and read the rest
    # loop through the lines and print the first 5 lines
    for line in lines[50:150]:
        # print the process of the loop every 1000 lines
        if lines.index(line) % 1000 == 0:
            print("Processing line", lines.index(line))
        # skip the content before the first comma, do not use split
        # skip the last two numbers which are the likes and replies
        new_comment = line[line.index(',')+2:line.rindex(',')-3]
        # print the first 5 lines
        query = funnel_prompt + new_comment
        response = generate_sentence(query)
        response_data = json.loads(response)
        response_content = response_data["message"]["content"].split('\n')[0].split(' | ')
        new_comment_words = []
        for item in response_content:
            try:
                new_comment_words.append(item.split('. ')[1])
            except IndexError:  
                continue  
        print(new_comment)
        print(new_comment_words)
        # make sure the new comment words are 7 in length, if not, add "None" to the list, if more than 7, ignore the rest
        if len(new_comment_words) < 7:
            new_comment_words += ['None'] * (7 - len(new_comment_words))
        elif len(new_comment_words) > 7:
            new_comment_words = new_comment_words[:7]
        # use concat to add the new comment and the new comment words to the dataframe
        comment_tags_df = pd.concat([comment_tags_df, pd.DataFrame([[new_comment] + new_comment_words], columns=['comment', 'tone', 'attitude', 'keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5'])], ignore_index=True)
        
# print the dataframe
print(comment_tags_df.head())
# store the dataframe in a csv file
comment_tags_df.to_csv('GB_comment_tags.csv', index=False)
        