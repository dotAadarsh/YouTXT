
# YouTXT

YouTXT is an app that convert any YouTube video to text and it provides the below

- Transcript
- Summary [TL;DR]
- Transcript Translation
- Search [Search the word in the video]
- Markdown editor

  

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/dotaadarsh/YouTXT)

  

## Working

  

### Packages

- [youtube-dl](https://github.com/ytdl-org/youtube-dl) - a command-line program to download videos from YouTube.com

- [openai](https://github.com/openai/openai-python) - provides convenient access to the OpenAI API from applications written in the Python language

- [streamit](https://github.com/streamlit/streamlit) - The fastest way to build and share data apps

- [streamlit-quill](https://github.com/okld/streamlit-quill) - [Quill editor](https://github.com/quilljs/quill) component for Streamlit.

- [Deepgram](https://github.com/deepgram/deepgram-python-sdk) - Python SDK for [Deepgram](https://deepgram.com/)'s automated speech recognition APIs.
- [itranslate](https://pypi.org/project/itranslate/) - Google translate free and unlimited, itranslate since gtranslate is taken
  

### API's

- Deepgram - Get yours at - https://console.deepgram.com/

- OpenAI’s API - Get yours at - https://openai.com/api/

  

### What it does?

- Get the URL From the user.

- Extracts the audio from the provided URL using YouTube-dl.

- Sends the extracted audio to the Deepgram.

- Deepgram provides the transcription and summary of the provided audio.

- With the help of OpenAI, the list of keywords are identified [It can actually do more than that].

- By mapping the each word with the start time, a search dict is created. With the help of this the user can search the video by providing the word.

- By passing the transcription to the Quill editor, the user is now able to modify it and do whatever he wants with the text.