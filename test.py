from gtts import gTTS

tts = gTTS("Hello, this is GeneGuide AI.", lang="en")

tts.save("voice.mp3")

print("Done!")