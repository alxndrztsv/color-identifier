import cv2
import cv2 as cv
import pandas as pd


# read the image;
img_path = 'shepardFairey_02.png'
img = cv.imread(img_path)
# read colors from the csv file;
file_path = 'colors.csv'
columns = ['color', 'color_name', 'hex', 'r', 'g', 'b']
df = pd.read_csv(file_path, names=columns, header=None)

# global variables;
clicked = False
r = g = b = 0


def get_color(r, g, b,):
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


def fn_click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        global clicked, r, g, b
        clicked = True
        b, g, r = img[y, x]
        r = int(r)
        g = int(g)
        b = int(b)


# add a mouse click event;
cv.namedWindow('image')
cv.setMouseCallback('image', fn_click)


while True:
    cv.imshow('image', img)
    if clicked:
        # rectangle(image, up-left, bottom-right, color, -1 thickness fills entirely);
        cv.rectangle(img, (0, 0), (730, 40), (b, g, r), -1)
        # text to display;
        text = get_color(r, g, b) + ' r=' + str(r) + ' g=' + str(g) + ' b=' + str(b)
        # putText(image, text, start, font, font scale, color, thickness, line type);
        cv.putText(img, text, (25, 25), 2, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        # change font color to black if the background is light;
        if r + g + b >= 600:
            cv.putText(img, text, (25, 25), 2, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        clicked = False
    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()

