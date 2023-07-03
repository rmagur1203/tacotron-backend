import os
import shutil
import numpy as np
import soundfile as sf
from datetime import datetime
from flask import Flask, send_file
from model import generate
from hparams import *
from utils.number import number_to_korean1, number_to_korean2
from utils.plot import plot_alignment
from utils.text import sequence_to_text, text_to_sequence

app = Flask(__name__)

shutil.rmtree("temp", ignore_errors=True)
os.makedirs("temp")

queue = []


def gen(hour, minute):
    if os.path.isfile("temp/root-{}-{}.wav".format(hour, minute)):
        return send_file(
            "temp/root-{}-{}.wav".format(hour, minute), mimetype="audio/wav"
        )
    if (hour, minute) in queue:
        return "이미 생성중입니다."
    queue.append((hour, minute))
    result = []
    date1 = number_to_korean1((hour - 1) % 12 + 1)
    date2 = number_to_korean2(minute)
    texts = ["안녕하세요 지금은 {}시 {}분입니다".format(date1, date2), "오늘의 날씨는 맑음입니다."]
    print(texts)
    for idx, text in enumerate(texts):
        # generate(text) returns (wav, alignment) tuple, we only need wav here
        wav, align = generate(text)
        result.append(wav)
        # append a small silence after each audio chunk
        result.append(np.zeros([int(sample_rate * 0.1)], dtype=np.float32))
        # generate alignment for each audio chunk
        plot_alignment(
            np.concatenate(align, axis=0),
            "temp/root-{}-{}-{}.png".format(hour, minute, idx),
            sequence_to_text(text_to_sequence("".join(texts))),
        )

    queue.remove((hour, minute))
    # concatenate all audio chunks
    wav = np.concatenate(result, axis=0)
    sf.write("temp/root-{}-{}.wav".format(hour, minute), wav, sample_rate)
    return send_file("temp/root-{}-{}.wav".format(hour, minute), mimetype="audio/wav")


@app.route("/")
def index():
    now = datetime.now()
    return gen(now.hour, now.minute)


@app.route("/<hour>/<minute>")
def index2(hour, minute):
    return gen(int(hour), int(minute))


@app.route("/favicon.ico")
def favicon():
    return ""


# @app.route("/align/<text>")
# def align(text):
#     if os.path.isfile("temp/{}.png".format(text)):
#         return send_file("temp/{}.png".format(text), mimetype="image/png")
#     wav, align = generate(text)
#     sf.write("temp/{}.wav".format(text), wav, sample_rate)
#     plot_alignment(
#         align, "temp/{}.png".format(text), sequence_to_text(text_to_sequence(text))
#     )
#     return send_file("temp/{}.png".format(text), mimetype="image/png")


# @app.route("/<text>")
# def hello(text):
#     if os.path.isfile("temp/{}.wav".format(text)):
#         return send_file("temp/{}.wav".format(text), mimetype="audio/wav")
#     wav, align = generate(text)
#     sf.write("temp/{}.wav".format(text), wav, sample_rate)
#     plot_alignment(
#         align, "temp/{}.png".format(text), sequence_to_text(text_to_sequence(text))
#     )
#     return send_file("temp/{}.wav".format(text), mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=True)
