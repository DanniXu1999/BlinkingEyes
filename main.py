import cv2
import numpy
import dlib
import sys
import math
import time
from cv2 import FONT_HERSHEY_COMPLEX
import face_recognition

class Point:
    def __init__(self, XValue, YValue):
        self.XValue=XValue
        self.YValue=YValue

class Eye:
    def __init__(self, pointArr, blink):
        self.pointArr=pointArr
        self.blink=blink

class Ppl:
    def __init__(self, time, id, next):
        self.time=time
        self.id=id
        self.next=next
        
def distance(p1, p2):
    return math.sqrt((p1.XValue-p2.XValue)**2+(p1.YValue-p2.YValue)**2)
    
def EAR(pointArr):
    ratio=distance(pointArr[1], pointArr[5])+distance(pointArr[2], pointArr[4])
    ratio=ratio/(2*distance(pointArr[0], pointArr[3]))
    #print(ratio)
    if (ratio<0.14) :
        return True
    else :
        return False
    
def sameface(face1, face2):
    result=face_recognition.compare_faces([face1.id], face2.id)
    return result[0]
    
def main():
    capture=cv2.VideoCapture(0)
    myFace=dlib.get_frontal_face_detector()
    landMark=dlib.shape_predictor("c:/Users/shape_predictor_68_face_landmarks.dat")
    t0=time.clock()
    _,pic=capture.read()
    faces=myFace(pic)
    num=len(faces)
    if num==0:
        print("You need a face to use the program!")
        return
    #print(num)
    #head=Ppl(0, 0, None)
    #crop_img = pic[faces[0].top():faces[0].bottom(), faces[0].left():faces[0].right()]
    #while True:
    #    array=face_recognition.face_encodings(crop_img)
    #    if len(array)>0:
    #        head.id=array[0]
    #        break
    #    else:
    #        continue
    #if num>1:
    #    ptr=head
    #    for face in faces:
    #        tempPeople=Ppl(0,0,None)
    #        crop_img = pic[face.top():face.bottom(), face.left():face.right()]
    #        while True:
    #            array=face_recognition.face_encodings(crop_img)
    #            if len(array)>0:
    #                tempPeople.id=array[0]
    #                break
    #            else:
    #                continue
    #            if (sameface(head,tempPeople)):
    #                continue
    #        ptr.next=tempPeople
    people=[]
    for j in range (0, num):
        tempPeople=Ppl(0,0, None)
        people.append(tempPeople) 
    
    while True:
        success, img=capture.read()
    
        faces=myFace(img)
        if len(faces)<num:
            for j in range(len(faces), num):
                people[j].time=0
        elif len(faces)>num:
            for j in range(num, len(faces)):
                tempPeople=Ppl(0,0, None)
                people.append(tempPeople)
        l=0
        for face in faces: #it should work for multiple faces
            top=face.top()
            bottom=face.bottom()
            left=face.left()
            right=face.right()
            allpoints=landMark(img, face)
            #tempPeople=Ppl(0,0,None)
            #crop_img = pic[face.top():face.bottom(), face.left():face.right()]
            #array=face_recognition.face_encodings(crop_img)
            #if len(array)>0:
            #    tempPeople.id=array[0]
            #else:
            #    continue
            #ptr=head
            #exist=False
            #while ptr!=None:
            #    if sameface(tempPeople, ptr):
            #        exist=True
            #        break
            #    ptr=ptr.next;
            #if exist==False:
            #    tempHead=Ppl(0,0,None)
            #    crop_img = pic[face.top():face.bottom(), face.left():face.right()]
            #    array=face_recognition.face_encodings(crop_img)
            #    if len(array)>0:
            #        tempPeople.id=array[0]
            #    else:
            #        continue
            #    tempHead.next=head
            #    head=tempHead
            #    ptr=head
            #exist=False
            
            if people[l].time==0:
                people[l].time=time.clock()
            elif time.clock()-people[l].time>8:
                cv2.putText(img,"Blink Your Eye or You Are BLind", (left-100, bottom),FONT_HERSHEY_COMPLEX,0.5, (151, 38, 38),1,7)
            timer="You didn't blink for "+str(round(time.clock()-people[l].time, 2))+ " seconds" 
            cv2.putText(img,timer,(left-100,top),FONT_HERSHEY_COMPLEX,0.5, (151, 38, 38),1,7)
        #cv2.rectangle(img, (left, top), (right, bottom), (255,255,255), 2)#img, (x,y) facelanmarks, color,width 
            leftEye=Eye(None, False)
            rightEye=Eye(None, False)
            tempArr= []
            for i in range(36, 42):
                temp=Point(allpoints.part(i).x,allpoints.part(i).y)
                tempArr.append(temp)
                x=allpoints.part(i).x
                y=allpoints.part(i).y
                cv2.circle(img, (x,y), 2, (63,71, 44), -1)
                cv2.putText(img,str(i-36), (x,y),FONT_HERSHEY_COMPLEX,0.3, (255, 68, 26),1,7)
            leftEye.pointArr=tempArr
            tempArr=[]
            for i in range(42, 48):
                temp=Point(allpoints.part(i).x, allpoints.part(i).y)
                tempArr.append(temp)
                x=allpoints.part(i).x
                y=allpoints.part(i).y
                cv2.circle(img, (x,y), 2, (240, 65, 85), -1)
                cv2.putText(img,str(i-42), (x,y),FONT_HERSHEY_COMPLEX,0.3, (255, 68, 26),1,7)
            rightEye.pointArr=tempArr
            rightEye.blink=EAR(rightEye.pointArr)
            leftEye.blink=EAR(leftEye.pointArr)
            #print(rightEye.blink)
            if (rightEye.blink & leftEye.blink):
                #print ("blink")#the timer restart
                people[l].time=time.clock()  
            l=l+1
              
        cv2.imshow('Image', img)
        key=cv2.waitKey(1)
        if key==27:
            break

main()