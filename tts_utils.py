from kokoro import KPipeline
import numpy as np
import time
from functools import lru_cache
import soundfile as sf
import os
@lru_cache(maxsize=None)  # Cache all results (or set a maxsize limit)
def load_pipeline(lang_code='a'):
    return KPipeline(lang_code=lang_code)
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
def save_audio(audio_data,output_path="static/",sampling_rate=24000):
    high_quality_path=output_path+"audio.wav"
    low_quality_path=output_path+"audio.ogg"
    if os.path.exists(high_quality_path):
        os.remove(high_quality_path)
    if os.path.exists(low_quality_path):
        os.remove(low_quality_path)
    sf.write(high_quality_path,audio_data,sampling_rate)
    sf.write(low_quality_path,audio_data,sampling_rate)
    print("Audio file saved successfully")
    return output_path,high_quality_path,low_quality_path