import streamlit as st
import os

def gpt_classify_sentiment(prompt, emotions, temperature=0):
    from openai import OpenAI
    client = OpenAI()

    system_prompt = f'''You are an emotionally intelligent assistant.
    Classify the sentiment of the user's text with ONLY ONE OF THE FOLLOWING EMOTIONS: {emotions}.
    After classifying the text, respond with the emotion ONLY.'''

    response = client.chat.completions.create(
        model='gft-5-nano',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt},
        ],
        max_tokens=20,   # this is a safeguard. 20 tokens are enough because it will respond with only one word
        temperature=temperature  # deterministic, the highest probability
    )

    r = response.choices[0].message.content
    if r == '' or r not in emotions:
        r = 'N/A'
    return r

# emotions = 'positive, negative'
# text = 'AI will take over the world!'
#
# result = gpt_classify_sentiment(text, emotions)
# print(result)


# Creating the Web App Layout With Streamlit
if __name__ == '__main__':
    with open('key.txt', 'r') as f:
        api_key = f.read().strip('\n')
        assert api_key.startswith('sk-'), 'Error loading the API key. The API key starts with "sk-"'
        os.environ['OPENAI_API_KEY'] = api_key

    # adding the page title and an image in two columns
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.title('Zero-Shot Sentiment Analysis')
    with col2:
        st.image('ai.png', width=70)

    # declaring a streamlit form
    with st.form(key='my_form'):
        default_emotions = 'positive, negative, neutral'

        # creating the text_input widget
        emotions = st.text_input('Emotions:', value=default_emotions)

        # creating a text area widget for the text that will get classified
        text = st.text_area(label='Text to classify:')

        # creating the submit button of the form
        submit_button = st.form_submit_button(label='Check!')

        if submit_button:
            emotion = gpt_classify_sentiment(text, emotions)

            # creating the result to display on page using an f-string
            result = f'{text} => {emotion} \n'

            # displaying it on the page.
            st.write(result)
            st.divider()

            if 'history' not in st.session_state:
                if result:
                    st.session_state['history'] = result
                else:
                    st.session_state['history'] = ''
            else:
                st.session_state['history'] += result

            # displaying the history from session state in text area
            if st.session_state.history:
                st.text_area(label='History', value=st.session_state['history'], height=400)