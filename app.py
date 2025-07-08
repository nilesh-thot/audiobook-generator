from flask import  Flask,request,render_template
from pdf_utils import *
from tts_utils import *
from PyPDF2 import PdfReader
import os
app=Flask(__name__)


# Define Voice Options (Based on the image provided)
# This list will be passed to the template.
VOICE_OPTIONS = [
    {"name": "Alloy (Female, US English)", "value": "af_alloy"},
    {"name": "Aoede (Female, US English)", "value": "af_aoede"},
    {"name": "Bella (Female, US English)", "value": "af_bella"},
    {"name": "Heart (Female, US English)", "value": "af_heart"},
    {"name": "Jessica (Female, US English)", "value": "af_jessica"},
    {"name": "Kore (Female, US English)", "value": "af_kore"},
    {"name": "Nicole (Female, US English)", "value": "af_nicole"},
    {"name": "Nova (Female, US English)", "value": "af_nova"},
    {"name": "River (Female, US English)", "value": "af_river"},
    {"name": "Sarah (Female, US English)", "value": "af_sarah"},
    {"name": "Sky (Female, US English)", "value": "af_sky"},
    {"name": "Adam (Male, US English)", "value": "am_adam"},
    {"name": "Echo (Male, US English)", "value": "am_echo"},
    {"name": "Eric (Male, US English)", "value": "am_eric"},
    {"name": "Fenrir (Male, US English)", "value": "am_fenrir"},
    {"name": "Liam (Male, US English)", "value": "am_liam"},
    {"name": "Michael (Male, US English)", "value": "am_michael"},
    {"name": "Onyx (Male, US English)", "value": "am_onyx"},
    {"name": "Puck (Male, US English)", "value": "am_puck"},
]
@app.route("/",methods=["GET","POST"])
def home():
    return render_template("home.html")

@app.route("/upload",methods=["POST"])
def upload():
    if request.method=="POST":
        file = request.files['formFile']

        if file.filename != '':
            # Save the file (you can specify any path)
            if os.path.exists("static/uploads/book.pdf"):
                os.remove("static/uploads/book.pdf")
            if file.filename.endswith(".pdf"):
                file.save(f"static/uploads/book.pdf")
            else:
                print(f"File type not supported")
                return '''
                    <h1>File type not suipported!Please wait until you get it</h1>'''
            pdf_reader = PdfReader('static/uploads/book.pdf')
            page_count = len(pdf_reader.pages)
            return render_template('display_pdf.html', 
                                pdf_path='static/uploads/book.pdf', 
                                page_count=page_count)
        
@app.route("/audio_generate",methods=["POST"])
def audio_generate():
    if request.method=="POST":
        init_page=int(request.form["initial_page"])
        end_page=int(request.form["final_page"])
        selected_voice = request.form["voice_option"]
        # text=preprocess_text(extract_specific_pages("static/uploads/book.pdf",pages=range(init_page,end_page+1)))
        text=extract_and_structure_pymupdf("static/uploads/book.pdf",pages=range(init_page,end_page+1))
        pipeline=load_pipeline()
        audio,time_taken=generate_audio(text,pipeline,filename=f'book part x pg{init_page}-{end_page} ',voice_option=selected_voice)
        high_quality_audio_path,low_quality_audio_path=save_audio(audio)
        print("Audio file written sucessfully")
        return render_template("play_audio.html",time_taken=time_taken,high_audio_path=high_quality_audio_path,low_audio_path=low_quality_audio_path)

        
if __name__=="__main__":
    app.run(debug=True)