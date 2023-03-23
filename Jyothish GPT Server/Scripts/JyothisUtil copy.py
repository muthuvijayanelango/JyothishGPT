from langchain import OpenAI
import os
import openai
import logging
import logging.config
os.environ['OPENAI_API_KEY'] = open("Jyothish GPT Server\OpenAI_Key.txt", "r").read()
#from gpt_index import download_loader
#from IPython.display import Markdown, display

#from llama_index.readers.schema.base import Document
import openai
#from gpt_index import GPTSimpleVectorIndex, GPTListIndex
#from gpt_index.langchain_helpers.chatgpt import ChatGPTLLMPredictor
from llama_index.langchain_helpers.chatgpt import ChatGPTLLMPredictor
#from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, QuestionAnswerPrompt, GPTListIndex
from llama_index import GPTSimpleVectorIndex, QuestionAnswerPrompt, GPTListIndex, readers, LLMPredictor
openai.api_key = open("Jyothish GPT Server\OpenAI_Key.txt", "r").read()
index = ""
directory_path = "Jyothish GPT Server\data"
query = ""
Newquery = ""
FirstResponse =""
Outputtext = ""
OldOutputtext = ""
ChatAIResponsePrefix = "I am not trained for this data in Jyothish AI model. However, I am giving below answer from ChatGPT Language AI Model"
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
llm_predictor = ChatGPTLLMPredictor(temperature=0)
llm_predictor2 = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo"))
logger = logging.getLogger('My_Logger')
 
def Secondcall(Newquery):
  completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": Newquery}]
   
)
  print(ChatAIResponsePrefix)
  print(completion.choices[0].message)

def ask_bot(input_index = 'JyothishKT.json'):
  
  index = GPTSimpleVectorIndex.load_from_disk(input_index)
  #index = GPTListIndex.load_from_disk(input_index)
 
  while True:
    query = input('What do you want to ask the Jyothish GPT?   \n')
    response = index.query(query,text_qa_template = QA_PROMPT, similarity_top_k = 2, response_mode="compact")
    logger.info("---------------------")
    logger.info(f"Query: {query}")
    logger.info(f"Response: {response}")
    for i, sn in enumerate(response.source_nodes):
        logger.info(f"Source Node: {sn}")
        index2 = GPTListIndex([readers.Document(sn.source_text)], llm_predictor=llm_predictor2)
        if i == 0:
            response2 = index2.query(query, text_qa_template = QA_PROMPT)
        else:
            REFINE_PROMPT_TMPL = (
                "The original question is as follows: {query_str}\n"
                f"We have provided an existing answer: {response2} \n"
                "We have the opportunity to refine the existing answer"
                "(only if needed) with some more context below.\n"
                "------------\n"
                "{context_str}\n"
                "------------\n"
                "Given the new context, refine the original answer to better "
                "answer the question. "
                "If the context isn't useful, return the original answer."
            )
            REFINE_PROMPT = QuestionAnswerPrompt(REFINE_PROMPT_TMPL)
            response2 = index2.query(query, text_qa_template=REFINE_PROMPT)
        logger.info(f"Response: {response2}")
    FirstResponse = response2.response
    if(FirstResponse == "I don't know."):
      Newquery = query
      Secondcall(Newquery)
    else:
      print ("\nJyothish GPT says: \n\n" + response.response + "\n\n\n")
    return response.response
  
ask_bot('JyothishKT.json')
