import tkinter as tk
import subprocess
import sys
import os

BG = "#111827"
CARD = "#1f2937"
TEXT = "#ffffff"
MUTED = "#9ca3af"
GREEN = "#00ff66"
RED = "#ff4444"
BLUE = "#3b82f6"

root = tk.Tk()
root.title("Mac Face Unlock")
root.geometry("500x600")
root.configure(bg=BG)
root.resizable(False, False)

# Header
tk.Label(
    root,
    text="🔐 Mac Face Unlock",
    font=("Helvetica", 26, "bold"),
    fg=TEXT,
    bg=BG
).pack(pady=(45, 10))

tk.Label(
    root,
    text="Local authentication prototype",
    font=("Helvetica", 11),
    fg=MUTED,
    bg=BG
).pack()

# Card
card = tk.Frame(
    root,
    bg=CARD,
    width=400,
    height=250
)
card.pack(pady=35)
card.pack_propagate(False)

status = tk.Label(
    card,
    text="Ready to verify",
    font=("Helvetica", 20, "bold"),
    fg=TEXT,
    bg=CARD
)
status.pack(pady=(55, 15))

instruction = tk.Label(
    card,
    text="Click below to start face verification.",
    font=("Helvetica", 11),
    fg=MUTED,
    bg=CARD
)
instruction.pack()

# Button
button = tk.Button(
    root,
    text="START VERIFICATION",
    font=("Helvetica", 13, "bold"),
    fg=TEXT,
    bg=BLUE,
    activebackground=BLUE,
    activeforeground=TEXT,
    relief="flat",
    cursor="hand2",
    padx=30,
    pady=15
)
button.pack(pady=10)


def check_result(process):
    """Check the face recognition process without freezing the GUI."""

    if process.poll() is None:
        root.after(100, lambda: check_result(process))
        return

    try:
        output = process.stdout.read()
    except Exception:
        output = ""

    button.config(
        state="normal",
        text="START VERIFICATION"
    )

    if "VERIFIED - ACCESS GRANTED" in output:
        status.config(
            text="✓ VERIFIED",
            fg=GREEN
        )

        instruction.config(
            text="ACCESS GRANTED",
            fg=GREEN
        )

    elif "CAMERA_ERROR" in output:
        status.config(
            text="CAMERA ERROR",
            fg=RED
        )

        instruction.config(
            text="Could not access the camera.",
            fg=RED
        )

    else:
        status.config(
            text="NOT VERIFIED",
            fg=RED
        )

        instruction.config(
            text="Face was not recognized.",
            fg=RED
        )


def verify():
    button.config(
        state="disabled",
        text="VERIFYING..."
    )

    status.config(
        text="Starting camera...",
        fg=TEXT
    )

    instruction.config(
        text="Look at the camera.",
        fg=MUTED
    )

    root.update_idletasks()

    script = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "face_unlock_v2.py"
    )

    try:
        process = subprocess.Popen(
            [sys.executable, script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        check_result(process)

    except Exception as e:
        button.config(
            state="normal",
            text="START VERIFICATION"
        )

        status.config(
            text="ERROR",
            fg=RED
        )

        instruction.config(
            text=str(e),
            fg=RED
        )


button.config(command=verify)

# Footer
tk.Label(
    root,
    text="All verification is performed locally.",
    font=("Helvetica", 9),
    fg=MUTED,
    bg=BG
).pack(side="bottom", pady=20)

root.mainloop()
