# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 13:35:11 2023

@author: niels
"""
import cv2
import math

def Vision():
    corners = []
    def getContours(img):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            
            if area > 1000:
                cv2.drawContours(imgContour, cnt, -1, (255,0,0), 2)
                perimeter = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.04 *perimeter, True) 
                objCorn = len(approx)
                x,y,w,h = cv2.boundingRect(approx)
                if objCorn == 3:
                    objectType = "Tr"
                    
                    for point in approx:
                            x_coord, y_coord = point.ravel()
                            print(f"Corner at ({x_coord}, {y_coord})")
                            corners.append(point.ravel())
                    cv2.line(imgContour, (corners[0][0],corners[0][1]), (corners[1][0],corners[1][1]),(0,0,255), 1)
                    cv2.line(imgContour, (corners[1][0],corners[1][1]), (corners[2][0],corners[2][1]),(0,0,255), 1)
                    cv2.line(imgContour, (corners[2][0],corners[2][1]), (corners[0][0],corners[0][1]),(0,0,255), 1)
                elif objCorn == 4:
                    aspectratio = w/float(h)
                    if aspectratio > 0.85 and aspectratio < 1.15: 
                        objectType = 'Sqr'
                    else:  
                        objectType= 'Rct'
                        print('Rectangle')
                        print("Area:", area)
                        
                        # Print corner coordinates
                        
                elif objCorn > 4:
                    objectType = 'Cir'
                else:
                    objectType = 'None'
                   
                    
                
                cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0,255,0), 1)
                cv2.putText(imgContour, objectType,(x+(w//2)-10, y+(h//2)),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,255),1)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    def angles(points):
        def distance(p1, p2):
            return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        
        def angle(a, b, c):
            return math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))
    
        point1, point2, point3 = points
    
        a = distance(point2, point3)
        b = distance(point1, point3)
        c = distance(point1, point2)
    
        angle_A = angle(b, c, a)
        angle_B = angle(c, a, b)
        angle_C = angle(a, b, c)
        cv2.putText(imgContour, f'A =', (corners[0][0]-15,corners[0][1]-5), cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,255))
        print('de hoek van de magneet is: ', angle_C)
        
        return angle_A, angle_B, angle_C
    
    imgr = cv2.imread('maskPATS.jpg')
    img = cv2.resize(imgr, (1920,1080))
    
    imgContour = img.copy()
    
    imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgB = cv2.GaussianBlur(imgG, (5,5), 1) # laatste is sigma hoe hoger hoe meer blur
    imgC = cv2.Canny(imgB,50,50) 
    getContours(imgC)
    #angles(corners)
    cv2.imshow('maskree', imgContour)
    
Vision()




