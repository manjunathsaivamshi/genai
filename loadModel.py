from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip
import os
import random

model_directory = "./saved_model"

def text_to_speech(text, filename):
    tts = gTTS(text, lang='en')
    tts.save(filename)


def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire file content
            content = file.read()
            # Split the content into paragraphs at every newline character
            paragraphs = content.split('\n')
            # Remove any empty paragraphs (if needed)
            paragraphs = [para for para in paragraphs if para.strip() != '']
            return paragraphs
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Replace 'your_file.txt' with the path to your text file
    #pipe = runModel()
    file_path = './data.txt'
    paragraphs = read_text_file(file_path)
    rdmnum = random.randint(1, 2500)
    gif_paths = ['animation.gif','animation1.gif','animation3.gif','animation4.gif']

    # Text to be displayed and converted to speech
    text = paragraphs[rdmnum]  # Replace with your desired text
    music_path = 'bgm.mp3'
    audio_filename = 'voice.mp3'

    # Convert text to speech
    text_to_speech(text, audio_filename)

    # Total duration for the video
    total_duration = 20  # seconds
    num_gifs = len(gif_paths)
    gif_duration = total_duration / num_gifs

    # Create a list to hold the video clips
    clips = []

    # Load each GIF, set its duration, and add text overlay
    for gif in gif_paths:
        clip = VideoFileClip(gif).subclip(0, gif_duration)
        clip = clip.set_duration(gif_duration)  # Set the duration for the clip

        # Create a text clip
        text_clip = TextClip(text, fontsize=24, color='white', bg_color='black', size=clip.size)  # Adjust size as needed
        text_clip = text_clip.set_position('center').set_duration(gif_duration)

        # Overlay the text on the GIF
        clip = clip.set_duration(gif_duration).fx(vfx.composite, text_clip)

        clips.append(clip)

    # Concatenate the video clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Load the background music file
    audio = AudioFileClip(music_path)

    # Adjust the audio volume to 30%
    audio = audio.volumex(0.3)

    # Load the speech audio file
    speech_audio = AudioFileClip(audio_filename)

    # Combine the background music with the speech audio
    final_audio = concatenate_audioclips([audio, speech_audio])

    # Set the audio to the final clip
    final_clip = final_clip.set_audio(final_audio)

    # Set the duration to the total duration (20 seconds)
    final_clip = final_clip.set_duration(total_duration)

    # Export the final video
    final_clip.write_videofile("output_video.mp4", codec="libx264", fps=24)

    # Clean up temporary audio file
    os.remove(audio_filename)

    # Close the clips to free resources
    for clip in clips:
        clip.close()
    final_clip.close()
    audio.close()
    speech_audio.close()




