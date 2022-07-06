import cv2
import numpy as np

# Create a VideoCapture object
cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture('outpy.avi')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

while(True):
    _, frame = cap.read()
    _, frame2 = cap2.read()

    if _ == True:

        # Write the frame into the file 'output.avi'
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        cv2.imshow('output', frame2)

        # Press Q on keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

    # When everything done, release the video capture and video write objects
cap.release()
cap2.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()