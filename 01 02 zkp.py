import tkinter as tk               #creates GUI elements (windows, buttons, labels, text boxes).
import hashlib, random             #computes cryptographic hashes for commitments.
from PIL import Image         #PIL.Image: opens and edits images, including for animations.
import matplotlib                   #Used for creating, visualizing, and animating images or data plots in a dynamic and interactive way.
matplotlib.use("TkAgg")                  #Makes Matplotlib plots work inside a Tkinter GUI.
import matplotlib.pyplot as plt           #creates figures and axes to draw on.
import matplotlib.animation as animation #used to create dynamic, animated visualizations by updating plots or images over time.
from matplotlib.patches import FancyBboxPatch   #draws a rounded rectangle box around images.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg       #embeds matplotlib figure inside Tkinter window.
import random              #generates random numbers or choices for challenges or fallback commitments.

# -------- GLOBALS -------- #
#These variables are global so multiple functions can access and modify them.

secret, commit, challenge = "", "", None

# -------- LOG -------- #
def log(msg):
    text_log.insert(tk.END, msg + "\n")
    text_log.see(tk.END)
#Adds a message msg to the log window (Text widget).
#tk.END → appends at the end of the text.
#see(tk.END) → auto-scrolls to the latest message.

# -------- ZKP FUNCTIONS -------- #
def generate_commitment():
    global secret, commit
    secret = entry_secret.get()    #                           Reads secret from input field (entry_secret).
    if not secret or len(secret) < 4 or not secret.isalnum():  #Checks if secret is valid (≥4 characters and alphanumeric).
        commit = hashlib.sha256(str(random.random()).encode()).hexdigest() #If invalid, generates a random hash as fallback commitment.
        label_commitment.config(text=commit)             # Updates the commitment label in GUI (label_commitment).
        label_result.config(text="---", fg="black")
        log("Commitment generated:")
        return
    commit = hashlib.sha256(secret.encode()).hexdigest()
    label_commitment.config(text=commit)
    label_result.config(text="---", fg="black")
    log("Commitment generated:")                        #Logs that a commitment was generated.

def send_challenge():
    global challenge
    if not commit:                #Verifier cannot send challenge if commitment is missing.
        label_result.config(text="✖ Rejected", fg="red")
        log("Challenge cannot be sent: No commitment.")
        return
    challenge = random.choice([0, 1])           #Randomly selects 0 or 1 as the challenge.
    label_challenge.config(text=str(challenge))  #Updates GUI to show the challenge.
    log(f"Verifier sends challenge: {challenge}")  #Logs the action.
 
def verify_commitment():
    if not commit or challenge is None:              #Checks if commitment or challenge is missing → rejects verification.
        label_result.config(text="✖ Rejected", fg="red")
        log("Verification failed: Missing commitment or challenge.")
        return
    
    #Recomputes hash of secret → compares with commitment.
    #Updates GUI and log with result: either accepted (honest) or rejected (dishonest).

    if secret and hashlib.sha256(secret.encode()).hexdigest() == commit:   
        label_result.config(text="✔ Accepted (Prover Honest)", fg="green")      
        log("Verification successful: Prover is honest.")
    else:
        label_result.config(text="✖ Rejected (Prover Dishonest)", fg="red")
        log("Verification failed: Prover is dishonest.")

def reset_all():
    global secret, commit, challenge
    secret = commit = challenge = ""
    entry_secret.delete(0, tk.END)
    label_commitment.config(text="---")
    label_challenge.config(text="---")
    label_result.config(text="---", fg="black")
    text_log.delete(1.0, tk.END)
"""
Resets all variables and clears GUI fields.
Clears the log.
Prepares the program for a new session."""

# ---------------- ANIMATION ---------------- #
# Replace paths with your own images
IMG_PATHS = [
    r"C:\Users\umaid\Downloads\https___dev-to-uploads.s3.amazonaws.com_uploads_articles_vtxos2ke2a99ncosd773.webp",
    r"C:\Users\umaid\Downloads\file_Jo4xevii_Mp_KNF_2_Fx_UMNU_1b_b1e0a8579f.webp",
    r"C:\Users\umaid\Downloads\images.jfif"
]

# Load images safely
IMAGES = []
for p in IMG_PATHS:
    try:
        IMAGES.append(Image.open(p))
    except:
        IMAGES.append(Image.new("RGB", (100, 100), "gray"))

W, H, Y, speed = 0.6, 0.55, 0.5-0.55/2, 0.005
#west, Height, [Y]cordinate and speed
x_pos = [0.5-W/2, 0.5-W/2+W+0.05, 0.5-W/2+2*(W+0.05)]
#X-cordinates [0.5 - W/2]Middle of screen,[0.5 - W/2 + W + 0.05]Right first, Right of the second[0.5 - W/2 + 2*(W + 0.05)].

fig, ax = plt.subplots(figsize=(9, 2))
ax.axis("off") 
#To create a custom drawing area (wide and short) without any axes, labels, or gridlines, so you can display clean graphics or animations.

def draw(px, img):   #To draw a rounded box and an image at a specific position.
    ax.add_patch(FancyBboxPatch((px,Y), W,H, boxstyle="round,pad=0.02,rounding_size=0.04",
    edgecolor="black", facecolor="none", transform=ax.transAxes))   
     #This code **draws a transparent, rounded rectangle with a black border at a specific position on the plot**, using axis-based coordinates so it stays in the same place on the figure.
    ax.imshow(img, extent=(px,px+W,Y,Y+H), transform=ax.transAxes) #Places the image inside the rounded rectangle at the given position.

def animate(frame):        #Defines a function called animate that updates the animation for each frame.
    ax.clear()             #Clears everything previously drawn on the axes so the new frame can be drawn.
    ax.axis("off")         #Hides the axes to keep the animation clean with no lines or labels.
    for i in range(3):     #Loops through three objects (or images) to update each one.
        x_pos[i] -= speed  #Loops through three objects (or images) to update each one.
        if x_pos[i] < -W-0.05:  #Checks if the object has moved completely off the left side of the screen.
            x_pos[i] = max(x_pos) + W + 0.05 #Moves the object to the right side after it exits the screen, creating a looping effect.
        draw(x_pos[i], IMAGES[i])   #Draws the image at its updated x-position.
    canvas.draw()  #Redraws the canvas so the updated animation appears in the Tkinter window.

# -------- GUI -------- #
root = tk.Tk()          #Creates the main Tkinter window (the root window of the application).
root.title("ZKP (Zero-Knowledge Proof)")  #Sets the title text shown at the top of the window.
root.geometry("820x700")    #Defines the window size as 820 pixels wide and 700 pixels tall.
root.resizable(False, False)  #Prevents the window from being resized horizontally or vertically.

tk.Label(root, text="Zero-Knowledge Proof **CRYPTOGRAPHY** ", font=("Arial",18,"bold")).pack(pady=10,)

# Animation Canvas
canvas_frame = tk.Frame(root)
canvas_frame.pack(pady=5, fill="both", expand=True)
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)
"""
It creates a title at the top of the window and then places a Matplotlib animation
inside a Tkinter window so the animation can be displayed and resized properly within the application."""

# Start animation It runs the animation by updating the figure every 30 milliseconds.
ani = animation.FuncAnimation(fig, animate, interval=30, blit=False)

# Input Frame
frame = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10, bg="#60A6C8") #frame inside the main window with a border, padding, and a gray background color.
frame.pack(fill="x", padx=20, pady=10)
#Places the frame in the window, makes it stretch horizontally, and adds space around it.

tk.Label(frame, text="Prover Secret:", bg="#2E9D9D").grid(row=0,column=0,sticky="w", pady=2)
entry_secret = tk.Entry(frame, show="*", width=40) #Creates an entry box where the user types the secret, hiding the characters with
entry_secret.grid(row=0,column=1,pady=2)    #Places the entry box next to the label in row 0, column 1 with some spacing.

#label is a widget used to display text or images in a window.

tk.Label(frame, text="Commitment:", bg="#2E9D9D").grid(row=1,column=0,sticky="w", pady=2)
label_commitment = tk.Label(frame, text="---", width=50, bg="white", relief="sunken", anchor="w")
label_commitment.grid(row=1,column=1,pady=2)

tk.Label(frame, text="Verifier Challenge:", bg="#2E9D9D").grid(row=2,column=0,sticky="w", pady=2)
label_challenge = tk.Label(frame, text="---", width=50, bg="white", relief="sunken", anchor="w")
label_challenge.grid(row=2,column=1,pady=2)
 
# Buttons
#All four buttons are placed in a single row inside a frame, with a little space between them, and each button runs its own function when clicked.

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)      #Adds vertical space above and below the frame for separation.
tk.Button(btn_frame, text="Generate Commitment", command=generate_commitment, width=20).grid(row=0,column=0,padx=5)
#Places the button in the first row, first column of the frame, with 5 pixels of horizontal spacing (padx=5).

tk.Button(btn_frame, text="Send Challenge", command=send_challenge, width=20).grid(row=0,column=1,padx=5) # button that sends a challenge to the verifier in the ZKP process.
tk.Button(btn_frame, text="Verify", command=verify_commitment, width=20).grid(row=0,column=2,padx=5)  # A button that checks if the commitment and challenge are correct.
tk.Button(btn_frame, text="Reset", command=reset_all, width=10).grid(row=0,column=3,padx=5)        #  A button that clears all inputs and outputs to start fresh.

# Result & Log
label_result = tk.Label(root, text="---", font=("Arial",14,"bold"))   # Creates a label to display results or messages in the window.
label_result.pack(pady=10)   #Places the label in the window. pady=10 → Adds vertical space above and below the label.

tk.Label(root, text="Processing Log (Verifier View):").pack() 
# creates a label that displays the text “Processing Log (Verifier View):” at the top of the log section in the window.

text_log = tk.Text(root, height=10, width=100, bg="#6fbfd7")
# This line creates a multi-line text box 10 lines tall and 100 characters wide with a light gray background, where you can display or write text.

text_log.pack(pady=5)
#This line places the text box in the window and adds a small vertical space of 5 pixels above and below it.

root.mainloop()
#This line **starts the Tkinter program** and keeps the window open, waiting for user actions like clicks or typing.

