import tkinter as tk
from tkinter import Canvas, Button, OptionMenu, StringVar
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def cartesian_to_spherical(x, y, width, height):
    """Converts 2D Cartesian canvas coordinates to spherical coordinates on a unit sphere."""
    r = 1  # Unit sphere
    theta = np.pi * (1 - y / height)  # Map y to polar angle (0 to pi)
    phi = 2 * np.pi * (x / width)  # Map x to azimuthal angle (0 to 2*pi)
    return r, theta, phi

def update_spherical_plot():
    """Updates the spherical plot in real-time as the user draws."""
    if not points:
        return

    # Get canvas dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Convert points to spherical coordinates
    spherical_points = [cartesian_to_spherical(x, y, canvas_width, canvas_height) for x, y in points]

    # Separate r, theta, phi
    r, theta, phi = zip(*spherical_points)

    # Convert spherical to Cartesian for plotting on a sphere
    x_sphere = [r[i] * np.sin(theta[i]) * np.cos(phi[i]) for i in range(len(r))]
    y_sphere = [r[i] * np.sin(theta[i]) * np.sin(phi[i]) for i in range(len(r))]
    z_sphere = [r[i] * np.cos(theta[i]) for i in range(len(r))]

    # Clear and update the spherical plot
    ax.clear()
    ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color='lightgray', alpha=0.5)
    ax.scatter(x_sphere, y_sphere, z_sphere, color='blue')
    ax.set_title("Shape on Spherical Surface")
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
    fig.canvas.draw()

def start_draw(event):
    """Handles the start of drawing on the canvas."""
    global drawing
    drawing = True
    points.clear()
    update_spherical_plot()

def draw(event):
    """Handles drawing on the canvas."""
    if drawing:
        x, y = event.x, event.y
        points.append((x, y))
        canvas.create_oval(x, y, x+1, y+1, fill='black')
        update_spherical_plot()

def stop_draw(event):
    """Handles the end of drawing on the canvas."""
    global drawing
    drawing = False

def clear_canvas():
    """Clears the canvas and the spherical plot."""
    global points
    points.clear()
    canvas.delete("all")
    ax.clear()
    ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color='lightgray', alpha=0.5)
    ax.set_title("Shape on Spherical Surface")
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
    fig.canvas.draw()

# Shape Functions
def draw_square():
    """Draw a square on the canvas."""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    points.clear()
    size = min(width, height) // 4
    square_points = [
        (width // 2 - size, height // 2 - size),
        (width // 2 + size, height // 2 - size),
        (width // 2 + size, height // 2 + size),
        (width // 2 - size, height // 2 + size),
        (width // 2 - size, height // 2 - size)
    ]
    for point in square_points:
        points.append(point)
    update_spherical_plot()

def draw_rectangle():
    """Draw a rectangle on the canvas."""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    points.clear()
    size_x = min(width, height) // 3
    size_y = min(width, height) // 2
    rectangle_points = [
        (width // 2 - size_x, height // 2 - size_y),
        (width // 2 + size_x, height // 2 - size_y),
        (width // 2 + size_x, height // 2 + size_y),
        (width // 2 - size_x, height // 2 + size_y),
        (width // 2 - size_x, height // 2 - size_y)
    ]
    for point in rectangle_points:
        points.append(point)
    update_spherical_plot()

def draw_circle():
    """Draw a circle on the canvas."""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    points.clear()
    radius = min(width, height) // 4
    for angle in np.linspace(0, 2*np.pi, 100):
        x = width // 2 + radius * np.cos(angle)
        y = height // 2 + radius * np.sin(angle)
        points.append((x, y))
    update_spherical_plot()

def draw_ellipse():
    """Draw an ellipse on the canvas."""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    points.clear()
    a = min(width, height) // 3  # semi-major axis
    b = min(width, height) // 6  # semi-minor axis
    for angle in np.linspace(0, 2*np.pi, 100):
        x = width // 2 + a * np.cos(angle)
        y = height // 2 + b * np.sin(angle)
        points.append((x, y))
    update_spherical_plot()

def draw_line():
    """Draw a line on the canvas."""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    points.clear()
    x1, y1 = width // 4, height // 4
    x2, y2 = 3 * width // 4, 3 * height // 4
    points.append((x1, y1))
    points.append((x2, y2))
    update_spherical_plot()

# Initialize Tkinter window
root = tk.Tk()
root.title("Draw Shape and Visualize on Spherical Surface")

# Canvas for drawing
canvas = Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Shape selector
shape_var = StringVar()
shape_var.set("Line")  # default value

shape_menu = OptionMenu(root, shape_var, "Line", "Square", "Rectangle", "Circle", "Ellipse")
shape_menu.pack()

# Draw button
draw_button = Button(root, text="Draw Shape", command=lambda: globals()[f"draw_{shape_var.get().lower()}"]())
draw_button.pack()

# Clear button
clear_button = Button(root, text="Clear", command=clear_canvas)
clear_button.pack()

# Initialize variables
drawing = False
points = []

# Set up the Matplotlib figure for spherical plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.ion()  # Turn on interactive mode

# Create a sphere for reference
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
sphere_x = np.outer(np.cos(u), np.sin(v))
sphere_y = np.outer(np.sin(u), np.sin(v))
sphere_z = np.outer(np.ones_like(u), np.cos(v))
ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color='lightgray', alpha=0.5)
fig.show()

# Bind mouse events for drawing
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

# Run the Tkinter main loop
root.mainloop()
