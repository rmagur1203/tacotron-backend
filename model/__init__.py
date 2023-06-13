import scipy
import librosa
import numpy as np
import tensorflow as tf

from utils.text import text_to_sequence
from .modules import griffin_lim
from .tacotron import Tacotron, post_CBHG
from hparams import *


tacotron = Tacotron(K=16, conv_dim=[128, 128])
tf.train.Checkpoint(model=tacotron).restore(
    tf.train.latest_checkpoint("./checkpoint/1")
).expect_partial()

cbhg = post_CBHG(K=8, conv_dim=[256, mel_dim])
tf.train.Checkpoint(model=cbhg).restore(
    tf.train.latest_checkpoint("./checkpoint/2")
).expect_partial()


def generate(text):
    seq = text_to_sequence(text)
    seq_len = int(len(seq) * 1.5)
    enc_input = np.asarray([seq], dtype=np.int32)
    sequence_length = np.asarray([len(seq)], dtype=np.int32)
    dec_input = np.zeros((1, seq_len, mel_dim), dtype=np.float32)

    pred = []
    for i in range(1, seq_len + 1):
        print("step: {}/{}".format(i, seq_len))
        mel_out, alignment = tacotron(
            enc_input, sequence_length, dec_input, is_training=False
        )
        if i < seq_len:
            dec_input[:, i, :] = mel_out[:, reduction * i - 1, :]
        pred.extend(mel_out[:, reduction * (i - 1) : reduction * i, :])

    mel = np.reshape(np.asarray(pred), [-1, mel_dim])

    mel = np.expand_dims(mel, axis=0)
    pred = cbhg(mel, is_training=False)

    pred = np.squeeze(pred, axis=0)
    pred = np.transpose(pred)

    pred = (np.clip(pred, 0, 1) * max_db) - max_db + ref_db
    pred = np.power(10.0, pred * 0.05)
    wav = griffin_lim(pred**1.5)
    wav = scipy.signal.lfilter([1], [1, -preemphasis], wav)
    wav = librosa.effects.trim(wav, frame_length=win_length, hop_length=hop_length)[0]
    wav = wav.astype(np.float32)

    return wav, alignment
