import tkinter as tk
from tkinter import Canvas, Button, OptionMenu, StringVar
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def cartesian_to_cylindrical(x, y, width, height, radius=1):
    """Converts 2D Cartesian canvas coordinates to cylindrical coordinates."""
    # Map the 2D point (x, y) to cylindrical coordinates
    theta = np.arctan2(y - height // 2, x - width // 2)  # Azimuthal angle
    z = (y - height // 2) / (height // 2)  # Scale z from the canvas height
    return radius, theta, z

def update_cylindrical_plot():
    """Updates the cylindrical plot in real-time as the user draws."""
    if not points:
        return

    # Get canvas dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Convert points to cylindrical coordinates
    cylindrical_points = [cartesian_to_cylindrical(x, y, canvas_width, canvas_height) for x, y in points]

    # Separate r, theta, z
    r, theta, z = zip(*cylindrical_points)

    # Convert cylindrical to Cartesian for plotting on the cylinder
    x_cyl = [r[i] * np.cos(theta[i]) for i in range(len(r))]
    y_cyl = [r[i] * np.sin(theta[i]) for i in range(len(r))]
    z_cyl = z  # Use z values directly

    # Clear and update the cylindrical plot
    ax.clear()
    ax.plot_wireframe(cylinder_x, cylinder_y, cylinder_z, color='lightgray', alpha=0.5)
    ax.scatter(x_cyl, y_cyl, z_cyl, color='blue')
    ax.set_title("Shape on Cylindrical Surface")
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
    fig.canvas.draw()

def start_draw(event):
    """Handles the start of drawing on the canvas."""
    global drawing
    drawing = True
    points.clear()
    update_cylindrical_plot()

def draw(event):
    """Handles drawing on the canvas."""
    if drawing:
        x, y = event.x, event.y
        points.append((x, y))
        canvas.create_oval(x, y, x+1, y+1, fill='black')
        update_cylindrical_plot()

def stop_draw(event):
    """Handles the end of drawing on the canvas."""
    global drawing
    drawing = False

def clear_canvas():
    """Clears the canvas and the cylindrical plot."""
    global points
    points.clear()
    canvas.delete("all")
    ax.clear()
    ax.plot_wireframe(cylinder_x, cylinder_y, cylinder_z, color='lightgray', alpha=0.5)
    ax.set_title("Shape on Cylindrical Surface")
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
    update_cylindrical_plot()

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
    update_cylindrical_plot()

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
    update_cylindrical_plot()

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
    update_cylindrical_plot()

def draw_line():
    """Draw a line on the canvas."""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    points.clear()
    x1, y1 = width // 4, height // 4
    x2, y2 = 3 * width // 4, 3 * height // 4
    points.append((x1, y1))
    points.append((x2, y2))
    update_cylindrical_plot()

# Initialize Tkinter window
root = tk.Tk()
root.title("Draw Shape and Visualize on Cylindrical Surface")

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

# Set up the Matplotlib figure for cylindrical plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.ion()  # Turn on interactive mode

# Create a cylinder for reference
z_cylinder = np.linspace(-1, 1, 100)
theta_cylinder = np.linspace(0, 2 * np.pi, 100)
Z, Theta = np.meshgrid(z_cylinder, theta_cylinder)
X_cylinder = np.cos(Theta)
Y_cylinder = np.sin(Theta)
cylinder_x = X_cylinder  # Define X values for cylinder
cylinder_y = Y_cylinder  # Define Y values for cylinder
cylinder_z = Z          # Define Z values for cylinder

ax.plot_wireframe(cylinder_x, cylinder_y, cylinder_z, color='lightgray', alpha=0.5)
fig.show()

# Bind mouse events for drawing
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

# Run the Tkinter main loop
root.mainloop()
