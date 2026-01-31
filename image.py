import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼 Modern Image Viewer")
        self.root.geometry("1000x600")
        self.root.configure(bg="#2c3e50")

        self.image_list = []
        self.current_image = 0
        self.zoom_level = 1.0
        self.slideshow_active = False
        self.fullscreen = False

        try:
            self.resample_method = Image.Resampling.LANCZOS
        except AttributeError:
            self.resample_method = Image.ANTIALIAS

        self.label = tk.Label(root, bg="#2c3e50")
        self.label.pack(expand=True)

        btn_frame = tk.Frame(root, bg="#34495e")
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Open Folder", command=self.load_folder).pack(side="left")
        tk.Button(btn_frame, text="<< Prev", command=self.prev_image).pack(side="left")
        tk.Button(btn_frame, text="Next >>", command=self.next_image).pack(side="left")
        tk.Button(btn_frame, text="Zoom +", command=self.zoom_in).pack(side="left")
        tk.Button(btn_frame, text="Zoom -", command=self.zoom_out).pack(side="left")

    def load_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.image_list = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]

        if not self.image_list:
            messagebox.showerror("Error", "No images found!")
            return

        self.current_image = 0
        self.show_image()

    def show_image(self):
        img = Image.open(self.image_list[self.current_image])

        w, h = img.size
        img = img.resize(
            (int(w * self.zoom_level), int(h * self.zoom_level)),
            self.resample_method
        )

        self.tk_img = ImageTk.PhotoImage(img)
        self.label.config(image=self.tk_img)

    def next_image(self):
        if self.image_list:
            self.current_image = (self.current_image + 1) % len(self.image_list)
            self.show_image()

    def prev_image(self):
        if self.image_list:
            self.current_image = (self.current_image - 1) % len(self.image_list)
            self.show_image()

    def zoom_in(self):
        self.zoom_level += 0.1
        self.show_image()

    def zoom_out(self):
        self.zoom_level -= 0.1
        self.show_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
