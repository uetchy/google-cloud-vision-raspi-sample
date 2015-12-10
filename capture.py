import cv2
import sys

def main():
  cap = cv2.VideoCapture(0)
  ret, frame = cap.read()
  # if not frame:
  #   return 1

  half_size = cv2.pyrDown(frame)
  target_path = "target.jpg"
  cv2.imwrite(target_path, half_size)
  sys.stdout.write(target_path)

  del(cap)

main()
