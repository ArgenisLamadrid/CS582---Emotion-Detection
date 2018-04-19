# Simple program that returns the probabilites of emotion

import sys
import scipy.io.wavfile

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")
speak.Speak("Hello World")


sys.path.append("../OpenVokaturi-3-0/api")
import Vokaturi
Vokaturi.load("../OpenVokaturi-3-0/lib/open/win/OpenVokaturi-3-0-win32.dll")

file_name = input("\n Name of file please: ")

(sample_rate, samples) = scipy.io.wavfile.read(file_name)

buffer_length = len(samples)
c_buffer = Vokaturi.SampleArrayC(buffer_length)

if samples.ndim == 1:  # mono
	c_buffer[:] = samples[:] / 32768.0
else:  # stereo
	c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0

voice = Vokaturi.Voice (sample_rate, buffer_length)
voice.fill(buffer_length, c_buffer)
soundQuality = Vokaturi.Quality()

emoProbs = Vokaturi.EmotionProbabilities()
voice.extract(soundQuality, emoProbs)

if soundQuality.valid:
	print ("Neutral: %.3f" % emoProbs.neutrality)
	print ("Happy: %.3f" % emoProbs.happiness)
	print ("Sad: %.3f" % emoProbs.sadness)
	print ("Angry: %.3f" % emoProbs.anger)
	print ("Fear: %.3f" % emoProbs.fear)

	speak.Speak("Neutral: %.3f" % emoProbs.neutrality)
	speak.Speak("Happy: %.3f" % emoProbs.happiness)
	speak.Speak("Sad: %.3f" % emoProbs.sadness)
	speak.Speak("Angry: %.3f" % emoProbs.anger)
	speak.Speak("Fear: %.3f" % emoProbs.fear)
else:
	print ("Not enough sonorancy to determine emotions")

voice.destroy()
