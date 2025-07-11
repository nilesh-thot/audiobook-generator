from flask import Flask, request, render_template, url_for # Added url_for
from pdf_utils import *  # Assuming this contains extract_and_structure_pymupdf
from tts_utils import *
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])  # Assuming POST is for some other functionality or future use
def home():
    return render_template("home.html")

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        if 'formFile' not in request.files:
            # Handle case where no file part is in the request
            return "No file part in the request.", 400

        file = request.files['formFile']

        if file.filename == '':
            # Handle case where no file is selected
            return "No file selected.", 400

        if file and file.filename.endswith(".pdf"):
            # Ensure the target directory exists
            upload_folder = "uploads"
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            pdf_save_path = os.path.join(upload_folder, "book.pdf")

            if os.path.exists(pdf_save_path):
                try:
                    os.remove(pdf_save_path)
                except OSError as e:
                    print(f"Warning: Could not remove existing file {pdf_save_path}: {e}")

            file.save(pdf_save_path)

            try:
                pdf_reader = PdfReader(pdf_save_path)
                page_count = len(pdf_reader.pages)
            except Exception as e:
                print(f"Error reading PDF {pdf_save_path}: {e}")
                return "Error processing PDF file. Please ensure it's a valid PDF.", 500

            # pdf_path for the template should be relative to the 'static' folder
            # if src="{{ url_for('static', filename=pdf_path_relative_to_static) }}" is used,
            # or the direct web path if not.
            # Given src="{{ pdf_path }}" in original template, and we save to 'static/uploads/book.pdf',
            # this path should be 'uploads/book.pdf' if template uses url_for('static', filename=pdf_path)
            # OR 'static/uploads/book.pdf' if the template directly uses src="{{ pdf_path }}" and static is served at root.
            # The updated display_pdf.html uses url_for, so we pass path relative to static.
            pdf_display_path_for_template = "uploads/book.pdf"

            return render_template('display_pdf.html',
                                   pdf_path=pdf_display_path_for_template, # Path for url_for('static', ...)
                                   page_count=page_count,
                                   voices=VOICE_OPTIONS) # Pass voice options to the template
        else:
            print(f"File type not supported: {file.filename}")
            return '''
                <h1>File type not supported! Only PDF files are allowed.</h1>
                <p><a href="/">Go back</a></p>'''

@app.route("/audio_generate", methods=["POST"])
def audio_generate():
    if request.method == "POST":
        try:
            init_page = int(request.form["initial_page"])
            end_page = int(request.form["final_page"])
            selected_voice = request.form["voice_option"] # Get selected voice

            if not (1 <= init_page <= end_page):
                 return "Invalid page range selected.", 400

        except ValueError:
            return "Invalid page numbers or voice option provided.", 400
        except KeyError:
            return "Missing form data (page numbers or voice option).", 400

        pdf_file_path = "static/uploads/book.pdf"
        if not os.path.exists(pdf_file_path):
            return "Uploaded PDF not found. Please re-upload.", 404

        # text=preprocess_text(extract_specific_pages("static/uploads/book.pdf",pages=range(init_page,end_page+1)))
        text = extract_and_structure_pymupdf(pdf_file_path, pages=range(init_page, end_page + 1))

        if not text or not text.strip():
            return "No text could be extracted from the selected PDF pages.", 400

        try:
            # Assuming KPipeline handles lang_code based on voice or a default like 'a' is fine.
            pipeline = load_pipeline() # from tts_utils
            # Pass the selected_voice to generate_audio
            audio_data, time_taken = generate_audio(text, pipeline, voice_option=selected_voice)

            if audio_data is None:
                # generate_audio should ideally raise an exception or return an error indicator
                print("Audio generation failed (audio_data is None).")
                return "Audio generation failed. Check server logs.", 500

        except Exception as e:
            print(f"Error during TTS processing or audio generation: {e}")
            return f"An error occurred during audio generation: {str(e)}", 500

        # Ensure static/uploads directory exists for saving audio
        audio_output_folder = "static/" # Save audio in the same folder as PDF
        if not os.path.exists(audio_output_folder):
            os.makedirs(audio_output_folder)

        high_quality_audio_path, low_quality_audio_path = save_audio(audio_data, output_path_folder=audio_output_folder,file_name=f"book part x pg{init_page}-{end_page}")

        print("Audio file written successfully")

        # For play_audio.html, pass paths relative to static folder for url_for
        # hq_path_for_template = os.path.relpath(high_quality_audio_path, 'static')
        # lq_path_for_template = os.path.relpath(low_quality_audio_path, 'static')

        return render_template("play_audio.html",
                               time_taken=time_taken,
                               high_audio_path=high_quality_audio_path,
                               low_audio_path=low_quality_audio_path)
    return "Invalid request method.", 405 # Should not happen with POST route

if __name__ == "__main__":
    # Ensure the static directory and uploads subdirectory exist at startup
    if not os.path.exists("static"):
        os.makedirs("static")
    if not os.path.exists("static/uploads"):
        os.makedirs("static/uploads")

    app.run(debug=True)
