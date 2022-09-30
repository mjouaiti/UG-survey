import re
import crepe
import numpy as np

import language_check
tool = language_check.LanguageTool('en-US')

mock_transcript = "Yeah, like, I don't know but maybe I'll be an engineer"
transcript = mock_transcript

fillers = ["uh", "um", "like", "you know", "I don’t know", "kind of", "sort of"]
maybes = ["maybe", "may ", "might", "perhaps", "I don’t know"]

_pitch, _volume = [], []
_rate, _silence = [], []
_fillers, _maybe = [], []

def transcript_analysis(transcript):
    nb_words = len(transcript.split(" "))
    nb_fillers = 0
    nb_maybes = 0
    for filler in fillers:
        nb_fillers += len([m.start() for m in re.finditer(filler, transcript)])
    for maybe in maybes:
        nb_maybes += len([m.start() for m in re.finditer(maybe, transcript)])
        
    _fillers.append(nb_fillers/nb_words)
    _maybe.append(nb_maybes/nb_words)
    
    
    matches = tool.check(text)
#    language_check.correct(text, matches)

    print("% of fillers: ", _fillers[-1])
    print("% of maybe: ", _maybe[-1])
    print("# of grammatical errors: ", len(matches))
    
    
def speech_analysis(speech):
    global _pitch, _volume
    audio, sr = librosa.load(speech, sr= 8000, mono=True)
    audio = librosa.effects.trim(audio, top_db= 10)
    clips = librosa.effects.split(audio, top_db=10)
    words = []
    for c in clips:
        data = audio[c[0]: c[1]]
        words.extend(data)
    
    _, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True, verbose=0)

    _pitch.append(np.mean(frequency))
    _volume.append(np.max(audio))
    _silence.append((len(audio) - len(words)) / len(audio))
    _rate.append(len(clips) / (len(audio) / sr))
    
    print("Pitch: ", _pitch[-1])
    print("Silence: ", (len(audio) - len(words)) / len(audio))
    print("Speech rate: ", len(clips) / (len(audio) / sr))
    
def summary():
    feedback = "I have analysed your speech and here is some advice that I can give you."
    
    if np.var(_pitch) > THRESHOLD:
        feedback += "There were a lot of variations in the pitch of your voice. Try to stabilise your voice."
    elif np.var(_volume) > THRESHOLD:
        feedback += "There were a lot of variations in the volume of your voice. Try to stabilise your voice."
    if np.mean(_silence) > 0.2:
        feedback += "You are taking long pauses when you speak, try to reduce pauses to appear confident."
    elif np.mean(_silence) < 0.05:
        feedback += "You are not taking any pauses when you speak, this makes it harder to understand you."
    
    if np.mean(_rate) * 60 > 150:
        feedback += "Your speech rate is too high, try to speak slower"
    elif np.mean(_rate) * 60 < 110:
        feedback += "Your speech rate is too low, try to speak a little faster"
        
    if np.mean(_fillers) > 0.1:
        feedback += "You are using a lot of filler words when you speak, this makes you appear hesitant, try to be more confident and assertive."
    if np.mean(_maybe) > 0.1:
        feedback += "You are using a lot of filler words when you speak, this makes you appear unsure, try to be more confident and assertive."
        
    return feedback

if __name__ == "__main__":
    transcript_analysis(transcript)
