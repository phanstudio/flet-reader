import subprocess
import os
from vosk import Model, KaldiRecognizer, SetLogLevel
from .constants import ROOTPATH

def exctractors_srt(url, num, nam):
    SAMPLE_RATE = 44100
    SetLogLevel(-1)

    model = Model(os.path.join(ROOTPATH,'models','M3-sm2'),lang="en-us")
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)

    with subprocess.Popen(
        [
            "ffmpeg", 
            "-loglevel", 
            "quiet", 
            "-i",
            url,
            "-ar", 
            str(SAMPLE_RATE) , 
            "-ac", 
            "1", 
            "-f", 
            "s16le", 
            "-",
        ],
        stdout=subprocess.PIPE).stdout as stream:

        
        # writing the string to a new file
        subtt = os.path.join(ROOTPATH,'Books',f'{nam}','sub')
        srtout = os.path.join(subtt, f'{num}.srt')
        if not os.path.exists(subtt):
            os.makedirs(subtt)
        with open(srtout, 'w') as newfile:
            newfile.write(rec.SrtResult(stream, 15))
