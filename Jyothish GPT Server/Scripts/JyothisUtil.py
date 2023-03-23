from langchain import OpenAI
import os
import openai
import logging
import logging.config
os.environ['OPENAI_API_KEY'] = open("Jyothish GPT Server\OpenAI_Key.txt", "r").read()
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
FinalAnswer = ""
completion = ""
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


""" def Secondcall(Newquery, FinalAnswer):
  completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": Newquery}]
   
)
#FinalAnswer = completion.choices[0].message
print(ChatAIResponsePrefix)
print(completion.choices[0].message) """
  
  
#ask_bot function
def ask_bot(query):
  input_index = 'JyothishKT.json'
  index = GPTSimpleVectorIndex.load_from_disk(input_index)
  while True:

    
    #Get the first response 
    response = index.query(query,text_qa_template = QA_PROMPT, similarity_top_k = 2, response_mode="compact")
    logger.info("---------------------")
    logger.info(f"Query: {query}")
    logger.info(f"Response: {response}")
    #Refine the response from source node with GPT List index
    for i, sn in enumerate(response.source_nodes):
        logger.info(f"Source Node: {sn}")
        index2 = GPTListIndex([readers.Document(sn.source_text)], llm_predictor=llm_predictor2)
        if i == 0:
            REFINE_PROMPT_TMPL = (
                "The original question is as follows: {query_str}\n"
                f"We have provided an existing answer: {response} \n"
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
            #Get the refined response
            response2 = index2.query(query, text_qa_template = REFINE_PROMPT)
            logger.info(f"Response: {response2}")
            #To check the refined answer
            if(response.response == "I don't know."):
               Findcode2 = response2.response.find('The answer is')
            else:
              Findcode2 = response2.response.find('Refined answer')
            #If refined answer if good, display to the user  
            if ((Findcode2) != -1):
               logger.info(f"Response: {response2}")
               print ("\nJyothish GPT says: \n\n" + response2.response + "\n\n\n")
               FinalAnswer = response2.response
            #Else give the original answer to the user  
            else:
              logger.info(f"Response: {response}")
              print ("\nJyothish GPT says: \n\n" + response.response + "\n\n\n")
              FinalAnswer = response.response
    return FinalAnswer
    #If the firstresponse is I don't know and also not able to refine the answer from source node, call ChatGPT      
    FirstResponse = response.response
    if FirstResponse == " I don't know." and Findcode2 == -1:
      Newquery = query
      #Secondcall(Newquery, FinalAnswer)
    return FinalAnswer

# When don't find answer in the .json file call this function 
""" def Secondcall(Newquery):
  completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": Newquery}]     
)
FinalAnswer = completion.choices[0].text
print(ChatAIResponsePrefix)
print(completion.choices[0].text)  """ 
query = input('What do you want to ask the Jyothish GPT?   \n')
ask_bot(query)
