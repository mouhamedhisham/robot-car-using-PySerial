import cv2
import serial
import serial.tools.list_ports
import time

# Paths of the classifiers
speed_sign_path = 'speedlimit.xml'
stop_sign_path = 'cascade_stop_3_15.xml'
yield_sign_path = 'yieldsign12Stages.xml'

cameraNo = 0  # CAMERA NUMBER
frameWidth = 640  # DISPLAY WIDTH (original)
frameHeight = 480  # DISPLAY HEIGHT (original)
color = (255, 0, 255)  # Color for rectangle around detected objects

# Initialize camera
cap = cv2.VideoCapture(cameraNo)
cap.set(3, frameWidth)  # Set width
cap.set(4, frameHeight)  # Set height

ports = list(serial.tools.list_ports.comports())
arduino_port = None
for p in ports:
    if "CH340" in p[1]:
        arduino_port = p[0]

print(arduino_port)


# Initialize Serial Communication
arduino = serial.Serial(arduino_port, 9600)  # Replace 'COM12' with the correct port
time.sleep(2)  # Allow some time for the serial connection to establish

def empty(a):
    pass

cv2.namedWindow("Result")  # Create window for result
cv2.resizeWindow("Result", frameWidth, frameHeight + 100)  # Resize window

# Create trackbars in the 'Result' window
cv2.createTrackbar("Scale", "Result", 170, 1000, empty)
cv2.createTrackbar("Neig", "Result", 3, 50, empty)
cv2.createTrackbar("Min Area", "Result", 0, 100000, empty)
cv2.createTrackbar("Brightness", "Result", 150, 255, empty)

# Load the Haar Cascade classifiers
speed_cascade = cv2.CascadeClassifier(speed_sign_path)
stop_cascade = cv2.CascadeClassifier(stop_sign_path)
yield_cascade = cv2.CascadeClassifier(yield_sign_path)

reduce_width = 320
reduce_height = 240

# Timer to control when to send signals to Arduino
last_sent_time = 0  # To track the last time the signal was sent
delay = 1  # Delay between signals

while True:
    # Set camera brightness from trackbar
    cameraBrightness = cv2.getTrackbarPos("Brightness", "Result")  # This must come after window creation
    cap.set(10, cameraBrightness)

    # Capture frame-by-frame
    success, img = cap.read()
    if not success:
        break

    # Resize frame for faster processing
    img_resized = cv2.resize(img, (reduce_width, reduce_height))
    gray_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    
    # Adjust scale and neighbors from trackbars
    scaleVal = 1 + (cv2.getTrackbarPos("Scale", "Result") / 1000)
    neig = cv2.getTrackbarPos("Neig", "Result")

    # Detect Speed Limit signs
    speed_signs = speed_cascade.detectMultiScale(gray_resized, scaleVal, neig)
    # Detect Stop signs
    stop_signs = stop_cascade.detectMultiScale(gray_resized, scaleVal, neig)
    # Detect Yield signs
    yield_signs = yield_cascade.detectMultiScale(gray_resized, scaleVal, neig)

    detected_sign = None
    
    for (x, y, w, h) in speed_signs:
        x = int(x * frameWidth / reduce_width)
        y = int(y * frameHeight / reduce_height)
        w = int(w * frameWidth / reduce_width)
        h = int(h * frameHeight / reduce_height)
        area = w * h
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)  # Green for Speed Limit
            cv2.putText(img, 'Speed Limit', (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
            detected_sign = 'Speed Limit'

    for (x, y, w, h) in stop_signs:
        x = int(x * frameWidth / reduce_width)
        y = int(y * frameHeight / reduce_height)
        w = int(w * frameWidth / reduce_width)
        h = int(h * frameHeight / reduce_height)
        area = w * h
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)  # Blue for Stop Sign
            cv2.putText(img, 'Stop Sign', (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
            detected_sign = 'Stop Sign'

    for (x, y, w, h) in yield_signs:
        x = int(x * frameWidth / reduce_width)
        y = int(y * frameHeight / reduce_height)
        w = int(w * frameWidth / reduce_width)
        h = int(h * frameHeight / reduce_height)
        area = w * h
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)  # Red for Yield Sign
            cv2.putText(img, 'Yield Sign', (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
            detected_sign = 'Yield Sign'

    # Check if enough time has passed since the last signal was sent
    current_time = time.time()
    if current_time - last_sent_time >= delay:
        if detected_sign == 'Speed Limit':
            arduino.write(b'F')  # Send 'F' for Forward
            print("Sent to Arduino: Speed Limit (F)")

        elif detected_sign == 'Stop Sign':
            arduino.write(b'S')  # Send 'S' for Stop
            print("Sent to Arduino: Stop Sign (S)")

        elif detected_sign == 'Yield Sign':
            arduino.write(b'B')  # Send 'B' for Backward
            print("Sent to Arduino: Yield Sign (B)")

        last_sent_time = current_time  # Reset the timer

    # Show the result
    cv2.imshow("Result", img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
