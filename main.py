
# PixelArtCode
import cv2
from tkinter import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Creating a dialog box for selecting a file
def selecting_file():
    Tk().withdraw()
    file_name = askopenfilename()
    return file_name


# Saving an image with adding "EDIT" at the end of the file to the source folder
def save_image(image, image_name):
    symbol_index = image_name.rfind('.')
    image_name = image_name[:symbol_index] + "_EDIT" + image_name[symbol_index:]
    cv2.imwrite(image_name, image)


def save_video(video, video_name):
    pass


# Drawing an image on the screen
def draw_image(image, image_name, pixel_size):
    cv2.imshow(f"PixelArt, size = {pixel_size}", image)
    key = cv2.waitKey(0)
    if key == 115:
        save_image(image, image_name)
    cv2.destroyAllWindows()


# Converting an image to pixel art
def conversion_to_pixel(image, pixel_size=15):
    width = int(image.shape[1])
    height = int(image.shape[0])
    # resolution of the final image
    pixel_height = int((height - pixel_size) / pixel_size) + 1
    pixel_width = int((width - pixel_size) / pixel_size) + 1
    half_pixel_size = int(pixel_size / 2)
    for y in range(0, height - pixel_size + 1, pixel_size):
        for x in range(0, width - pixel_size + 1, pixel_size):
            pixel_color = image[y + half_pixel_size, x + half_pixel_size]
            image[y:y + pixel_size, x:x + pixel_size] = pixel_color
    cropped_image = image[0:pixel_height * pixel_size, 0:pixel_width * pixel_size]
    return cropped_image


# Pixelation of the video stream
def pixel_video(video, pixel_size):
    while True:
        ret, frame = video.read()
        key = cv2.waitKey(1)
        if not ret or (key & 0xFF in [27, 32, 113]):
            break
        image = conversion_to_pixel(frame, pixel_size)
        cv2.imshow("frame", image)
    video.release()
    cv2.destroyAllWindows()


# Pixel art of a single image
def image_pixel_art():
    pixel_size = int(txt.get())
    image_name = selecting_file()
    if image_name == '':
        print('missing the input image')
        return -1
    image = cv2.imread(image_name)
    pixel_img = conversion_to_pixel(image, pixel_size)
    draw_image(pixel_img, image_name, pixel_size)


# Pixelation of video and output to the screen
def video_pixel_art():
    pixel_size = int(txt.get())
    video_name = selecting_file()
    if video_name == '':
        print('missing the input video')
        return -1
    video = cv2.VideoCapture(video_name)
    pixel_video(video, pixel_size)


# Pixelate webcam video and display it on the screen
def webcam_pixel_art():
    pixel_size = int(txt.get())
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    pixel_video(video, pixel_size)


# The formation of the main window
window = Tk()
icon = PhotoImage(file="data/icon.png")
window.iconphoto(False, icon)
window.geometry("700x400+300+350")
window.resizable(False, False)
window.title("Python Art by FriLDD")
window.config(bg="#33cccc")


# Text on the main window
lbl = Label(window,
            text="Enter the pixel size",
            font=("Arial", 20, "bold"),
            bg="#33cccc"
            )
lbl.place(x=20, y=20)

# Text input window options
txt = Entry(window, width=5, font=("Arial", 15, "bold"))
txt.place(x=20, y=60)
txt.insert(0, "20")
txt.focus()

# Calling functions based on clicks
image_button = Button(window, text="image_button", command=image_pixel_art, activebackground="#E0E0E0")
image_button.place(x=20, y=100)
video_button = Button(window, text="video_button", command=video_pixel_art, activebackground="#E0E0E0")
video_button.place(x=20, y=140)
webcam_button = Button(window, text="webcam_button", command=webcam_pixel_art, activebackground="#E0E0E0")
webcam_button.place(x=20, y=180)

# Starting an infinite loop
window.mainloop()
