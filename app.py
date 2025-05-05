from flask import  Flask,request,render_template
from pdf_utils import *
from tts_utils import *
from PyPDF2 import PdfReader
import os
app=Flask(__name__)

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
        # text=preprocess_text(extract_specific_pages("static/uploads/book.pdf",pages=range(init_page,end_page+1)))
        text=extract_and_structure_pymupdf("static/uploads/book.pdf",pages=range(init_page,end_page+1))
        pipeline=load_pipeline()
        audio,time_taken=generate_audio(text,pipeline)
        audio_path_folder,low_quality_audio_path,high_quality_audio_path=save_audio(audio)
        print("Audio file written sucessfully")
        return render_template("play_audio.html",time_taken=time_taken,low_quality_audio_path=low_quality_audio_path,high_quality_audio_path=high_quality_audio_path)    #"static/audio.flac")
        
if __name__=="__main__":
    app.run(debug=True)