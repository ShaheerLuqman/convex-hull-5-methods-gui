import tkinter as tk
import timeit


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def doIntersect(p1, q1, p2, q2, method):
    if method == 1:
        return do_intersect_method_1(p1, q1, p2, q2)
    elif method == 2:
        return do_intersect_method_2(p1, q1, p2, q2)
    elif method == 3:
        return do_intersect_method_3(p1, q1, p2, q2)
    else:
        return False


def do_intersect_method_1(p1, q1, p2, q2):
    def orientation(p, q, r):
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if val > 0:
            return 1  # Clockwise orientation
        elif val < 0:
            return 2  # Counterclockwise orientation
        else:
            return 0  # Collinear orientation

    def onSegment(p, q, r):
        return (
            q.x <= max(p.x, r.x)
            and q.x >= min(p.x, r.x)
            and q.y <= max(p.y, r.y)
            and q.y >= min(p.y, r.y)
        )

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2) and (o3 != o4):
        return True
    if (o1 == 0) and onSegment(p1, p2, q1):
        return True
    if (o2 == 0) and onSegment(p1, q2, q1):
        return True
    if (o3 == 0) and onSegment(p2, p1, q2):
        return True
    if (o4 == 0) and onSegment(p2, q1, q2):
        return True

    return False


def do_intersect_method_2(p1, q1, p2, q2):
    # Check if slopes are different (lines are not parallel)
    slope1 = (q1.y - p1.y) / (q1.x - p1.x) if (q1.x - p1.x) != 0 else float("inf")
    slope2 = (q2.y - p2.y) / (q2.x - p2.x) if (q2.x - p2.x) != 0 else float("inf")

    if slope1 != slope2:
        # Check if intersection point is within the range of both line segments
        intersect_x = (p2.y - p1.y + slope1 * p1.x - slope2 * p2.x) / (slope1 - slope2)
        intersect_y = slope1 * (intersect_x - p1.x) + p1.y

        if (
            min(p1.x, q1.x) <= intersect_x <= max(p1.x, q1.x)
            and min(p1.y, q1.y) <= intersect_y <= max(p1.y, q1.y)
            and min(p2.x, q2.x) <= intersect_x <= max(p2.x, q2.x)
            and min(p2.y, q2.y) <= intersect_y <= max(p2.y, q2.y)
        ):
            return True

    return False


def do_intersect_method_3(p1, q1, p2, q2):
    # Parametric representation: p1 + t * (q1 - p1) = p2 + s * (q2 - p2)
    # Solve for t and s using a system of linear equations

    dx1 = q1.x - p1.x
    dy1 = q1.y - p1.y
    dx2 = q2.x - p2.x
    dy2 = q2.y - p2.y

    determinant = (q1.x - p1.x) * (q2.y - p2.y) - (q2.x - p2.x) * (q1.y - p1.y)

    if determinant == 0:
        # The lines are parallel, and intersection is not possible
        return False

    # Solve for t and s
    t = ((p2.x - p1.x) * (q2.y - p2.y) - (p2.y - p1.y) * (q2.x - p2.x)) / determinant
    s = ((p2.x - p1.x) * dy1 - (p2.y - p1.y) * dx1) / determinant

    # Check if the values of t and s are in the range [0, 1]
    if 0 <= t <= 1 and 0 <= s <= 1:
        return True

    return False


class MouseClickCoordinatesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point Intersection")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.clicked_coordinates = []
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.clear_button = tk.Button(
            root, text="Clear Canvas", command=self.clear_canvas
        )
        self.clear_button.pack()

        self.clear_message_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.clear_message_label.pack()

        self.method_var = tk.IntVar(value=1)
        self.last_used_method = 1  # Default to Method 1

        self.time_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.time_label.pack()

        # Horizontal layout for convex hull methods
        self.horizontal_buttons_frame = tk.Frame(root)
        self.horizontal_buttons_frame.pack()

        self.method1_button = tk.Button(
            self.horizontal_buttons_frame,
            text="Orientation Method",
            command=lambda m=1: self.on_method_change(m),
        )
        self.method1_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.method2_button = tk.Button(
            self.horizontal_buttons_frame,
            text="Slope and Intercept Method",
            command=lambda m=2: self.on_method_change(m),
        )
        self.method2_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.method3_button = tk.Button(
            self.horizontal_buttons_frame,
            text="Parametric Method",
            command=lambda m=3: self.on_method_change(m),
        )
        self.method3_button.pack(side=tk.LEFT, padx=20, pady=20)

    def on_canvas_click(self, event):
        if len(self.clicked_coordinates) < 4:
            x, y = event.x, event.y
            self.clicked_coordinates.append(Point(x, y))
            self.update_canvas()

            if len(self.clicked_coordinates) == 4:
                self.measure_time_for_methods()

    def measure_time_for_methods(self):
        method = self.method_var.get()
        self.last_used_method = method  # Update last used method
        if len(self.clicked_coordinates) != 4:
            self.time_label.config(text="")
            return

        p1, q1, p2, q2 = (
            self.clicked_coordinates[0],
            self.clicked_coordinates[1],
            self.clicked_coordinates[2],
            self.clicked_coordinates[3],
        )

        # Measure time for the selected method
        if method == 1:
            elapsed_time = timeit.timeit(
                lambda: doIntersect(p1, q1, p2, q2, 1), number=1000
            )
        elif method == 2:
            elapsed_time = timeit.timeit(
                lambda: doIntersect(p1, q1, p2, q2, 2), number=1000
            )
        elif method == 3:
            elapsed_time = timeit.timeit(
                lambda: doIntersect(p1, q1, p2, q2, 3), number=1000
            )
        else:
            elapsed_time = 0.0

        elapsed_time * 1000
        # Display elapsed time on the GUI
        elapsed_time_text = f"Method {method}: {elapsed_time:.5f} ms"
        self.time_label.config(text=elapsed_time_text)

        if self.do_intersect_lines(method):
            self.display_intersect_message()
        else:
            self.display_no_intersect_message()

    def update_canvas(self):
        self.canvas.delete("all")

        for i in range(len(self.clicked_coordinates) - 1):
            x1, y1 = self.clicked_coordinates[i].x, self.clicked_coordinates[i].y
            x2, y2 = (
                self.clicked_coordinates[i + 1].x,
                self.clicked_coordinates[i + 1].y,
            )

            line_color = "green" if i == 0 else "blue" if i == 2 else None

            if line_color:
                self.canvas.create_line(x1, y1, x2, y2, fill=line_color)

        for point in self.clicked_coordinates:
            x, y = point.x, point.y
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")

    def clear_canvas(self):
        self.clicked_coordinates = []
        self.canvas.delete("all")
        self.clear_message_label.config(text="")
        self.method_var.set(self.last_used_method)  # Set method to last used
        self.on_method_change()

    def do_intersect_lines(self, method):
        p1, q1, p2, q2 = (
            self.clicked_coordinates[0],
            self.clicked_coordinates[1],
            self.clicked_coordinates[2],
            self.clicked_coordinates[3],
        )
        return doIntersect(p1, q1, p2, q2, method)

    def display_intersect_message(self):
        self.clear_message_label.config(
            text="Lines intersect! Click 'Clear Canvas' to continue"
        )

    def display_no_intersect_message(self):
        self.clear_message_label.config(
            text="Lines do not intersect! Click 'Clear Canvas' to continue"
        )

    def on_method_change(self, method=None):
        # Update the method_var to the selected method
        if method is not None:
            self.method_var.set(method)
            self.measure_time_for_methods()
        else:
            # If method is not specified, clear canvas and reset clicked_coordinates
            self.clicked_coordinates = []
            self.canvas.delete("all")
            self.clear_message_label.config(text="")
            self.time_label.config(text="")
            self.clear_button.config(
                text="Clear Canvas"
            )  # Remove method number from clear button


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseClickCoordinatesApp(root)
    root.mainloop()
