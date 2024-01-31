import streamlit as st

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain
from system_messages import *

N = 5  # Number of iterations
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
if 'current_iteration' not in st.session_state:
    st.session_state.raw_options = 0
if 'profile' not in st.session_state:
    st.session_state.profile = 'No profile yet, this is the first ever session!'

chat_model = ChatOpenAI(openai_api_key=API_KEY, model_name='gpt-4-1106-preview', 
                        temperature=0.3, max_tokens=4096)
TITLE = 'Essay Interview Tool v0.1'
st.set_page_config(page_title=TITLE, page_icon=None)
st.title(TITLE)

progress_bar = st.progress(st.session_state.current_iteration * progress_step)

# Parse LLM output function
def parse_and_store_llm_output():
    # Split the output into reasoning and the prompts section
    parts = st.session_state.llm_output.split("REASONING:")
    if len(parts) > 1:
        reasoning_part, prompts_part = parts[1].split("PROMPTS:", 1)
        st.session_state.reasoning = reasoning_part.strip()

        # Split each set of prompts
        prompts_sections = prompts_part.split("PROMPTS:")
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
            st.session_state.options = [f"(A) {option_a}", f"(B) {option_b}", "(C) Neither/something else"]
        else:
            st.session_state.options = ["(C) Neither/something else"]
    else:
        st.session_state.options = ["No more prompts available"]

# Generate LLM output for all prompts
def generate_all_llm_output():
    chat_chain = LLMChain(prompt=PromptTemplate.from_template(user_prompt_generator), llm=chat_model)
    st.session_state.llm_output = chat_chain.run(PROFILE=st.session_state.profile, N=N)
    # st.write(st.session_state.llm_output)
    parse_and_store_llm_output()
    display_current_prompt()
    progress_bar.progress(st.session_state.current_iteration * progress_step)

# 'Go' button to start the process
if not st.session_state.process_started:
    if st.button('Go'):
        st.session_state.process_started = True
        st.session_state.current_iteration = 1
        generate_all_llm_output()

def process_user_input():
    if st.session_state.selected_option == "(C) Neither/something else" and not st.session_state.custom_answer.strip():
        st.error("Please fill in your answer when choosing 'Neither/something else'.")
    else:
        user_input = f"{st.session_state.selected_option}: {st.session_state.custom_answer}" if st.session_state.selected_option == "(C) Neither/something else" else st.session_state.selected_option
        if st.session_state.current_iteration == 1:
            st.session_state.total_choices.append({'reasoning used to generate these questions': st.session_state.reasoning})
        st.session_state.total_choices.append({'options': st.session_state.options_text, 'choice': user_input})
        st.session_state.current_iteration += 1
        if st.session_state.current_iteration <= N:
            display_current_prompt()  # Display next prompt
            st.rerun()
        else:
            process_total_choices()
            generate_all_llm_output()
            st.rerun()
            
def process_total_choices():
    chat_chain = LLMChain(prompt=PromptTemplate.from_template(answer_profile_reconciliation), llm=chat_model)
    st.session_state.profile = chat_chain.run(PROFILE=st.session_state.profile, SESSION_CHOICES=st.session_state.total_choices)
    st.session_state.current_iteration = 1

# Display LLM output and options if process started
if st.session_state.process_started:
    with st.expander('See cognition of LLM'):
        st.write('FULL OUTPUTS', st.session_state.llm_output)
        # st.write('REASONING', st.session_state.reasoning)
        st.write('PROFILE',st.session_state.profile)
    st.subheader('**Please select which of the following prompts you would be more interested and motivated to write about.**')

    # Process each iteration until all questions are answered
    if st.session_state.current_iteration <= N:
        # Radio buttons for options
        st.session_state.selected_option = st.radio("If they required the same amount of time/effort, I would rather:", st.session_state.options, index=0)
        
        # Text input for custom answer
        if st.session_state.selected_option == "(C) Neither/something else":
            st.session_state.custom_answer = st.text_input("Write in:", value=st.session_state.custom_answer, placeholder="a few words on what you'd rather write about")

        # Submit button
        if st.button('**Submit**'):
            process_user_input()  # Function to process user input