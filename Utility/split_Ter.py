from pydub import AudioSegment
import math, os

class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename

        self.audio = AudioSegment.from_mp3(self.filename)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        # split_audio.export(self.folder + '\\' + split_filename, format="wav")
        split_audio.export(os.path.join(self.folder, split_filename), format="mp3")
        # split_audio.export(self.folder+'\\'+split_filename, format="mp3")
        
    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i)+'.mp3'
            self.single_split(i, i+min_per_split, split_fn)
            # print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')

def five_min_splitter(
        file = r'C:\Users\ajuga\Downloads\audiobook_LeavingTheRatRaceWithPython.mp3',
        folder = ''
):
    split_wav = SplitWavAudioMubin(folder, file)
    split_wav.multiple_split(min_per_split=5)
