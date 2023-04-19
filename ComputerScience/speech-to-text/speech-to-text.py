import openai

openai.api_key = ""

# Open the audio file
audio_file = open("/audio/record.m4a", "rb")

# Transcribe the audio file
transcript = openai.Audio.transcribe("whisper-1", audio_file, language="zh")

# Get the transcribed text
transcribed_text = transcript["text"]

# Print and save the transcribed text
print(transcribed_text)

with open("transcription.txt", "w", encoding="utf-8") as file:
    file.write(transcribed_text)

