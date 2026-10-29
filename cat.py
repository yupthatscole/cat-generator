import io
import tkinter as tk
from PIL import Image, ImageTk
import pygame
import requests
import threading

pygame.mixer.init()

root = tk.Tk()
root.title("meowwww")
root.geometry("550x700")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

click_count = 0

def get_cat_and_meow():
    global click_count

    click_count += 1
    counter_label.configure(text=f"meowed: {click_count}")

    try:
        pygame.mixer.music.load("meow.mp3")
        pygame.mixer.music.play()
    except Exception:
        root.bell()

    status_label.config(text="summoning kitty...", fg="black")

    threading.Thread(target=fetch_cat, daemon=True).start()


def fetch_cat():
    try:
        response = requests.get(
            "https://api.thecatapi.com/v1/images/search",
            timeout=10
        )
        response.raise_for_status()

        image_url = response.json()[0]["url"]

        img_response = requests.get(image_url, timeout=10)
        img_response.raise_for_status()

        img_bytes = io.BytesIO(img_response.content)

        pil_image = Image.open(img_bytes)
        pil_image = pil_image.convert("RGB")
        pil_image = pil_image.resize(
            (500, 500),
            Image.Resampling.LANCZOS
        )

        root.after(0, lambda: display_cat(pil_image))

    except requests.RequestException:
        root.after(0, lambda: status_label.config(
            text="sorry could nyat fetch kitty",
            fg="red"
        ))

    except Exception:
        root.after(0, lambda: status_label.config(
            text="check ur connection dumbass",
            fg="red"
        ))


def display_cat(pil_image):
    tk_image = ImageTk.PhotoImage(pil_image)

    image_display.config(image=tk_image, text="")
    image_display.image = tk_image

    status_label.config(text="meow loaded cat", fg="black")

counter_label = tk.Label(
    root,
    text="meowed: 0",
    font=("Arial", 16, "bold"),
    bg="#f0f0f0"
)
counter_label.pack(pady=10)

image_frame = tk.Frame(root, width=500, height=500, bg="#e0e0e0")
image_frame.pack(pady=5)
image_frame.pack_propagate(False)

image_display = tk.Label(
    image_frame,
    text="[ click button or else ]",
    bg="#e0e0e0",
    font=("Arial", 14)
)
image_display.pack(expand=True, fill="both")

status_label = tk.Label(root, text="", font=("Arial", 10, "italic"), bg="#f0f0f0")
status_label.pack(pady=2)

action_button = tk.Button(
    root,
    text="click NOW",
    command=get_cat_and_meow,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=15,
    pady=8
)
action_button.pack(pady=10)

root.mainloop()