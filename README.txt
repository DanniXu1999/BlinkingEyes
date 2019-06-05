ATTENTION: To not make the people with small eyes disappointed, I made the determination of closed eye quite sensitive. If the project cannot detect your blinkings, please blink harder.

For testing: I already test this project on both my laptops, and it is working. If you cannot test it, you can try to watch the vedio I included or go to this link to watch this vedio: https://drive.google.com/file/d/1dmHocxmOwpbA6ZahfKrzOYFm_Cle017r/view?usp=sharing

Usage:
	This project can detect if you are starring at the computer screen for too long. If you are, it will show up the message on the screen and remind you to blink your eyes.


class Point gives you the (x,y) value of a single point in the image.

class Eye has an array of 6 points which is the points around the eyes in the picture.

class Ppl gives you the time of last time a certain person blinked eyes, and will give you a certain id for different people in the future

distance() gives you the distance of two points in the image

EAR() gives you the ratio of the closeness of an eye (the clear description of EAR is on the proposal)

in main()
	I used cv2.VideoCapture to catch the picture from the camera and then use dlib.get_frontal_face_detector to get where is the face and then I use shape_predictor_68_face_landmarks.dat to determine where the 68 points of a face are.
	Then I do a calculation for EAR and if EAR is small enough, it counts as a blink of one eye. If both eyes are blinking, the Time of this person would be reset.

For multiple people:
	I have an array of people with their previous locations and the time that they last exist. In every frame, if I have a face whose location is not close to any of the faces inside the array, that means I get a new face, so I create a new Ppl and then append it to the array of people. If there is a face inside the array of people did not exist for too long (more than 1 second), I will remove this Ppl from the array.
