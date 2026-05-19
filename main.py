import tkinter as tk
from tkinter import messagebox
import random
import math

# ---------------- WINDOW ---------------- #
root = tk.Tk()
root.title("🎲 Immersive Random Number Generator")
root.geometry("700x500")
root.config(bg="#0f172a")

# ---------------- VARIABLES ---------------- #
generated_numbers = set()

# ---------------- ANIMATED BACKGROUND ---------------- #
canvas = tk.Canvas(root, bg="#0f172a", highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

particles = []

for _ in range(40):
    x = random.randint(0, 700)
    y = random.randint(0, 500)
    size = random.randint(2, 5)
    speed = random.uniform(0.5, 2)

    particle = {
        "id": canvas.create_oval(
            x, y, x + size, y + size,
            fill="#38bdf8",
            outline=""
        ),
        "x": x,
        "y": y,
        "size": size,
        "speed": speed
    }

    particles.append(particle)

def animate_particles():
    for p in particles:
        p["y"] += p["speed"]

        if p["y"] > 520:
            p["y"] = -10
            p["x"] = random.randint(0, 700)

        canvas.coords(
            p["id"],
            p["x"],
            p["y"],
            p["x"] + p["size"],
            p["y"] + p["size"]
        )

    root.after(30, animate_particles)

animate_particles()

# ---------------- MAIN FRAME ---------------- #
main_frame = tk.Frame(root, bg="#1e293b", bd=0)
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=380)

# Glow effect
glow = tk.Label(
    root,
    bg="#38bdf8"
)
glow.place(relx=0.5, rely=0.5, anchor="center", width=460, height=390)
main_frame.lift()

# ---------------- TITLE ---------------- #
title = tk.Label(
    main_frame,
    text="🎲 RANDOM NUMBER GENERATOR",
    font=("Orbitron", 18, "bold"),
    fg="#38bdf8",
    bg="#1e293b"
)
title.pack(pady=20)

# ---------------- INPUT FIELDS ---------------- #
def styled_entry(parent):
    entry = tk.Entry(
        parent,
        font=("Consolas", 14),
        bg="#0f172a",
        fg="white",
        insertbackground="white",
        relief="flat",
        justify="center"
    )
    return entry

tk.Label(
    main_frame,
    text="Start Number",
    font=("Arial", 12),
    fg="white",
    bg="#1e293b"
).pack()

entry_start = styled_entry(main_frame)
entry_start.pack(pady=5, ipady=5)

tk.Label(
    main_frame,
    text="End Number",
    font=("Arial", 12),
    fg="white",
    bg="#1e293b"
).pack()

entry_end = styled_entry(main_frame)
entry_end.pack(pady=5, ipady=5)

# ---------------- CHECKBOX ---------------- #
repeat_var = tk.BooleanVar()

repeat_box = tk.Checkbutton(
    main_frame,
    text="Allow Repetition",
    variable=repeat_var,
    bg="#1e293b",
    fg="#38bdf8",
    activebackground="#1e293b",
    activeforeground="#38bdf8",
    selectcolor="#0f172a",
    font=("Arial", 11, "bold")
)

repeat_box.pack(pady=10)

# ---------------- RESULT LABEL ---------------- #
result_label = tk.Label(
    main_frame,
    text="✨ Waiting...",
    font=("Orbitron", 24, "bold"),
    fg="#facc15",
    bg="#1e293b"
)

result_label.pack(pady=20)

# ---------------- GENERATION ANIMATION ---------------- #
def rolling_animation(final_number):
    count = 0

    def animate():
        nonlocal count

        fake_num = random.randint(0, 999)
        result_label.config(text=str(fake_num))

        count += 1

        if count < 20:
            root.after(60, animate)
        else:
            result_label.config(text=f"🎉 {final_number}")

    animate()

# ---------------- GENERATE FUNCTION ---------------- #
def generate_number():
    try:
        start = int(entry_start.get())
        end = int(entry_end.get())

        if start > end:
            messagebox.showerror(
                "Invalid Range",
                "Start number must be less than End number."
            )
            return

        allow_repeat = repeat_var.get()

        if not allow_repeat:
            total_possible = end - start + 1

            if len(generated_numbers) >= total_possible:
                messagebox.showinfo(
                    "Completed",
                    "All unique numbers have been generated!"
                )
                return

            while True:
                num = random.randint(start, end)

                if num not in generated_numbers:
                    generated_numbers.add(num)
                    break
        else:
            num = random.randint(start, end)

        rolling_animation(num)

        root.after(
            1500,
            lambda: ask_more()
        )

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid integers."
        )

# ---------------- ASK MORE ---------------- #
def ask_more():
    more = messagebox.askyesno(
        "Generate Again?",
        "Do you want another random number?"
    )

    if not more:
        root.destroy()

# ---------------- BUTTON HOVER EFFECT ---------------- #
def on_enter(e):
    generate_btn.config(bg="#0ea5e9")

def on_leave(e):
    generate_btn.config(bg="#38bdf8")

# ---------------- GENERATE BUTTON ---------------- #
generate_btn = tk.Button(
    main_frame,
    text="⚡ GENERATE",
    command=generate_number,
    font=("Arial", 14, "bold"),
    bg="#38bdf8",
    fg="black",
    activebackground="#0ea5e9",
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=10
)

generate_btn.pack(pady=10)

generate_btn.bind("<Enter>", on_enter)
generate_btn.bind("<Leave>", on_leave)

# ---------------- FOOTER ---------------- #
footer = tk.Label(
    main_frame,
    text="Created with Tkinter ✨",
    font=("Arial", 9),
    fg="gray",
    bg="#1e293b"
)

footer.pack(side="bottom", pady=10)

# ---------------- RUN ---------------- #
root.mainloop()
