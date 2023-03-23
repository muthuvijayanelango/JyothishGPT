#from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
#from gpt_index import QuestionAnswerPrompt
#from gpt_index import GPTSimpleVectorIndex
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, QuestionAnswerPrompt
from langchain import OpenAI
import sys
#from google.colab import drive
import os
import openai
query = ""
Newquery = ""
FirstResponse =""
ChatAIResponsePrefix = "I am not trained for this data in Jyothish AI model. However, I am giving below answer from ChatGPT Language AI Model"
os.environ["OPENAI_API_KEY"] = open("Jyothish GPT Server\OpenAI_Key.txt", "r").read()
openai.api_key = open("Jyothish GPT Server\OpenAI_Key.txt", "r").read()
directory_path = "Jyothish GPT Server\data"
QA_PROMPT_TMPL = (
        "Answer the question as truthfully as possible using the provided text, and if the answer is not contained "
        "within the text below, say \"I don't know\" \n"
        "---------------------\n"
        "Context:\n"
        "{context_str}"
        "\n---------------------\n"
        "Given the context information and not prior knowledge, "
        "Q: {query_str}\n A:"
    )
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
def construct_index(directory_path):
   # set maximum input size
  max_input_size = 4096
   # set number of output tokens
  num_outputs = 256
   # set maximum chunk overlap
  max_chunk_overlap = 20
   # set chunk size limit
  chunk_size_limit = 600

  prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

   # define LLM
  llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-ada-001", max_tokens=num_outputs))
  
  documents = SimpleDirectoryReader(directory_path).load_data()

   
  index = GPTSimpleVectorIndex(documents,text_qa_template=QA_PROMPT, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
  
  index.save_to_disk('Friendlyneutralenemy.json')
  
  return index
#index = construct_index("Jyothish GPT Server\data")

def Secondcall(Newquery):
  completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", 
  messages=[{"role": "user", "content": Newquery}]
   
)
  print(ChatAIResponsePrefix)
  print(completion.choices[0].message)

def ask_bot(input_index = 'Friendlyneutralenemy.json'):
  #index = GPTSimpleVectorIndex.load_from_disk(input_index)
  index = GPTSimpleVectorIndex.load_from_disk(input_index)
  
  while True:
    query = input('What do you want to ask the Jyothish GPT?   \n')
    response = index.query(query,text_qa_template = QA_PROMPT, response_mode="compact")
    FirstResponse = response.response
    if(FirstResponse == " I don't know."):
      Newquery = query
      Secondcall(Newquery)
    else:
      print ("\nJyothish GPT says: \n\n" + response.response + "\n\n\n")
    return response.response
  

      
  
# def Secondcall(Newquery):
#   completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo", 
#   messages=[{"role": "user", "content": Newquery}]



  


ask_bot('Friendlyneutralenemy.json')