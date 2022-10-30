import youtube_dl, asyncio, os, json, openai
from deepgram import Deepgram
import streamlit as st
from pathlib import Path
from streamlit_quill import st_quill

st.set_page_config(
    page_title="Text it up!",
    page_icon="🖺",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://twitter.com/dotaadarsh",
        'About': "Text it up! - An app that provides transcription of YT videos"
    }
)

openai.api_key = st.secrets["OPENAI_API_KEY"]
DEEPGRAM_API_KEY = st.secrets["DEEPGRAM_API_KEY"]

st.header("Text it up!")
video_url = st.text_input("Please enter the YouTube url", value= "https://youtu.be/JKxlsvZXG7c")

def markdown(text):
    with st.expander("Markdown editor"):
        c1, c2 = st.columns([3, 1])

        c2.subheader("Parameters")
        with c1:
            content = st_quill(
                value=text,
                placeholder="Write your text here",
                html=c2.checkbox("Return HTML", False),
                readonly=c2.checkbox("Read only", False),
                key="quill",
            )

            if content:
                st.subheader("Content")
                st.write(content)


async def transcribe(PATH_TO_FILE):
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    idx = 0
    with open(PATH_TO_FILE, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = await deepgram.transcription.prerecorded(source, {'summarize': True, 'punctuate': True, "diarize": True, "utterances": True })
        st.json(response, expanded=False)
        response_result_json = json.dumps(response, indent=4)
        # print(response_result_json)
        col1, col2 = st.columns(2)
        with col1: 
            with st.expander("Transcript"):
                st.write(response["results"]["channels"][0]["alternatives"][0]["transcript"])
        with col2:
            with st.expander("Summary/Keywords"):
                st.header("Summary")
                st.write(response["results"]["channels"][0]["alternatives"][0]["summaries"][0]["summary"])
                st.header("Keywords")
                response_openai = openai.Completion.create(
                    model="text-davinci-002",
                    prompt=f'Extract keywords from this text:\n\n{response["results"]["channels"][0]["alternatives"][0]["transcript"]}',
                    temperature=0.3,
                    max_tokens=60,
                    top_p=1.0,
                    frequency_penalty=0.8,
                    presence_penalty=0.0
                )
                # st.write(response_openai) 
                keywords_results = response_openai["choices"][0]["text"].split(',')
                for item in keywords_results:
                    st.write(item)

            # st.write(response["results"]["channels"][0]["alternatives"][0]["words"])
            # st.write(list(item for item in response["results"]["channels"][0]["alternatives"][0]["words"]))\
            # for item in response["results"]["channels"][0]["alternatives"][0]["words"]:
            #     st.write(item[idx])
            #     idx += 1
    with st.expander("Search the video"):
        search = dict()
        for item in response["results"]["channels"][0]["alternatives"][0]["words"]:
            #st.write(item["word"], item["start"])
            search[item["word"]] =  item["start"]
        # st.write(search)

        keyword = st.text_input("Enter the word")
        
        if keyword in search:
            time = int(search[keyword])
            #st.video(f"{video_url}?t={time}")
            st.video(video_url, start_time=time)
    return response

async def main(video_url):

    videoinfo = youtube_dl.YoutubeDL().extract_info(url = video_url, download=False)
    # st.json(videoinfo, expanded=False)
    filename = f"{videoinfo['id']}.mp3"
    # st.write(filename)

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([videoinfo['webpage_url']])
    # st.write("Download complete... {}".format(filename))
    # st.audio(filename)
    base = Path.cwd()
    PATH_TO_FILE = f"{base}/{filename}"
    
    return PATH_TO_FILE

response = asyncio.run(transcribe(asyncio.run(main(video_url))))
markdown(response["results"]["channels"][0]["alternatives"][0]["transcript"])
