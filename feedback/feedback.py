import re
import crepe

mock_transcript = "Yeah, like, I don't know but maybe I'll be an engineer"
transcript = mock_transcript

fillers = ["uh", "um", "like", "you know", "I don’t know", "kind of", "sort of"]
maybes = ["maybe", "may ", "might", "perhaps", "I don’t know"]

_pitch, _volume = [], []

def transcript_analysis(transcript):
    nb_words = len(transcript.split(" "))
    nb_fillers = 0
    nb_maybes = 0
    for filler in fillers:
        nb_fillers += len([m.start() for m in re.finditer(filler, transcript)])
    for maybe in maybes:
        nb_maybes += len([m.start() for m in re.finditer(maybe, transcript)])
        
    print("% of fillers: ", nb_fillers/nb_words)
    print("% of maybe: ", nb_maybes/nb_words)
    
    
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
    
    print("Pitch: ", _pitch[-1])
    print("Silence: ", (len(audio) - len(words)) / len(audio))
    print("Speech rate: ", len(clips) / (len(audio) / sr))
    
    

### problem with Google API is that it either ignores filler words or detects something very irrelevant, like mum instead of hum or are instead of eeh.

if __name__ == "__main__":
    transcript_analysis(transcript)
