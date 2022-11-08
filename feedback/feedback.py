import re
import crepe
import numpy as np

import language_check
import librosa
tool = language_check.LanguageTool('en-US')

mock_transcript = "Yeah, like, I don't know but maybe I'll be an engineer"
transcript = mock_transcript

fillers = ["uh", "um", "like", "you know", "I don’t know", "kind of", "sort of"]
maybes = ["maybe", "may ", "might", "perhaps", "I don’t know"]

class Feedback():

    def __init__(self):
        self._pitch, self._volume = [], []
        self._rate, self._silence = [], []
        self._fillers, self._maybe = [], []
        self._errors = []

    def transcript_analysis(self, transcript):
        nb_words = len(transcript.split(" "))
        nb_fillers = 0
        nb_maybes = 0
        for filler in fillers:
            nb_fillers += len([m.start() for m in re.finditer(filler, transcript)])
        for maybe in maybes:
            nb_maybes += len([m.start() for m in re.finditer(maybe, transcript)])
            
        self._fillers.append(nb_fillers/nb_words)
        self._maybe.append(nb_maybes/nb_words)
        
        
        matches = tool.check(transcript)
        self._errors.append(matches)
    #    language_check.correct(text, matches)

        print("% of fillers: ",self. _fillers[-1])
        print("% of maybe: ", self._maybe[-1])
        print("# of grammatical errors: ", len(matches))
          
    def speech_analysis(self, speech):
        global _pitch, _volume
        audio, sr = librosa.load(speech, sr= 8000, mono=True)
        audio = librosa.effects.trim(audio, top_db= 10)
        clips = librosa.effects.split(audio, top_db=10)
        words = []
        for c in clips:
            data = audio[c[0]: c[1]]
            words.extend(data)
        
        _, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True, verbose=0)

        self._pitch.append(np.mean(frequency))
        self._volume.append(np.max(audio))
        self._silence.append((len(audio) - len(words)) / len(audio))
        self._rate.append(len(clips) / (len(audio) / sr))
        
        print("Pitch: ", _pitch[-1])
        print("Silence: ", (len(audio) - len(words)) / len(audio))
        print("Speech rate: ", len(clips) / (len(audio) / sr))
        
    def summary(self):
        feedback = "I have analysed your speech and here is some advice that I can give you."
        
        if np.var(self._pitch) > THRESHOLD:
            feedback += "There were a lot of variations in the pitch of your voice. Try to stabilise your voice."
        elif np.var(self._volume) > THRESHOLD:
            feedback += "There were a lot of variations in the volume of your voice. Try to stabilise your voice."
        if np.mean(self._silence) > 0.2:
            feedback += "You are taking long pauses when you speak, try to reduce pauses to appear confident."
        elif np.mean(self._silence) < 0.05:
            feedback += "You are not taking any pauses when you speak, this makes it harder to understand you."
        
        if np.mean(self._rate) * 60 > 150:
            feedback += "Your speech rate is too high, try to speak slower"
        elif np.mean(self._rate) * 60 < 110:
            feedback += "Your speech rate is too low, try to speak a little faster"
            
        if len(self._errors) > 10:
            feedback += "There are a number of grammatical errors in your speech, which makes it harder to understand you. You should practice your English."
            
        if np.mean(self._fillers) > 0.1:
            feedback += "You are using a lot of filler words when you speak, this makes you appear hesitant, try to appear more confident and assertive."
        elif np.mean(self._maybe) > 0.1:
            feedback += "You are using a lot of filler words when you speak, this makes you appear unsure, try to appear more confident and assertive."
            
        return feedback

if __name__ == "__main__":
    f = Feedback()
    f.transcript_analysis(transcript)
    f.speech_analysis([0]*100)
    f.summary()
