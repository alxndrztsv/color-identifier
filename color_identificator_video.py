import cv2 as cv
import pandas as pd

# read colors from the csv file;
file_path = 'colors.csv'
columns = ['color', 'color_name', 'hex', 'r', 'g', 'b']
df = pd.read_csv(file_path, names=columns, header=None)

# read vide file;
cap = cv.VideoCapture('video_resized.mp4')

# global variables;
clicked = False
r = g = b = x_pos = y_pos = 0
text = ''


def get_color(r, g, b,):
    """ Function to get color from the dataframe. """
    minimum = 10000
    color_name = ''
    for i in range(len(df)):
        distance = abs(r - int(df.loc[i, 'r'])) + \
                   abs(g - int(df.loc[i, 'g'])) + \
                   abs(b - int(df.loc[i, 'b']))
        if distance <= minimum:
            minimum = distance
            color_name = df.loc[i, 'color_name']
    return color_name


def fn_clicked(event, x, y, flags, param):
    """ Function to react on a mouse click event. """
    # if left button is clicked;
    if event == cv.EVENT_LBUTTONDOWN:
        global clicked, x_pos, y_pos
        x_pos = x
        y_pos = y
        clicked = True


while cap.isOpened():
    # capture frame by frame;
    ret, frame = cap.read()
    if ret:
        if text != '':
            # rectangle(image, up-left, length-width, color, -1 thickness fills entirely);
            cv.rectangle(frame, (0, 0), (380, 40), (b, g, r), -1)
            # putText(image, text, start, font, font scale, color, thickness, line type);
            cv.putText(frame, text, (25, 25), 2, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            # change font color to black if the background is light;
            if r + g + b >= 600:
                cv.putText(frame, text, (25, 25), 2, 0.5, (0, 0, 0), 1, cv.LINE_AA)
        cv.imshow('Frame', frame)
        if clicked:
            # get colors;
            b, g, r = frame[y_pos, x_pos]
            r = int(r)
            g = int(g)
            b = int(b)
            # text to display;
            text = get_color(r, g, b) + ' r=' + str(r) + ' g=' + str(g) + ' b=' + str(b)
            clicked = False

        if cv.waitKey(30) == ord('q'):
            break
    else:
        break

    # add a mouse click event;
    cv.namedWindow('Frame')
    cv.setMouseCallback('Frame', fn_clicked)

# release the video capture;
cap.release()

# close all frames;
cv.destroyAllWindows()
