import streamlit as st
import subprocess
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI

# This loads the .env file which contains the openAI API key
load_dotenv()
if "page" not in st.session_state:
    st.session_state.page = 0
# This is the start quiz function which is called when the respective button is clicked 
def Start_quiz(): 
    st.session_state.page += 1
    st.session_state.question_index = 0
# This function was used during development to allow movement between the quiz page and the home page 
def restart(): st.session_state.page = 0


# we start of with the home page represented by session_state.page == 0
if st.session_state.page == 0:
    # Title and descriptoin
    st.markdown(""" # Quiz Wiz
    ##### Your AI Quiz Generation Tool. Create simple quiz Quizzes with a click of a button! <br>
    Simply specify the quiz topic and the number of questions you want the Wiz to generate and viola! <br><br>
    """, True)

    # Column division used to roughly center some elements
    buff, inputcol, buff2 = st.columns([1, 5, 1])
    button_buff, buttoncol, button_buff2 = st.columns([6,3,6])
    result_buff1, resultcol1, result_buff12 = st.columns([1,5,1])

    # input from user (quiz topic, number of questions)
    topic = inputcol.text_input('Quiz Topic:', placeholder="Type a quiz topic ...")
    num = inputcol.number_input("Enter number of questions:", value=None, placeholder="Type a number ...", step=1, min_value=1, max_value=20)
    inputcol.markdown("""<br>""", unsafe_allow_html=True)

    # We have a button called "Generate Quiz", if clicked, then session_state.click[1] is set to true  
    def clicked(button):
        st.session_state.clicked[button] = True
    
    if 'clicked' not in st.session_state:
        st.session_state.clicked = {1:False}
    
    buttoncol.button("Generate Quiz", on_click=clicked, args=[1])

    # if the "Generate Quiz" button was clicked
    if st.session_state.clicked[1]:   
        # called the quizgenerator.py to generate quiz, will return a JSON string
        arguments = [topic,str(num)]  
        result = subprocess.run([sys.executable, "quizgenerator.py"]+arguments, capture_output=True, text=True)
        # Parse the JSON string
        quiz_data = json.loads(result.stdout.strip())

        # Generate image that matches the quiz topic
        client = OpenAI()
        response = client.images.generate(
        model="dall-e-3",
        prompt= "An image to put at the beginning of a quiz on "+topic,
        size="1024x1024",
        quality="standard",
        n=1,
        )
        image_url = response.data[0].url
        st.image(image_url)

        # Initialize session_state variables, we will use them to store the quiz questions
        st.session_state.number_of_questions = quiz_data["number"]
        st.session_state.questions = []
        st.session_state.options_A = []
        st.session_state.options_B = []
        st.session_state.options_C = []
        st.session_state.options_D = []
        st.session_state.correct_answers = []
        st.session_state.user_answers = []
        # Initialize the user answer array
        for i in range(st.session_state.number_of_questions):
            st.session_state.user_answers.append("")
        # Fill the session_state variables used for quiz to display them at the appropriate page
        for i in range(1, st.session_state.number_of_questions + 1):
            question_data = quiz_data[f"Question{i}"]
            st.session_state.questions.append(question_data['Question'])
            st.session_state.options_A.append(question_data['A'])
            st.session_state.options_B.append(question_data['B'])
            st.session_state.options_C.append(question_data['C'])
            st.session_state.options_D.append(question_data['D'])
            st.session_state.correct_answers.append(question_data['Answer'])

        # Columns to roughly center some items
        result_buff, resultcol, result_buff2 = st.columns([1,4,1])
        button_buff1, buttoncol1, button_buff12 = st.columns([5,2,5])
        # Success message
        resultcol.success("Quiz Generated! Click on the 'Start Quiz' button to start the quiz")
        # Start quiz button, increments session_state.page to 1 so the condition for the next if statement will be true
        buttoncol1.button("Start quiz", on_click=Start_quiz)
                
if st.session_state.page == 1:
    
    # For the next 2 functions, follow the order of comments while reading them
    def multiple_choice_question(question, options):
        # 3. Writes Question text
        st.write("<span style='font-size:1.8em;'>**"+question+"**</span>",unsafe_allow_html=True)
        buff, inputcol = st.columns([1, 50])
        # 4. Writes out options
        selected_option = inputcol.radio("", options, label_visibility ="collapsed",)
        return selected_option

    def show_current_question():
        # 1. Preps question text and option variables
        question_text = st.session_state.questions[st.session_state.question_index]
        options = [
            "a. " + st.session_state.options_A[st.session_state.question_index],
            "b. " + st.session_state.options_B[st.session_state.question_index],
            "c. " + st.session_state.options_C[st.session_state.question_index],
            "d. " + st.session_state.options_D[st.session_state.question_index]
        ]
        # 2. Call multiple_choice_question function. Gets back the selected option
        selected_option = multiple_choice_question(question_text, options)  
        # 5. Your choice text
        st.write("<br> You selected:", selected_option, unsafe_allow_html=True)
        # 6. Saves user current answer
        st.session_state.user_answers[st.session_state.question_index]=(selected_option)
    
    # next question, increments question index
    def next_question():
        st.session_state.question_index += 1

    # used during development to ease development 
    def reset_questions():
        st.session_state.question_index = 0

    # submit answers, increments session state for page, page 3 is the feedback report page
    def submit():   
        st.session_state.page = 2
    
    # intialized question_index if not initialized
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0

    # every question but last one
    if (st.session_state.question_index<st.session_state.number_of_questions-1):
        show_current_question()
        st.button("Next Question", on_click=next_question)
    # last question, shows submit button
    elif (st.session_state.question_index == st.session_state.number_of_questions-1):
        show_current_question()
        st.button("Submit", on_click=submit)


# feedback report

if st.session_state.page == 2:
    # title
    st.write("<br> <div style='text-align:center; font-size:2.7em;'><b>" + "Quiz Results" +
        "</b></div>", unsafe_allow_html=True)
    score = 0
    st.session_state.question_index = 0

    # functions to print an individual question, add score to score variable
    def print_question():   
        global score
        question_text = st.session_state.questions[st.session_state.question_index]
        st.write("<span style='font-size:1.8em;'>**"+question_text+"**</span>",unsafe_allow_html=True)
        st.write("a. "+ st.session_state.options_A[st.session_state.question_index])
        st.write("b. "+ st.session_state.options_B[st.session_state.question_index])
        st.write("c. "+ st.session_state.options_C[st.session_state.question_index])
        st.write("d. "+ st.session_state.options_D[st.session_state.question_index])
        user_ans = st.session_state.user_answers[st.session_state.question_index]
        real_ans = st.session_state.correct_answers[st.session_state.question_index]
        # st.write(user_ans + " " +real_ans)
        if(user_ans[:1] == real_ans.lower()):
            st.success("Your answer \"" + user_ans[2:] + "\" is correct!")
            score+=1
        else:
            st.error("Your answer \"" + user_ans[2:] + "\" is incorrect. Correct answer is "+real_ans)
    
    # function to call print_question for each question
    for i in range(0, st.session_state.number_of_questions):
        st.session_state.question_index = i
        print_question()
    
    # display score
    st.write("<br><div style='text-align:center; font-size:2.7em;'><b>" + 
        "Your score is " + str(score) + " out of " + str(st.session_state.number_of_questions) +
        "</b></div>", unsafe_allow_html=True)
   
   # home button to return you to the beginning of the page
    def home():
        st.session_state.page = 0
        st.session_state.clicked = {1:False}
    button_buff, buttoncol, button_buff2 = st.columns([5,2,5])
    buttoncol.button("Home Page", on_click=home)