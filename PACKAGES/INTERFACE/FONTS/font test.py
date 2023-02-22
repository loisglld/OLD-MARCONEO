#coding:utf-8
import tkinter as tk
import pyglet

pyglet.font.add_file("C:/Users/galla/Desktop/MARCO_LOIS/PACKAGES/INTERFACE/FONTS/MAKISUPA.TTF")
fontTitle = ("Batrider-Textured", 200)
fontText = ("MAKISUPA", 50)
  
root = tk.Tk()
root.state('zoomed')
sample_text = tk.Text(root, width=root.winfo_screenwidth(),
                      height = root.winfo_screenheight(), bg = "black")
sample_text.pack()
  
Font_tuple = ("MAKISUPA", 80)
  
sample_text.configure(font = Font_tuple, fg='white')
root.mainloop()