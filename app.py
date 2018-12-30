from flask import Flask, request, render_template, send_from_directory
from gtts import gTTS
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

UPLOAD_FOLDER = 'static'
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/transform', methods=['POST'])
def transform():
    file = request.files['file']
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(file.stream, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    tts = gTTS(text=text, lang='el')
    tts.save('static/result.mp3')
    filename = 'result.mp3'

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        mimetype="audio/mp3",
        as_attachment=True,
        attachment_filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
