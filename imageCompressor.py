import numpy as np
from numpy import r_
import PIL.Image
import PIL.ImageTk
import scipy.fft as DCT2_library
import tkinter
from tkinter import filedialog
from tkinter.messagebox import showinfo
import os

# Global variables
img_directory = ""
output_directory = ""
output_name = "result"
HEIGHT, WIDTH = 600, 600
colors = {'blue': '#212a49', 'white': 'white', 'violet': '#646e9f', 'green': '#21e7b6', 'green2': '#2c7270'}
font = 'Sans-Serif'

def select_image():
    global img_directory

    img_path = filedialog.askopenfilename( title='Please select a picture', initialdir=os.getcwd(), filetypes=[('Image File', ['.bmp'])])
    if (len(img_path) > 0) and os.path.isfile(img_path):
        img_directory = img_path
        lbl_img_directory.config(text=img_directory)

def select_output_directory():
    global output_directory
    
    output_directory_path = filedialog.askdirectory()
    if (len(output_directory_path) > 0) and os.path.isdir(output_directory_path):
        output_directory = output_directory_path + "/"
        lbl_output_directory.config(text=output_directory)

def display_output(img_original, img_compressed):    
    x = window.winfo_x() / (1.5)
    y = window.winfo_y()
    WIDTH = window.winfo_width()
    if(WIDTH < 900):
        WIDTH = window.winfo_width() * 2
    HEIGHT = window.winfo_height()
    img_w, img_h = 420, 420

    window_display_output = tkinter.Toplevel(window)
    window_display_output.title('Original vs. Compressed')
    window_display_output.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, x, y))
    window_display_output.minsize(WIDTH, HEIGHT)
    
    # GUI: Left frame
    left_frame = tkinter.Frame(window_display_output, bg=colors['blue'])
    left_frame.place(relx=0.25, rely=0, relwidth=0.5, relheight=1, anchor='n')

    lbl_OriginalImage = tkinter.Label(left_frame, text='Original image', font=(font, 18), fg=colors['white'], bg=colors['blue'])
    lbl_OriginalImage.place(relx=0.5, rely=0, relwidth=0.6, relheight=0.2, anchor='n')

    # GUI: Left frame image
    image_frame_left = tkinter.Frame(left_frame, bg=colors['violet']) 
    image_frame_left.place(relx=0.5, rely=0.20, width=img_w+10, height=img_h+10, anchor='n')
    
    resized_image = img_original.resize((img_w, img_h), PIL.Image.ANTIALIAS)
    pi_img_original = PIL.ImageTk.PhotoImage(image=resized_image)
    
    lbl_img_original = tkinter.Label(image_frame_left, image=pi_img_original)
    lbl_img_original.place(relwidth=1,relheight=1)
    
    # GUI: Right frame
    right_frame = tkinter.Frame(window_display_output, bg=colors['green2'])
    right_frame.place(relx=0.75, rely=0, relwidth=0.5, relheight=1, anchor='n')

    lbl_OriginalImage = tkinter.Label(right_frame, text='Compressed image', font=(font, 18), fg= colors['white'], bg=colors['green2'])
    lbl_OriginalImage.place(relx=0.5, rely=0, relwidth=0.6, relheight=0.2, anchor='n')

    # GUI: Right frame image
    image_frame_right = tkinter.Frame(right_frame, bg=colors['green2']) 
    image_frame_right.place(relx=0.5, rely=0.20, width=img_w+10, height=img_h+10, anchor='n')

    resized_image_right = img_compressed.resize((img_w, img_h), PIL.Image.ANTIALIAS)
    pi_img_compressed = PIL.ImageTk.PhotoImage(image=resized_image_right)

    lbl_img_compressed = tkinter.Label(image_frame_right, image=pi_img_compressed)
    lbl_img_compressed.place(relwidth=1, relheight=1)

    window_display_output.mainloop()

def save_image(img, output_directory, output_name):
    path = output_directory + output_name + '.bmp'
    img.save(path)

def check_parameters(img, output_directory):
    try:
        int(str(value_F.get())) # F must be an integer
        int(str(value_d.get())) # d must be an integer
    except:
        return False

    F = int(value_F.get())
    d = int(value_d.get())

    if(not(img) or img == ""): # img can't be empty
        return False

    if(not(output_directory) or output_directory == ""): #output_directory can't be empty
        return False

    if(F <= 0): # F >= 1
        return False
    
    if(d < 0 or d > ((2 * F) - 2)): # 0 <= d <= 2F-2
        return False

    return True

def image_to_matrix(img):
    img_grey = img.convert('L') # 'L': 8-bit pixels, black and white
    img_matrix = np.array(img_grey)

    return img_matrix

def dct2(sub_img):
    return DCT2_library.dctn(sub_img, 2, norm='ortho')

def idct2(sub_img):
    return DCT2_library.idctn(sub_img, 2, norm='ortho')

def compress(img_matrix, F, d):
    img_sizes = img_matrix.shape
    outcome_matrix = np.zeros(img_sizes)

    # split, dct2, frequencies elimination, idct2, recostruct
    for row in r_[:img_sizes[0]:F]:
        for col in r_[:img_sizes[1]:F]:
            if(((row+F) > img_sizes[0]) or (col+F > img_sizes[1])):
                continue

            sub_img_dct2 = dct2(img_matrix[row:(row+F), col:(col+F)])

            for i in range(0, F):
                for j in range(0, F):
                    if((i+j) >= d):
                        sub_img_dct2[i][j] = 0

            outcome_matrix[row:(row+F), col:(col+F)] = idct2(sub_img_dct2)

    # round, normalize
    outcome_matrix = np.around(outcome_matrix)
    outcome_matrix = outcome_matrix.clip(0, 255)

    return outcome_matrix

def main():
    global img_directory
    global output_directory

    if(check_parameters(img_directory, output_directory) == False):
        showinfo("Error", "Wrong parameters!")
    else:
        F = int(value_F.get())
        d = int(value_d.get())

        img = PIL.Image.open(img_directory)
        img_matrix = image_to_matrix(img)
        img_outcome = compress(img_matrix, F, d)
        img_outcome = PIL.Image.fromarray(img_outcome.astype('uint8'))
        save_image(img_outcome, output_directory, output_name)
        display_output(img, img_outcome)
    
# GUI
window = tkinter.Tk()
window.title("Image Compressor")
window.minsize(WIDTH, HEIGHT)
background = tkinter.Label(window, bg=colors['blue'])
background.place(x=0, y=0, relwidth=1, relheight=1)
window.geometry("+%d+%d" % (window.winfo_screenwidth() / 2 - WIDTH / 2, window.winfo_screenheight() / 2 - HEIGHT / 2))

# GUI: Title
title_frame = tkinter.Frame(window)
title_frame.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1, anchor='n')
lbl_title = tkinter.Label(title_frame, text="IMAGE COMPRESSOR", font=(font, 18), fg=colors['white'], bg=colors['blue'])
lbl_title.place(relwidth=1, relheight=1)

# GUI: Body 
font_size = 12
body_frame = tkinter.Frame(window, bg=colors['blue'])
body_frame.place(relx=0.5, rely=0.20, relwidth=0.75, relheight=0.6, anchor='n')

# GUI: Input  
lbl_select_image_input = tkinter.Label(body_frame, text="Select Image (.bpm only):", font=(font, font_size), fg=colors['white'], bg=colors['blue'])
lbl_select_image_input.place(relx=0.5, rely=0.05, anchor='n')

lbl_img_directory = tkinter.Label(body_frame, text="", font=(font, font_size), fg=colors['white'], bg=colors['violet'])
lbl_img_directory.place(relx=0.45, rely=0.15, relwidth=0.65, relheight=0.09, anchor='n')

btn_select_image_input = tkinter.Button(body_frame, text="...", font=(font, font_size), fg=colors['white'], bg=colors['green2'], highlightbackground=colors['green2'], highlightthickness= 500, command=select_image)
btn_select_image_input.place(relx=0.81, rely=0.15, relwidth=0.08, relheight=0.09, anchor='n')

# GUI: Output
y_offset = 0.25
lbl_select_image_output = tkinter.Label(body_frame, text="Select Image Output:", font=(font, font_size), fg=colors['white'], bg=colors['blue'])
lbl_select_image_output.place(relx=0.5, rely=0.05+y_offset, anchor='n')
    
lbl_output_directory = tkinter.Label(body_frame, text="", font=(font, font_size), fg=colors['white'], bg=colors['violet'])
lbl_output_directory.place(relx=0.45, rely=0.15+y_offset, relwidth=0.65, relheight=0.09, anchor='n')

btn_select_image_output = tkinter.Button(body_frame, text="...", font=(font, font_size), fg=colors['white'], bg=colors['green2'], highlightbackground=colors['green2'], highlightthickness= 500, command=select_output_directory)
btn_select_image_output.place(relx=0.81, rely=0.15+y_offset, relwidth=0.08, relheight=0.09, anchor='n')

# GUI: F/d value 
y_offset = y_offset * 2 - 0.05
lbl_F = tkinter.Label(body_frame, text="F-value (> 0):", font=(font, font_size), fg=colors['white'], bg=colors['blue'])
lbl_F.place(relx=0.30, rely=0.18+y_offset, relwidth=0.30, relheight=0.09, anchor='n') 
value_F = tkinter.Spinbox(body_frame, from_=1, to=100, width=10, font=(font, font_size), fg=colors['white'], bg= colors['green2'])
value_F.place(relx=0.30, rely=0.30+y_offset, relwidth=0.15, relheight=0.09, anchor='n') 

lbl_d = tkinter.Label(body_frame, text="d-value ([0, 2F-2]):", font=(font, font_size), fg=colors['white'], bg=colors['blue'])
lbl_d.place(relx=0.70, rely=0.18+y_offset, relwidth=0.30, relheight=0.09, anchor='n') 
value_d = tkinter.Spinbox(body_frame, from_=0, to=100, width=10, font=(font, font_size), fg=colors['white'], bg= colors['green2'])
value_d.place(relx=0.70, rely=0.30+y_offset, relwidth=0.15, relheight=0.09, anchor='n') 

# GUI: Compress
lower_frame = tkinter.Frame(window)
lower_frame.place(relx=0.5, rely=0.85, relwidth=0.25, relheight=0.1, anchor='n')
btn_compress = tkinter.Button(lower_frame, text="COMPRESS", fg=colors['white'], bg=colors['green'], font=("Sans-Serif", font_size+2), highlightbackground=colors['green'], highlightthickness=500, command=main)
btn_compress.place(relwidth=1, relheight=1)

if __name__ == "__main__":
    window.mainloop()