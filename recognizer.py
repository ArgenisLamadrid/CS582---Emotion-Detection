# Argenis Lamadrid, Nicholas Otero, Asislo Alfiler
# CS 582 2018
# Calculates a score of emotions over a set of given .wav filetypes
# .wav Files must be in the same directory as recognizer.py

import sys
import scipy.io.wavfile
sys.path.append("../OpenVokaturi-3-0/api")
import Vokaturi

emoNeut = emoHapp = emoSad = emoAnger = emoFear = 0.0
files = []
fileCount = 0;
osLoaded = False

print("1 for linux32 ")
print("2 for linux64 ")
print("3 for mac32 ")
print("4 for mac64 ")
print("5 for win32 ")
print("6 for win64 ")
selection = input("Please select os version: ")

#while loop for selecting the os version
while(osLoaded == False):
	if selection == '1':
		print("Loading...")
		Vokaturi.load("../OpenVokaturi-3-0/lib/open/linux/OpenVokaturi-3-0-linux32.so")
		osLoaded = True
		print("OS loaded")

	elif selection == '2':
		print("Loading...")
		Vokaturi.load("../OpenVokaturi-3-0/lib/open/linux/OpenVokaturi-3-0-linux64.so")
		osLoaded = True
		print("OS loaded")

	elif selection == '3':
		print("Loading...")
		Vokaturi.load("../OpenVokaturi-3-0/lib/open/macos/OpenVokaturi-3-0-mac32.dylib")
		osLoaded = True
		print("OS loaded")

	elif selection == '4':
		print("Loading...")
		Vokaturi.load("../OpenVokaturi-3-0/lib/open/macos/OpenVokaturi-3-0-mac64.dylib")
		osLoaded = True
		print("OS loaded")

	elif selection == '5':
		print("Loading...")
		Vokaturi.load("../OpenVokaturi-3-0/lib/open/win/OpenVokaturi-3-0-win32.dll")
		osLoaded = True
		print("OS loaded")

	elif selection == '6':
		print("Loading...")
		Vokaturi.load("../OpenVokaturi-3-0/lib/open/win/OpenVokaturi-3-0-win64.dll")
		osLoaded = True
		print("OS loaded")

	else:
		selection = input("Please select a valid os version: ")
#end of while loop

# until 'done' command is given take file names from user input, increment fileCount
#'done' command is last entry in files[]
file_name = input("\n please input the name of your first file: ")
files.append(file_name)
fileCount += 1

while(file_name != 'done'):
	file_name = input("\n please input the name of your next file, type 'done' when finished: ")
	files.append(file_name)
	fileCount += 1

#calculates emotion probabilites from files[] - the last entry
#
for i in range(fileCount - 1):
	print("Calculating...")
	print('-- ' + files[i])

	file_name = files[i]
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
		emoNeut += emoProbs.neutrality
		emoHapp += emoProbs.happiness
		emoSad += emoProbs.sadness
		emoAnger += emoProbs.anger
		emoFear += emoProbs.fear

	else:
		print ("Not enough sonorancy to determine emotions")

	voice.destroy()
# end of for loop

print("\n" + str(fileCount-1) + "  file(s) total" + "\n")

if (emoNeut >= emoHapp and emoNeut >= emoSad and emoNeut >= emoAnger and emoNeut >= emoFear):
	print("Neutral, Confidence: %.2f" % ((emoNeut / (fileCount-1))* 100) + "%" )

elif (emoHapp >= emoNeut and emoHapp >= emoSad and emoHapp >= emoAnger and emoHapp >= emoFear):
	print("Happy, Confidence: %.2f" % ((emoHapp / (fileCount-1))* 100) + "%")

elif (emoSad >= emoNeut and emoSad >= emoHapp and emoSad >= emoAnger and emoSad >= emoFear):
	print("Sad, Confidence: %.2f" % ((emoSad / (fileCount-1))* 100) + "%")

elif (emoAnger >= emoNeut and emoAnger >= emoHapp and emoAnger >= emoSad and emoAnger >= emoFear):
	print("Angry, Confidence: %.2f" % ((emoAnger / (fileCount-1))* 100) + "%")

elif (emoFear >= emoNeut and emoFear >= emoHapp and emoFear >= emoSad and emoFear >= emoAnger):
	print("Fear, Confidence: %.2f" % ((emoFear / (fileCount-1))* 100) + "%")
