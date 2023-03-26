from flask import Flask
import env
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
import os
import logging
import openai
import logging.config
from llama_index.langchain_helpers.chatgpt import ChatGPTLLMPredictor
#from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, QuestionAnswerPrompt, GPTListIndex
from llama_index import GPTSimpleVectorIndex, QuestionAnswerPrompt, GPTListIndex, readers, LLMPredictor
index = ""
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
#llm_predictor2 = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo"))
llm_predictor2 = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
logger = logging.getLogger('My_Logger')
app = Flask(__name__)

@app.route('/ask_bot/<query>', methods=['GET'])
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
             
    if(FinalAnswer == "I don't know."):
      FinalAnswer = FinalAnswer + ". I am not trained for this query in Jyothish GPT. Try refining your query with more appropriate context"            
    return str(FinalAnswer)

# Run Server
if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
