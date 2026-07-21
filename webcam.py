import cv2
import numpy as np


camera_data = { "hsv_frame": None}

# Prints The HSV Value Of the Pixel Clicked By The Mouse 
def show_hsv_value(event, x, y, flags, data):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_image = data["hsv_frame"]

        if hsv_image is None:
            return

        pixel = hsv_image[y, x]

        hue = pixel[0]
        saturation = pixel[1]
        value = pixel[2]

        print( f"Clicked HSV: " f"H={hue}, S={saturation}, V={value}" )

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow("NAVI Camera Test")

if not camera.isOpened():
    print("Camera could not be oepened.")
    raise SystemExit

cv2.setMouseCallback( "NAVI Camera Test",show_hsv_value, camera_data)

# While Camera Is Running
while True:
    # Splits Input Into True/False and Frame
    result = camera.read()
    success= result[0]
    frame= result[1]

    # Exits If Camera Doesn't Connect
    if not success:
        print("Frame was not captured.")
        break

    # Converts BGR To HSV
    hsv_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
    camera_data["hsv_frame"] = hsv_frame  

    # Green Pixel Range For Min And Max
    lower_green=np.array([35,30,50]) # Hue, Saturation, Value
    upper_green=np.array([90,255,255])

    # Red Pixel Range For Min And Max
    lower_red_1=np.array([0,210,100])
    upper_red_1=np.array([10,255,255]) 
    lower_red_2=np.array([170,210,100]) # Red Wraps Around Hue Scale
    upper_red_2=np.array([179,255,255])

    # Makes Green Pixels White, Other Pixels Black
    green_mask= cv2.inRange(hsv_frame,lower_green,upper_green)
    red_mask_1=cv2.inRange(hsv_frame,lower_red_1,upper_red_1)
    red_mask_2=cv2.inRange(hsv_frame,lower_red_2,upper_red_2)
    red_mask=cv2.bitwise_or(red_mask_1,red_mask_2)

    # Determines If It Is Real Object
    green_pixel_count=cv2.countNonZero(green_mask)
    red_pixel_count=cv2.countNonZero(red_mask)
  

    # Detection
    green_detected=green_pixel_count >700
    
    red_detected=red_pixel_count>700

    if red_detected:
        status= "RED HAZARD DETECTED"
        command= "STOP"
        text_color=(0,0,255)
    
    elif green_detected:
        status="GREEN TARGET DETECTED"
        command = "MOVE FORWARD"
        text_color=(0,255,0)

    else:
        status="NO TARGET DETECTED"
        command= "STOP"
        text_color=(0,165,255)

    # Display Text In Window
    cv2.putText(frame, f"COMMAND: {command}", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)
    cv2.putText(frame, status, (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)

    # Shows Frames In Windows
    cv2.imshow("NAVI Camera Test",frame)
    cv2.imshow("NAVI HSV Test",hsv_frame)
    cv2.imshow("NAVI Green Mask Test",green_mask)
    cv2.imshow("NAVI Red Mask Test",red_mask)

    # Waits 1 Milisecond For Camera To Process
    cv2.waitKey(1)
  
camera.release()
cv2.destroyAllWindows()