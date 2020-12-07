import cv2
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
ret, frame = cap.read()
cv2.imshow('frame', frame)
cv2.imwrite('frame.jpg', frame)
cv2.waitKey()
cap.release()
cv2.destroyAllWindows()