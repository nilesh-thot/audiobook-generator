# 🎧 Audiobook Generator 📚🔊

Transform your PDF documents into captivating audiobooks! This application makes it super easy to convert text into speech, so you can enjoy your favorite books on the go, while multitasking, or simply give your eyes a rest.

## Features

- 📄 **Easy PDF Upload**: Simply select and upload your PDF file through our user-friendly interface.
- 🎯 **Precise Page Selection**: Don't want the whole book? No problem! Specify the exact start and end pages you want to convert.
- 🔍 **Smart Text Extraction**:
    - Efficiently pulls text from your chosen PDF pages.
    - Leverages the power of PyMuPDF for superior text extraction, intelligently preserving paragraph structures and handling pesky hyphenations for a smoother listening experience.
- 🗣️ **High-Quality Text-to-Speech (TTS)**:
    - Converts your extracted text into natural-sounding speech using the advanced Kokoro TTS engine.
    - Smartly caches the TTS pipeline, meaning subsequent audio generations are even faster! ⚡
- 🎧 **Dual Audio Output & Playback**:
    - Get your audiobook in two convenient formats: crystal-clear WAV (for the audiophiles) and compressed MP3 (for portability).
    - Listen directly in your browser with integrated playback options.

## 🚀 How to Use This Awesome App - Step-by-Step!

1.  **📤 Upload Your PDF**: Head to the main page and click the upload button. Select the PDF document you're excited to listen to. The app will quickly process it.
2.  **👀 Review & Select Pages**: Once uploaded, you'll see a preview of your PDF (or at least its path) and, crucially, the total number of pages. Now, decide which part of the book you want to hear.
3.  **🔢 Enter Page Range**: In the provided fields, type in the starting page number and the ending page number for the section you want to convert into an audiobook.
4.  **⚙️ Text Extraction Magic**: Hit the "Generate Audio" button! Behind the scenes, the app springs into action, carefully extracting the text from your selected pages using PyMuPDF. It works hard to keep paragraphs intact and fix hyphenated words, so the text is clean and ready for narration.
5.  **🎤 AI Narration**: The cleaned text is then passed to the powerful Kokoro TTS engine. This is where the magic of speech synthesis happens, turning written words into spoken audio. The first time you run it for a language, it might take a moment to load the TTS model, but thanks to caching, it'll be speedier next time!
6.  **💾 Audio Ready!**: Voilà! The application generates your audio. It saves two versions for you:
    *   A high-quality `.wav` file for the best listening experience.
    *   A compressed `.mp3` file, perfect for saving space on your devices.
7.  **▶️ Play & Enjoy**: You'll be presented with links to both audio files. Click to play them directly in your browser and immerse yourself in your newly generated audiobook!

## 🛠️ Technologies Powering This App

- **🐍 Backend**: Flask (Python) - For a lightweight and robust web server.
- **📄 PDF Processing**: PyPDF2 & PyMuPDF (fitz) - For reading and extracting text from PDFs with precision.
- **🗣️ Text-to-Speech**: Kokoro TTS (`kokoro` library) - For generating high-quality, natural-sounding speech.
- **🎶 Audio Magic**: Pydub & SoundFile - For handling audio formats, converting WAV to MP3, and saving files.

## 🚀 Getting Started

Follow these steps to get the Audiobook Generator running on your local machine.

### 1. Clone the Repository

First, clone this repository to your local machine using Git:
```bash
git clone https://github.com/nilesh-thot/audiobook-generator
cd audiobook-generator
```

### 2. Install Dependencies

This project uses Python. It's recommended to use a virtual environment.
```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the required packages
pip install -r requirements.txt
```


### 3. Run the Application

Once the dependencies are installed, you can run the Flask application:
```bash
python app.py
```
Open your web browser and navigate to `http://127.0.0.1:5000/` to use the app!

## 🤝 Contributing

We welcome contributions to make this Audiobook Generator even better! If you have ideas for new features, bug fixes, or improvements, please feel free to:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or fix (`git checkout -b feature/your-amazing-feature`).
3.  **Make your changes** and commit them (`git commit -m 'Add some amazing feature'`).
4.  **Push to the branch** (`git push origin feature/your-amazing-feature`).
5.  **Open a Pull Request** and describe your changes.

We appreciate your help in making this project awesome! 🎉
