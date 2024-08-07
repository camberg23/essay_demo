import streamlit as st
import random

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain
from system_messages import *

N = 6  # Number of questions per round
progress_step = 1.0 / N

# Initialize session state variables
if 'llm_output' not in st.session_state:
    st.session_state.llm_output = ""
if 'reasoning' not in st.session_state:
    st.session_state.reasoning = ""
if 'options_text' not in st.session_state:
    st.session_state.options_text = ""
if 'options' not in st.session_state:
    st.session_state.options = []
if 'total_choices' not in st.session_state:
    st.session_state.total_choices = []
if 'current_iteration' not in st.session_state:
    st.session_state.current_iteration = 0
if 'process_started' not in st.session_state:
    st.session_state.process_started = False
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = ""
if 'custom_answer' not in st.session_state:
    st.session_state.custom_answer = ""
if 'raw_options' not in st.session_state:
    st.session_state.raw_options = ""
if 'profile' not in st.session_state:
    st.session_state.profile = 'No profile yet, this is the first ever session!'
if 'selected_interests' not in st.session_state:
    st.session_state.selected_interests = ""
if 'all_prompts' not in st.session_state:
    st.session_state.all_prompts = "No previous prompts yet, this is the first ever session!"
if 'interim_interests' not in st.session_state:
    st.session_state.interim_interests = ""

chat_model = ChatOpenAI(openai_api_key=st.secrets['API'], model_name='gpt-4o-2024-05-13', temperature=0.3)
chat_model_random = ChatOpenAI(openai_api_key=st.secrets['API'], model_name='gpt-4o-2024-05-13', temperature=random.uniform(0.6, 1.1))

TITLE = 'essay.app: Intake and Prompt Personalization, v0.4'
st.set_page_config(page_title=TITLE, page_icon='essay_logo.png')
st.title(TITLE)
st.markdown('[User directions, draft](https://docs.google.com/document/d/1PKCTD1h836ExDOS8xw3qUpuRGUy532b5CQMVXi41q8k/edit?usp=sharing)')

progress_bar = st.progress(st.session_state.current_iteration * progress_step)

# Parse LLM output function
def parse_and_store_llm_output():
    # Split the output into reasoning and the prompts section
    parts = st.session_state.llm_output.split("REASONING:")
    if len(parts) > 1:
        reasoning_part, prompts_part = parts[1].split("QUESTIONS:", 1)
        st.session_state.reasoning = reasoning_part.strip()

        # Split each set of prompts
        prompts_sections = prompts_part.split("QUESTIONS:")
        st.session_state.all_prompts = [{'options_text': prompts.strip()} for prompts in prompts_sections if prompts.strip()]

# Function to display current prompt and options
def display_current_prompt():
    st.session_state.custom_answer = ""
    if st.session_state.current_iteration - 1 < len(st.session_state.all_prompts):
        current_prompt = st.session_state.all_prompts[st.session_state.current_iteration - 1]
        st.session_state.options_text = current_prompt['options_text']
        # Split and format options correctly based on new labeling
        raw_options = st.session_state.options_text.split("(B)")
        if len(raw_options) >= 2:
            option_a = raw_options[0].strip().replace("(A)", "").strip()
            option_b = raw_options[1].strip().replace("(B)", "").strip()
            # st.session_state.options = [f"(A) {option_a}", f"(B) {option_b}"]
            st.session_state.options = [f"(A) {option_a}", f"(B) {option_b}", "(C) Equally interesting", "(D) Neither/something else"]
        else:
            st.session_state.options = ["Sorry, there was an uncaught error in generating options for you. Please refresh the page and try again."]
    else:
        st.session_state.options = ["No more prompts available"]

# Generate LLM output for all prompts
def generate_all_llm_output():
    chat_chain = LLMChain(prompt=PromptTemplate.from_template(user_prompt_generator), llm=chat_model)
    st.session_state.llm_output = chat_chain.run(PROFILE=st.session_state.profile, LAST_OPTIONS=st.session_state.all_prompts,
                                                 INTERESTS=st.session_state.selected_interests, N=N)
    # st.write(st.session_state.llm_output)
    parse_and_store_llm_output()
    display_current_prompt()
    progress_bar.progress(st.session_state.current_iteration * progress_step)

# 'Go' button to start the process
if not st.session_state.process_started:
    st.write("To begin, please choose up to six of your top interests from the following list:")
    col1, col2 = st.columns([4, 1])  # Adjust the proportion as needed
    with col1:
        st.session_state.selected_interests = st.multiselect(
            "To begin, please choose up to six of your top interests from the following list:", 
            interests, 
            max_selections=6,
            label_visibility="collapsed"
        )
    disabled = len(st.session_state.selected_interests) == 0
    with col2:
        if st.button('Begin Demo', disabled=disabled):
            with st.spinner('Generating choices...'):
                st.session_state.process_started = True
                st.session_state.current_iteration = 1
                generate_all_llm_output()
                st.rerun()

def process_user_input():
    if st.session_state.selected_option == "(D) Neither/something else" and not st.session_state.custom_answer.strip():
        st.error("Please fill in your answer when choosing 'Neither/something else'.")
    else:
        user_input = f"{st.session_state.selected_option}: {st.session_state.custom_answer}" if st.session_state.selected_option == "(D) Neither/something else" else st.session_state.selected_option
        if st.session_state.current_iteration == 1:
            st.session_state.total_choices.append({'reasoning used to generate these questions': st.session_state.reasoning})
        st.session_state.total_choices.append({'options': st.session_state.options, 'choice': user_input})
        st.session_state.current_iteration += 1
        if st.session_state.current_iteration <= N:
            display_current_prompt()  # Display next prompt
            st.rerun()
        else:
            process_total_choices()
            generate_all_llm_output()
            st.rerun()
            
def process_total_choices():
    chat_chain = LLMChain(prompt=PromptTemplate.from_template(infer_from_answers), llm=chat_model)
    insights = chat_chain.run(SESSION_CHOICES=st.session_state.total_choices)
    # st.write(insights)
    chat_chain = LLMChain(prompt=PromptTemplate.from_template(profile_reconciliation), llm=chat_model)
    st.session_state.profile = chat_chain.run(PROFILE=st.session_state.profile, INTERESTS=st.session_state.selected_interests, 
                                              INSIGHTS=insights)
    # chat_chain = LLMChain(prompt=PromptTemplate.from_template(answer_profile_reconciliation), llm=chat_model)
    # st.session_state.profile = chat_chain.run(PROFILE=st.session_state.profile, INTERESTS=st.session_state.selected_interests, 
    #                                           SESSION_CHOICES=st.session_state.total_choices)
    st.session_state.total_choices = []
    st.session_state.current_iteration = 1

# Display LLM output and options if process started
if st.session_state.process_started:
    with st.expander('See what the system has learned about you and how it developed the current set of choices'):
        # st.write('FULL OUTPUTS', st.session_state.llm_output)
        st.write('**CURRENT STATE OF USER PROFILE:**',st.session_state.profile)
        st.write('**REASONING BEHIND CURRENT ROUND OF PROMPT CHOICES**:', st.session_state.reasoning)
    st.subheader('**Please choose which of the following two questions you’d rather address in your writing:**')

    # Process each iteration until all questions are answered
    if st.session_state.current_iteration <= N:
        # Radio buttons for options
        st.session_state.selected_option = st.radio("If they required the same amount of time/effort, I would rather:", st.session_state.options, index=None, label_visibility='collapsed')
        
        # Text input for custom answer
        if st.session_state.selected_option == "(D) Neither/something else":
            st.session_state.custom_answer = st.text_input("Write in:", value=st.session_state.custom_answer, placeholder="just a couple of words on why you chose (D) or what you'd rather write about")

        # Submit button
        if st.button('**Submit**'):
            with st.spinner('Processing your choices and generating a new set of prompts (this could take up to 1 min)...'):
                # st.snow()
                # st.write(st.session_state.total_choices)
                process_user_input()  # Function to process user input

with st.sidebar:
    disable = st.session_state.profile == 'No profile yet, this is the first ever session!'
    disable2 = st.session_state.process_started == False

    # Move the selected interests input to the top of the sidebar
    st.title("Update Interests")
    
    # Assign interim selected interests
    st.session_state.interim_interests = st.multiselect(
        "Update your initial interests as desired:", 
        interests, 
        default=st.session_state.selected_interests,
        max_selections=6,
    )
    
    # Update interests button
    if st.button('Update Interests', disabled=disable2):
        st.session_state.selected_interests = st.session_state.interim_interests

    
    st.title('Prompt Personalizer')
    user_input_topic = st.text_area("Input your assigned prompt or topic of interest:", height=200)
    user_first_thoughts = st.text_area("Jot down any initial rough thoughts you might have about this topic:", height=200)
    if st.button('Personalize topic', key='submit_personalization', disabled=disable):
        if user_input_topic:
            # Call LLM with the user's input
            with st.spinner('Generating suggestions...'):
                chat_chain = LLMChain(prompt=PromptTemplate.from_template(prompt_personalizer), llm=chat_model)
                personalized_prompt = chat_chain.run(PROFILE=st.session_state.profile, INTERESTS=st.session_state.selected_interests,
                                                     USER_INPUT=user_input_topic, FIRST_THOUGHTS=user_first_thoughts)
                st.subheader('Here are a few personalized angles you might consider:')
                st.write(personalized_prompt)
        else:
            st.error("Please enter a topic or prompt to proceed.")
    st.title('Prompt Generator')
    if st.button('Generate a random prompt for me', disabled=disable):
        with st.spinner('Generating a personalized prompt...'):
                chat_chain = LLMChain(prompt=PromptTemplate.from_template(prompt_idea_generator), llm=chat_model_random)
                random_topic = chat_chain.run(PROFILE=st.session_state.profile, INTERESTS=st.session_state.selected_interests, RANDOM=random.uniform(1,100000000))
                st.subheader('Here is a personalized writing prompt for you:')
                st.write(random_topic)
