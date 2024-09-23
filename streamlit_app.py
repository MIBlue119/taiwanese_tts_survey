import streamlit as st
import os
from yating_tts_sdk import YatingClient as ttsClient

# Set up the Yating TTS client
URL = "https://tts.api.yating.tw/v2/speeches/short"
KEY = os.environ.get("YATING_API_KEY")
# Initialize the TTS client
client = ttsClient(URL, KEY)

def generate_audio(text, model, speed, pitch, energy):
    file_name = "generated_audio"
    try:
        client.synthesize(
            text,
            ttsClient.TYPE_TEXT,
            model,
            speed,
            pitch,
            energy,
            ttsClient.ENCODING_MP3,
            ttsClient.SAMPLE_RATE_16K,
            file_name
        )
        return f"{file_name}.mp3"
    except Exception as err:
        st.error(f"An error occurred: {err}")
        return None

# Streamlit app
st.title("台語文字轉語音生成器")

# Add a check for the API key
if not KEY:
    st.error("API key not found. Please set the YATING_API_KEY environment variable.")
    st.stop()


# User input
text = st.text_area("請輸入要轉換的台語文字：", max_chars=100)

# Speaker selection
speaker_options = {
    "女聲 1": ttsClient.MODEL_TAI_FEMALE_1,
    "女聲 2": ttsClient.MODEL_TAI_FEMALE_2,
    "男聲": ttsClient.MODEL_TAI_MALE_1
}
selected_speaker = st.selectbox("選擇說話者：", list(speaker_options.keys()))

# Voice customization
st.subheader("自訂語音設定")
speed = st.slider("語速", 0.5, 1.5, 1.0, 0.1)
pitch = st.slider("音調", 0.5, 1.5, 1.0, 0.1)
energy = st.slider("音量", 0.5, 1.5, 1.0, 0.1)

if st.button("生成語音"):
    if text:
        with st.spinner("正在生成語音..."):
            audio_file = generate_audio(text, speaker_options[selected_speaker], speed, pitch, energy)
        
        if audio_file:
            st.success("語音生成成功！")
            
            # Play audio
            st.audio(audio_file, format="audio/mp3")
            
            # Download button
            with open(audio_file, "rb") as file:
                btn = st.download_button(
                    label="下載音檔",
                    data=file,
                    file_name=audio_file,
                    mime="audio/mp3"
                )
            
            # Clean up the generated file
            os.remove(audio_file)
    else:
        st.warning("請輸入要轉換的文字。")