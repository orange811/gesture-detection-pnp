# gesture-detection-pnp

This project is created by Piyush Jain, Neha Pattanshetti and Piyush More in our second year of college for our Bachelor's degree in Electronics and Telecommunications

Human communication has been a complex and ever-evolving phenomenon. While spoken language is the most common form of communication, other languages have been established for specific purposes.
Sign language, in particular, is used by individuals with hearing or speech impairments to communicate, through hand gestures. 
However, understanding it can be challenging.

To address this challenge, we have developed technology by using computer vision algorithms with the help of your device’s camera to read the number of fingers raised by a person in real-time and display it on a simple seven-segment display.
The display, in turn, is driven by an Arduino. Inspired by sign language, where gestures communicate messages, we aim to create a technology that could understand these gestures just like everyday English without needing to learn the language itself.

# Working of the code:
To read the number of fingers raised through the integrated camera, we capture the orientation of the hand and fingers in each frame by leveraging the OpenCV Python library.
After extracting each image frame, we will use the MediaPipe library to process these frames and detect the position of fingers by placing visual nodes (also known as hand landmarks) on them.
This will allow us to understand whether a finger is raised based on the position of the visual nodes in space. 
We then convert this information into a digital output representing the number of fingers raised. 
In the final step, this digital output is fed to an Arduino using the PyFirmata library in Python. 
We will use this Arduino board to drive a simple seven-segment display, which will show the final output, i.e., numbers.

# Conclusion:
We have transformed hand gestures into something that can now be comprehended through written language.
This project has the potential to be further developed to read English alphabets formed by using fingers as seen in sign language. 
It can act as a steppingstone to bridge the communication gap between sign language users and non-users without ever having to learn the language itself.
