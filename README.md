# QuizWiz
This is a simply quiz generator tool that uses openAI API to create a simple MCQ quiz

To use this app, first download the files to you local machine.
Create a .env file, add this line 
``` python
OPENAI_API_KEY= "your openAI API key"
```
Make sure you have installed all necessary libraries (namely langChain and Streamlit)

Open the terminal, navigate to the directory of the project.
Run the following command from the terminal:
```
streamlit run QuizWiz.py
```
A browser tab should open for you. 
Enter the quiz topic and the number of questions you want to generate and viola!
