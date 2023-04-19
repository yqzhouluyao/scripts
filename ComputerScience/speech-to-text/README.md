# 切分音频文件：

Whisper API 仅支持小于 25 MB 的文件，如果您有比这更长的音频文件，则需要将其分成 25 MB 或更小的块或使用压缩音频格式。



### 1. 安装 PyDub 和 FFmpeg

PyDub 依赖 FFmpeg 来处理各种音频格式。首先，使用 pip 安装 PyDub，然后安装 FFmpeg。

```sh
pip install pydub
brew install ffmpeg
```



### 2. 创建 Python 脚本 split_audio.py

使用以下内容创建 Python 脚本 split_audio.py，该脚本将音频文件切分成 10 分钟长的音频片段，您可以根据自己音频文件的具体情况进行切分。

```python
from pydub import AudioSegment
import os
#切分成10分钟长的音频片段，您可以根据自己音频文件的具体情况进行切分
def split_audio(input_file, output_dir, chunk_length_ms=10 * 60 * 1000):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, chunk in enumerate(chunks):
        chunk.export(os.path.join(output_dir, f"{i:03d}_{os.path.basename(input_file).split('.')[0]}.mp3"), format="mp3")

if __name__ == "__main__":
    input_file = "/Users/zhouluyao/Desktop/split_audio/001.m4a"
    output_dir = "/Users/zhouluyao/Desktop/split_audio/output/"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    split_audio(input_file, output_dir)
```

将 `/Users/zhouluyao/Desktop/split_audio/001.m4a` 替换为长音频文件的路径，将 `/Users/zhouluyao/Desktop/split_audio/output/` 替换为要保存拆分音频文件的文件夹的路径。



### 3. 运行脚本

```python
python split_audio.py
```

此脚本会将输入音频文件拆分为更小的块，每个块 10 分钟（默认情况下），并将它们保存在指定的输出文件夹中。您可以更改 `split_audio` 函数中的 `chunk_length_ms` 参数以根据需要调整块长度（以毫秒为单位）。拆分音频文件后，您可以使用 Whisper API 处理每个较小的块。



# 音频文件转文本：

要使用 OpenAI 的 API 将本地录音文件 `record.m4a` 转换为文本，请按照以下步骤操作：

### 1. 安装 OpenAI Python 库（v0.27.0 或更高版本）

```sh
pip3 install openai
```



### 2. 使用以下脚本 speech-to-text.py 将本地录音文件 record.m4a 转换为文本

```python
import openai

# Set your API key
#openai.api_key = "sk-1sFnitcInw96iD2UH6bjT3BlbkFJNmgvL4ur9ulkv4g"
openai.api_key = "<YOUR_API_KEY>"

# Open the audio file
audio_file = open("/Users/zhouluyao/Downloads/002.m4a", "rb")

# Transcribe the audio file
transcript = openai.Audio.transcribe("whisper-1", audio_file, language="zh")

# Get the transcribed text
transcribed_text = transcript["text"]

# Print and save the transcribed text
print(transcribed_text)

with open("transcription.txt", "w", encoding="utf-8") as file:
    file.write(transcribed_text)
```

将 `<YOUR_API_KEY>` 替换为您的实际 [API](https://platform.openai.com/account/api-keys) 密钥，并将 `/Users/zhouluyao/Downloads/002.m4a` 替换为您的音频文件的路径。



### 3、您可以运行以下命令生成文本文件

```
python3 speech-to-text.py
```
