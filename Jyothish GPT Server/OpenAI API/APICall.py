import requests
import openai
openai.api_key = open("Jyothish GPT Server\OpenAI_Key.txt", "r").read()
URL = "https://api.openai.com/v1/chat/completions"
#URL = "https://api.openai.com/v1/completions"

payload = {
#"model": "gpt-3.5-turbo",
"model": "ada:ft-personal-2023-03-03-05-27-06",
"messages": [{"role": "user", "content": f"What is the 24th Nakshatra?"}],
"temperature" : 1.0,
"top_p":1.0,
"n" : 1,
"stream": False,
"presence_penalty":0,
"frequency_penalty":0,
}

headers = {
"Content-Type": "application/json",
"Authorization": f"Bearer {openai.api_key}"
}
Mymodel = "ada:ft-personal-2023-03-03-05-27-06"
response = openai.Completion.create(
    model = Mymodel,
    #prompt = "Q:What is the 24th Nakshatra?\n A:"
    prompt = f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: \n\n---\n\nQuestion: Who is the author of Jyothisha?\nAnswer:"
)  
print(response['choices'][0]['text'])
# response.content
# print(response.content)

#response = requests.post(URL, headers=headers, json=payload, stream=True)
