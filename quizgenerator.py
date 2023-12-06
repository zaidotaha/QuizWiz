from openai import OpenAI
from IPython.display import Markdown, display
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema.output_parser import StrOutputParser
import re
import sys
# this script is called from quizwiz.py with two parameters, number of questions and quiz topics, it returns a json object storing the quiz
def main(num_questions, quiz_context):
    client = OpenAI()
    template = """
    You are an expert in every field there is and want to help me create a quiz. 
    I want you to create a quiz with {num_questions} multiple choice questions about the following concept/content: {quiz_context}.
    Your reply must be structured and limited the following format:

    Format the output as JSON. There should be a "number" key specifying number of questions. 
    Keys for questions will be in the format of "Question" followed by the number of question, for example Question1, Question2 etc.
    The value for each question will be a JSON string of a python dictionary with the following format:
    'Question':'This is the question', 'A':'Option A', 'B':'Option B', 'C':'Option C', 'D':'Option D', 'Answer': 'A'

    {{
    number: 3,
    "Question1": {{
        "Question": "What is the capital of France?",
        "A": "Berlin",
        "B": "Paris",
        "C": "Madrid",
        "D": "Rome",
        "Answer": "B"
    }},
    "Question2": {{
        "Question": "Which programming language is known for its simplicity and readability?",
        "A": "Java",
        "B": "Python",
        "C": "C++",
        "D": "JavaScript",
        "Answer": "B"
    }},
    "Question3": {{
        "Question": "What is the largest planet in our solar system?",
        "A": "Mars",
        "B": "Jupiter",
        "C": "Saturn",
        "D": "Neptune",
        "Answer": "B"
    }}
    }}
    """ 
    prompt = PromptTemplate.from_template(template)
    chain = prompt | ChatOpenAI(temperature=0.0) | StrOutputParser()
    result = chain.invoke({"num_questions":num_questions, "quiz_context":quiz_context})
    Markdown(result)
    return result

if __name__ == "__main__":
    r = main(sys.argv[1], int(sys.argv[2]))
    print(r)
