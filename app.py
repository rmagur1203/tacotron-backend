import os
import shutil
import soundfile as sf
from flask import Flask, send_file
from model import generate
from hparams import *
from utils.plot import plot_alignment
from utils.text import sequence_to_text, text_to_sequence

app = Flask(__name__)

shutil.rmtree("temp", ignore_errors=True)
os.makedirs("temp")


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/favicon.ico")
def favicon():
    return ""


@app.route("/align/<text>")
def align(text):
    if os.path.isfile("temp/{}.png".format(text)):
        return send_file("temp/{}.png".format(text), mimetype="image/png")
    wav, align = generate(text)
    sf.write("temp/{}.wav".format(text), wav, sample_rate)
    plot_alignment(
        align, "temp/{}.png".format(text), sequence_to_text(text_to_sequence(text))
    )
    return send_file("temp/{}.png".format(text), mimetype="image/png")


@app.route("/<text>")
def hello(text):
    if os.path.isfile("temp/{}.wav".format(text)):
        return send_file("temp/{}.wav".format(text), mimetype="audio/wav")
    wav, align = generate(text)
    sf.write("temp/{}.wav".format(text), wav, sample_rate)
    plot_alignment(
        align, "temp/{}.png".format(text), sequence_to_text(text_to_sequence(text))
    )
    return send_file("temp/{}.wav".format(text), mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=True)
