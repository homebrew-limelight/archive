import grip
import cv2
import time

pipeline = grip.GripPipeline()

cap = cv2.VideoCapture(0)
time.sleep(2)

while True:
     
    ret, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edit = pipeline.process(frame)
    cv2.imshow('frame', edit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
