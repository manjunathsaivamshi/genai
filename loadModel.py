from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip, concatenate_audioclips
from PIL import Image, ImageDraw, ImageFont
import os
import random

def text_to_speech(text, filename):
    tts = gTTS(text, lang='en')
    tts.save(filename)

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            paragraphs = content.split('\n')
            paragraphs = [para for para in paragraphs if para.strip() != '']
            return paragraphs
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def create_text_image(text, size):
    image = Image.new('RGB', size, color='black')
    draw = ImageDraw.Draw(image)
    
    # Load a font (default font is used here)
    font = ImageFont.load_default()
    
    # Calculate text size and position
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

    # Draw the text on the image
    draw.text(position, text, fill='white', font=font)

    return image

# Example usage
if __name__ == "__main__":
    os.remove("output_video.mp4")
    file_path = './data.txt'  # Replace with your text file path
    paragraphs = read_text_file(file_path)
    
    if not paragraphs:
        print("No paragraphs to process.")
        exit()

    rdmnum = random.randint(0, len(paragraphs) - 1)  # Adjusted range to prevent index error
    gif_paths = ['animation.gif', 'animation1.gif', 'animation3.gif', 'animation4.gif']  # Your GIF files

    text = paragraphs[rdmnum]
    music_path = 'bgm.mp3'  # Your background music file
    audio_filename = 'voice.mp3'

    # Convert text to speech
    text_to_speech(text, audio_filename)

    # Total duration for the video
    total_duration = 20  # seconds
    num_gifs = len(gif_paths)
    gif_duration = total_duration / num_gifs

    # Create a list to hold the video clips
    clips = []

    # Load each GIF and overlay text
    for gif in gif_paths:
        clip = VideoFileClip(gif).subclip(0, gif_duration).set_duration(gif_duration)

        # # Create an image with the text overlay
        # text_image = create_text_image(text, clip.size)
        # text_image_path = "temp_text_image.png"
        # text_image.save(text_image_path)

        # Load the text image as a video clip with a specific duration
        # text_clip = ImageClip(text_image_path).set_duration(gif_duration).set_position('center')

        # Composite the text image on top of the GIF clip
        # composite_clip = CompositeVideoClip([clip, text_clip])

        clips.append(clip)

    # Concatenate the video clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Load the background music file
    audio = AudioFileClip(music_path).volumex(0.3)

    # Load the speech audio file
    speech_audio = AudioFileClip(audio_filename)

    # Combine the background music with the speech audio
    #final_audio = concatenate_audioclips([audio, speech_audio])

    # Set the audio to the final clip
    final_clip = final_clip.set_audio(speech_audio).set_duration(total_duration)

    # Export the final video
    final_clip.write_videofile("output_video.mp4", codec="libx264", fps=24)

    # Clean up temporary files
    os.remove(audio_filename)
    # os.remove(text_image_path)

    # Close the clips to free resources
    for clip in clips:
        clip.close()
    final_clip.close()
    audio.close()
    speech_audio.close()
