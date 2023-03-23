from llama_index.langchain_helpers.chatgpt import ChatGPTLLMPredictor
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, QuestionAnswerPrompt, GPTListIndex
from llama_index.readers.schema.base import Document
import openai
import logging
import logging.config
logger = logging.getLogger('My_Logger')
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
llm_predictor = ChatGPTLLMPredictor(temperature=0)
    # set maximum input size
max_input_size = 4096
   # set number of output tokens
num_outputs = 256
   # set maximum chunk overlap
max_chunk_overlap = 20
   # set chunk size limit
chunk_size_limit = 600
prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
#logging.config.fileConfig('../logging.conf', disable_existing_loggers=False)
#logger = logging.getLogger(__name__)

def construct_index(directory_path,llm_predictor,prompt_helper):
 
  documents = SimpleDirectoryReader(directory_path).load_data()
  
  #index = GPTListIndex(documents,llm_predictor=llm_predictor)
  index = GPTSimpleVectorIndex(documents,text_qa_template=QA_PROMPT, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
  logger.info("---------------------")
  logger.info(f"Indexing completed, .json file generated")
  index.save_to_disk('JyothishKT.json')
  logger.info("---------------------")
  logger.info(f".json file saved")
  return index

index = construct_index(directory_path,llm_predictor,prompt_helper)