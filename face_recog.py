
import subprocess

#path = //media//bhuwanesh-ug1-3317//NIIT//NU MATERIAL//NU-TERM1//DSA - GKRISH//PROJECT//face-recognition-opencv//

python3_command = "recognize_faces_image.py --encodings encoding_test.pickle --image examples/example_05.jpeg"  
# launch your python2 script using bash

process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()  # receive output from the python2 script
