from pydub import AudioSegment
from kokoro import KPipeline
import numpy as np
import time
from functools import lru_cache
import soundfile as sf
import os
@lru_cache(maxsize=None)  # Cache all results (or set a maxsize limit)
def load_pipeline(lang_code='a'):
    try:
        return KPipeline(lang_code=lang_code)
    except Exception as e:
        print(f"Failed to load KPipeline for lang_code '{lang_code}': {e}")
        # Re-raise or return None/custom error object
        raise # or return None
def generate_audio(text,pipeline,voice_option="af_heart",sample_rate=24000):
    try:
        # Generate audio chunks
        generator = pipeline(text, voice=voice_option)
        audio_chunks = []
        i=0
        time_start=time.time()
        for _, _, audio in generator:
            print(f"Chunk {i+1} completed")
            i+=1
            audio_chunks.append(audio)
        time_end=time.time()
        if not audio_chunks:
            print("No audio generated")
            return None
        print("Audio generation completed successfully")
        # Combine audio chunks
        full_audio = np.concatenate(audio_chunks)
        
        
        # Display results
        return full_audio,time_end-time_start
                    
                    
    except Exception as e:
        # st.error(f"Error generating audio: {str(e)}")
        print(f"Error occured in generating audio:{e}")
        return None


def convert_wav_to_mp3(input_filepath, output_filepath="audio.mp3"):
    """
    Converts a WAV audio file to MP3 format with good compression for smaller file size
    while trying to maintain reasonable audio quality.

    Args:
        filepath (str): The path to the input WAV audio file.
        output_filepath (str, optional): The desired path for the output MP3 file.
                                         Defaults to "audio.mp3" in the current directory.
    """
    try:
        audio = AudioSegment.from_wav(input_filepath)
        audio.export(output_filepath, format="mp3", bitrate="64k") # 128k is a good balance
        print(f"Successfully converted '{input_filepath}' to '{output_filepath}'")
    except Exception as e:
        print(f"Error during conversion: {e}")

def save_audio(audio_data,output_path_folder="static/",file_name='audio',sampling_rate=24000):
    high_quality_audio_path=os.path.join(output_path_folder, "{file_name}.wav")#output_path_folder+"audio.wav"
    low_quality_audio_path=os.path.join(output_path_folder, "{file_name}.mp3")#output_path_folder+"audio.mp3"
    if os.path.exists(high_quality_audio_path):
        os.remove(high_quality_audio_path)
    if os.path.exists(low_quality_audio_path):
        os.remove(low_quality_audio_path)
    sf.write(high_quality_audio_path,audio_data,sampling_rate)
    convert_wav_to_mp3(output_filepath=low_quality_audio_path,input_filepath=high_quality_audio_path)
    print("Audio file saved successfully")
    return high_quality_audio_path,low_quality_audio_path

