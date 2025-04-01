from kokoro import KPipeline
import numpy as np
import time
from functools import lru_cache

@lru_cache(maxsize=None)  # Cache all results (or set a maxsize limit)
def load_pipeline(lang_code='a'):
    return KPipeline(lang_code=lang_code)
def generate_audio(text,pipeline,voice_option="af_heart"):
    try:
            # Generate audio chunks
            generator = pipeline(text, voice=voice_option)
            audio_chunks = []
            i=0
            time_start=time.time()
            for _, _, audio in generator:
                # print(f"Chunk {i+1} completed")
                i+=1
                audio_chunks.append(audio)
            time_end=time.time()
            if not audio_chunks:
                print("No audio generated")
                return None
            
            # Combine audio chunks
            full_audio = np.concatenate(audio_chunks)
            
            
            # Display results
            return audio,time_end-time_start
                    
                    
    except Exception as e:
        # st.error(f"Error generating audio: {str(e)}")
        print(f"Error occured in generating audio:{e}")
        return None