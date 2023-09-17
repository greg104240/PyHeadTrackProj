

'''
by: Greg Jones
=============================================================================
Potential Future Features/Objectives:
Basic Reqs:
        *-Print/Label/Color Code Zones of Control for Flight Sim Implementation
        *-Make Screen Pix width, height variables
        
1-*-3D space tracking
        *-zoom in/zoom out ability 
        *-sensativity scale slider (tkinter tutorial slider: https://www.youtube.com/watch?v=knUHd8ZGyiM

2-*-compass to show how head movement would affect rotation on a compass
        *-line representing head movement x axis rotational plane
        *-line representing up down head movement y axis rotational plane
        *-indicator for zoom in/out(z axis movement)

3-*-multi point tracking
        *-multi webcam input for better tracking

3.1-*-interface with arduino servos for pov camera linked to users head(Experimental/optional)

4-*-MSFS2020 inplementation followed by DCS(if possible)
        *-ability to hardset limits of veiw
        *-auto determine hardware size for users game screen

5-*-Experimental:
        gesture tracking for button pushing, etc

6-*-Auto detect what camera code to use for openCV/CV2 module(Experimental)

7-*-Side Quest:
        *-implement on a website with a server computer using JS for user input/refined contols
        *-use facial tracking to make a facial recognition program utilizing 468 facial landmarks and storing them for comparison to other faces 
        
=============================================================================
'''
#webcam
import cv2
#face tracking
import mediapipe as mp
#debug logging
import logging
#sllider generation/GUI for user controls(exparamental)/(Slider controls)
#from tkinter import *
#from tkinker import ttk
'==============================================================================================================================='

#2D def to determine and report users tracking object location 1 Point Track for now
def ReportObjectLocation(x,y,z,width,height, deadzoneLengthX, deadzoneLengthY, deadzoneLengthZ):
        #User Deadzone:
        #will become adjustable with slider eventually, hardset to +-5degrees for X,Y,Z
        #currently tracks only X,Y, 2D only

        position = 'Empty'

        #Center
        #while int(x * width) == 350 and int(y * height) == 350:
        #center w/Deadzone(hardcoded)
        if (int(x * width) >= 345 and int(x * width) <= 355) and (int(y * height) >= 345 and int(y * height) <= 355):
                position = 'Center - Deadzone'
                logging.debug('Center - Deadzone\n')
        #else:
                #position = 'Out of Center'


        #Left 
        elif (int(x * width) < 345) or (int(x * width < 350) and int(y * height) < 345) or (int(x * width) < 350 and int(y * height) > 355):
                position = 'Left of Center/Out of Deadzone'
                logging.debug('Left of Center/Out of Deadzone\n')

        #Right
        elif (int(x * width) > 355) or (int(x * width) > 350  and int(y * height) < 345) or (int(x * width) > 350 and int(y * height) > 355):
                position = 'Right of Center/Out of Deadzone'
                logging.debug('Right of Center/Out of Deadzone\n')    

        elif (int(x * width) <= 0 and int(x * width) < 345 and int(y * height) == 350) or (int(x * width) > 355 and int(x * width) <= 700 and int(y * height) == 350) \
             or (int(y * height) <= 0 and int(y * height) < 345 and int(x * width) == 350) or (int(y * height) > 355 and int(y * height) <= 700 and int(x * width) == 350):

                position = 'Centerline - Out of Deadzone'
                logging.debug('Centerline - Out of Deadzone\n')

        else:
                position = 'Position Unknown'
                logging.debug('Position Unknown - Pos(X,Y): ', int(x * width), int(y * height), '\n')
        return position

#def generateGuidanceLines(startX, endX, startY, endY, thickness):
#def generateZones():      
#def GetScreenDimensions():

'''
**********************************************************************************************************************

Main

********************************************************************************************************************

logging Config
'''
logging.basicConfig(filename='HeadTrackerProg.log', filemode = 'w', \
                    format=' %(asctime)s - %(levelname)s - %(message)s ', encoding='utf-8',level=logging.DEBUG)
logging.debug('Start of Program\n')


#camera code depending on what camera you use code my need to change
camvid1 = cv2.VideoCapture(0)
#face mesh
faceMesh = mp.solutions.face_mesh.FaceMesh(False, 1)
mpDraw = mp.solutions.drawing_utils
drawSpecCircle = mpDraw.DrawingSpec(thickness = 3, circle_radius = 2, color = (255,0,0))
drawSpecLine = mpDraw.DrawingSpec(thickness=1, circle_radius=2,color=(0,0,255))


#face testing multi landmarks(not implementaed yet)
landMarkList = [1,2,3,4,5]


#cv2 txt
font = cv2.FONT_HERSHEY_SIMPLEX
fontSize = .5
fontColor = (0,255,0)
fontThick = 1

width = 700
height = 700

prevPosition = 'Empty'

while(True):
        ret, frame = camvid1.read()
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceMesh.process(frameRGB)

        #print(results.multi_face_landmarks)
        frame = cv2.resize(frame,(width,height))

        #draws tracking lines for testing
        cv2.line(frame, (int(int(width)/2),int(height)-int(height)),(350,700),(255,0,0),1)
        cv2.line(frame, (0,350),(700,350),(255,0,0),1)

        if results.multi_face_landmarks != None:
                for faceLandmarks in results.multi_face_landmarks:
                      count = 0
                      for lm in faceLandmarks.landmark:
                              if count == 1:#count in landMarkList:
                                      'displays number of tracked object'
                                      cv2.putText(frame, str(count),(int(lm.x*width),int(lm.y*height)),font,fontSize,fontColor,fontThick)
                                      position = ReportObjectLocation(lm.x, lm.y, 'NULL', width,height, 'NULL', 'NULL', 'NULL')
                                      if str(position) != str(prevPosition):
                                              print('Current Pos: ',position, 'Prev Position: ',prevPosition)
                                              logging.debug('Out of Center - Deadzone\n')
                                              prevPosition = position
                                              '''DEBUG - print(prevPosition)'''
                                      
                              count+= 1

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
camvid1.release()
cv2.destroyAllWindows()
logging.debug('\nEnd of Program')


