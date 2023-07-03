import os
import soundfile as sf
from model import generate
from hparams import *

sf.write(
    os.path.join("output", "{}.wav".format(1)),
    generate("안녕하세요. 반갑습니다.")[0],
    sample_rate,
)
