from pydub import AudioSegment
import os

def split_audio(input_file, output_dir, chunk_length_ms=10 * 60 * 1000):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, chunk in enumerate(chunks):
        chunk.export(os.path.join(output_dir, f"{i:03d}_{os.path.basename(input_file).split('.')[0]}.mp3"), format="mp3")

if __name__ == "__main__":
    input_file = "/Users/zhouluyao/Desktop/zhongcai/001.m4a"
    output_dir = "/Users/zhouluyao/Desktop/zhongcai/output/"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    split_audio(input_file, output_dir)
