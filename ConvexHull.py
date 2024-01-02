import tkinter as tk
import random
import time
import timeit
from functools import cmp_to_key


class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y


def dist_sq(p1, p2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # collinear
    elif val > 0:
        return 1  # clockwise
    else:
        return 2  # counterclockwise


def compare(p0, p1, p2):
    o = orientation(p0, p1, p2)
    if o == 0:
        if dist_sq(p0, p2) >= dist_sq(p0, p1):
            return -1
        else:
            return 1
    else:
        if o == 2:
            return -1
        else:
            return 1


def draw_convex_hull(lines, canvas, color="red"):
    # Clear previous convex hull lines and highlights
    canvas.delete("convex_hull")

    for i in range(len(lines) - 1):
        p1, p2 = lines[i], lines[i + 1]
        canvas.create_line(
            p1.x, p1.y, p2.x, p2.y, fill=color, width=2, tags="convex_hull"
        )

    # Connect first and last points with a line
    p1, p2 = lines[-1], lines[0]
    canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=color, width=2, tags="convex_hull")

    # Highlight points that are part of the convex hull
    for point in lines:
        canvas.create_oval(
            point.x - 2,
            point.y - 2,
            point.x + 2,
            point.y + 2,
            fill=color,
            outline=color,
            tags="convex_hull",
        )


def draw_convex_hull_partial(lines, canvas, delay=10, delete=True, color="red"):
    # Clear previous convex hull lines and highlights
    if delete == True:
        canvas.delete("convex_hull")

    for i in range(len(lines) - 1):
        p1, p2 = lines[i], lines[i + 1]
        canvas.create_line(
            p1.x, p1.y, p2.x, p2.y, fill=color, width=2, tags="convex_hull"
        )

    # Highlight points that are part of the convex hull
    for point in lines:
        canvas.create_oval(
            point.x - 2,
            point.y - 2,
            point.x + 2,
            point.y + 2,
            fill=color,
            outline=color,
            tags="convex_hull",
        )
    canvas.update_idletasks()
    canvas.after(delay)


def display_time(time_text, canvas):
    # Clear canvas before displaying elapsed time
    canvas.delete("time_text")

    # Display elapsed time on the canvas
    canvas.create_text(
        250,
        480,
        text=time_text,
        fill="black",
        font=("Helvetica", 12),
        tags="time_text",
    )


def calculate_det(a, b, c):
    return (a.x * b.y + b.x * c.y + c.x * a.y) - (a.y * b.x + b.y * c.x + c.y * a.x)


def convex_hull_method_1(canvas, points):
    def brute_force():
        if len(points) < 3:
            return
        sorted_points = sorted(points, key=lambda p: (p.x, p.y))
        n = len(sorted_points)
        convex_set = set()

        p0 = min(sorted_points, key=lambda point: (point.y, point.x))

        for i in range(n - 1):
            for j in range(i + 1, n):
                points_left_of_ij = points_right_of_ij = True
                for k in range(n):
                    if k != i and k != j:
                        det_k = calculate_det(
                            sorted_points[i], sorted_points[j], sorted_points[k]
                        )
                        if det_k > 0:
                            points_right_of_ij = False
                        elif det_k < 0:
                            points_left_of_ij = False
                        else:
                            if (
                                sorted_points[k].x < sorted_points[i].x
                                or sorted_points[k].x > sorted_points[j].x
                                or sorted_points[k].y < sorted_points[i].y
                                or sorted_points[k].y > sorted_points[j].y
                            ):
                                points_left_of_ij = points_right_of_ij = False
                                break

                if points_left_of_ij or points_right_of_ij:
                    convex_set.update([sorted_points[i], sorted_points[j]])

        sorted_convex_set = sorted(convex_set, key=lambda p: (p.x, p.y))
        sorted_convex_set = sorted(
            sorted_convex_set, key=cmp_to_key(lambda p1, p2: compare(p0, p1, p2))
        )
        return sorted_convex_set

    def brute_force_drawing():
        if len(points) < 3:
            return
        sorted_points = sorted(points, key=lambda p: (p.x, p.y))
        n = len(sorted_points)
        convex_set = set()

        p0 = min(sorted_points, key=lambda point: (point.y, point.x))

        for i in range(n - 1):
            for j in range(i + 1, n):
                points_left_of_ij = points_right_of_ij = True
                for k in range(n):
                    if k != i and k != j:
                        det_k = calculate_det(
                            sorted_points[i], sorted_points[j], sorted_points[k]
                        )
                        if det_k > 0:
                            points_right_of_ij = False
                        elif det_k < 0:
                            points_left_of_ij = False
                        else:
                            if (
                                sorted_points[k].x < sorted_points[i].x
                                or sorted_points[k].x > sorted_points[j].x
                                or sorted_points[k].y < sorted_points[i].y
                                or sorted_points[k].y > sorted_points[j].y
                            ):
                                points_left_of_ij = points_right_of_ij = False
                                break

                if points_left_of_ij or points_right_of_ij:
                    convex_set.update([sorted_points[i], sorted_points[j]])

        sorted_convex_set = sorted(convex_set, key=lambda p: (p.x, p.y))
        sorted_convex_set = sorted(
            sorted_convex_set, key=cmp_to_key(lambda p1, p2: compare(p0, p1, p2))
        )
        return sorted_convex_set

    start_time = timeit.default_timer()
    hull_points = brute_force()
    end_time = timeit.default_timer()
    elapsed_time = (end_time - start_time) * 1000
    elapsed_time_text = f"Brute Force: {elapsed_time:.2f} ms"

    display_time(elapsed_time_text, canvas)
    draw_convex_hull(hull_points, canvas, "blue")


def convex_hull_method_2(canvas, points):
    def jarvis_march_drawing():
        num_points = len(points)
        if num_points < 3:
            return []

        # Find the bottommost point as the starting point
        start_point = max(points, key=lambda p: (p.y))
        convex_hull_points = []

        current_point = start_point
        while True:
            convex_hull_points.append(current_point)

            draw_convex_hull_partial(convex_hull_points, canvas, 50)

            next_point = None

            # Iterate through the candidate points to find the next point in the convex hull
            for candidate_point in points:
                if candidate_point != current_point:
                    if (
                        next_point is None
                        or orientation(current_point, candidate_point, next_point) == 2
                    ):
                        next_point = candidate_point
                    else:
                        # Draw a temporary line if the orientation is not counterclockwise
                        canvas.create_line(
                            candidate_point.x,
                            candidate_point.y,
                            next_point.x,
                            next_point.y,
                            fill="grey",
                            width=2,
                            tags="convex_hull",
                        )
                        canvas.update_idletasks()
                        canvas.after(1)

            current_point = next_point

            # Check if we have completed a full cycle and reached the starting point
            if current_point == start_point:
                break
            canvas.create_line(
                convex_hull_points[-1].x,
                convex_hull_points[-1].y,
                convex_hull_points[0].x,
                convex_hull_points[0].y,
                fill="red",
                width=2,
                tags="convex_hull",
            )
        canvas.update_idletasks()
        canvas.after(10)

        return convex_hull_points

    def jarvis_march():
        num_points = len(points)
        if num_points < 3:
            return []

        # Find the leftmost point as the starting point
        start_point = min(points, key=lambda p: (p.x, p.y))
        convex_hull_points = []

        current_point = start_point
        while True:
            convex_hull_points.append(current_point)
            next_point = None

            for candidate_point in points:
                if candidate_point != current_point:
                    if (
                        next_point is None
                        or orientation(current_point, candidate_point, next_point) == 2
                    ):
                        next_point = candidate_point

            current_point = next_point
            if current_point == start_point:
                break

        return convex_hull_points

    start_time = timeit.default_timer()
    hull_points = jarvis_march()
    end_time = timeit.default_timer()
    elapsed_time = (end_time - start_time) * 1000
    elapsed_time_text = f"Jarvis March: {elapsed_time:.2f} ms"

    display_time(elapsed_time_text, canvas)
    jarvis_march_drawing()
    draw_convex_hull(hull_points, canvas, "orange")


def convex_hull_method_3(canvas, points):
    def graham_scan_drawing():
        if len(points) < 3:
            return

        p0 = min(points, key=lambda point: (point.y, point.x))
        candidate_points = sorted(
            points, key=cmp_to_key(lambda p1, p2: compare(p0, p1, p2))
        )

        stack = []
        stack.append(candidate_points[0])
        stack.append(candidate_points[1])
        canvas.create_line(
            stack[-1].x,
            stack[-1].y,
            stack[-2].x,
            stack[-2].y,
            fill="red",
            width=2,
            tags="convex_hull",
        )
        canvas.update_idletasks()
        canvas.after(1)
        stack.append(candidate_points[2])
        canvas.create_line(
            stack[-1].x,
            stack[-1].y,
            stack[-2].x,
            stack[-2].y,
            fill="red",
            width=2,
            tags="convex_hull",
        )
        canvas.update_idletasks()
        canvas.after(1)

        for i in range(3, len(candidate_points)):
            while (
                len(stack) > 1
                and orientation(stack[-2], stack[-1], candidate_points[i]) != 2
            ):
                canvas.create_line(
                    stack[-1].x,
                    stack[-1].y,
                    stack[-2].x,
                    stack[-2].y,
                    fill="green",
                    width=2,
                    tags="convex_hull",
                )
                canvas.update_idletasks()
                canvas.after(20)
                stack.pop()
            stack.append(candidate_points[i])
            draw_convex_hull_partial(stack, canvas, delay=50)
        canvas.create_line(
            stack[-1].x,
            stack[-1].y,
            stack[0].x,
            stack[0].y,
            fill="red",
            width=2,
            tags="convex_hull",
        )
        canvas.update_idletasks()
        canvas.after(10)
        return stack

    def graham_scan():
        if len(points) < 3:
            return

        p0 = min(points, key=lambda point: (point.y, point.x))
        candidate_points = sorted(
            points, key=cmp_to_key(lambda p1, p2: compare(p0, p1, p2))
        )

        stack = []
        stack.append(candidate_points[0])
        stack.append(candidate_points[1])
        stack.append(candidate_points[2])

        for i in range(3, len(candidate_points)):
            while (
                len(stack) > 1
                and orientation(stack[-2], stack[-1], candidate_points[i]) != 2
            ):
                stack.pop()
            stack.append(candidate_points[i])
        return stack

    start_time = timeit.default_timer()
    hull_points = graham_scan()
    end_time = timeit.default_timer()
    elapsed_time = (end_time - start_time) * 1000
    elapsed_time_text = f"Graham Scan: {elapsed_time:.2f} ms"

    display_time(elapsed_time_text, canvas)
    graham_scan_drawing()
    draw_convex_hull(hull_points, canvas)


def convex_hull_method_4(canvas, points):
    def quick_elimination(points):
        def isInsideBoundingBox(point, bounding_box):
            x_bb, y_bb = zip(
                *[(p.x, p.y) for p in bounding_box]
            )  # Extract x and y coordinates of bounding box vertices
            cross = 0
            for i in range(4):
                x1, y1, x2, y2 = x_bb[i - 1], y_bb[i - 1], x_bb[i], y_bb[i]

                if (x1 <= point.x < x2 or x2 <= point.x < x1) and point.y <= (
                    (y2 - y1) / (x2 - x1)
                ) * (point.x - x1) + y1:
                    cross += 1
            return cross % 2 != 0

        candidate_points = list(points)

        leftmost = min(candidate_points, key=lambda p: p.x)
        candidate_points.remove(leftmost)
        rightmost = max(candidate_points, key=lambda p: p.x)
        candidate_points.remove(rightmost)
        topmost = max(candidate_points, key=lambda p: p.y)
        candidate_points.remove(topmost)
        bottommost = min(candidate_points, key=lambda p: p.y)
        candidate_points.remove(bottommost)

        # Correct order of bounding box vertices
        bounding_box = [topmost, leftmost, bottommost, rightmost]

        # Eliminate points inside the bounding box
        remaining_points = [
            point
            for point in candidate_points
            if not isInsideBoundingBox(point, bounding_box)
        ]
        for point in bounding_box:
            remaining_points.append(point)

        return remaining_points

    def quick_elimination_drawing(points):
        def isInsideBoundingBox(point, bounding_box):
            x_bb, y_bb = zip(
                *[(p.x, p.y) for p in bounding_box]
            )  # Extract x and y coordinates of bounding box vertices
            cross = 0
            for i in range(4):
                x1, y1, x2, y2 = x_bb[i - 1], y_bb[i - 1], x_bb[i], y_bb[i]

                if (x1 <= point.x < x2 or x2 <= point.x < x1) and point.y <= (
                    (y2 - y1) / (x2 - x1)
                ) * (point.x - x1) + y1:
                    cross += 1
            return cross % 2 != 0

        candidate_points = list(points)

        leftmost = min(candidate_points, key=lambda p: p.x)
        candidate_points.remove(leftmost)
        rightmost = max(candidate_points, key=lambda p: p.x)
        candidate_points.remove(rightmost)
        topmost = max(candidate_points, key=lambda p: p.y)
        candidate_points.remove(topmost)
        bottommost = min(candidate_points, key=lambda p: p.y)
        candidate_points.remove(bottommost)

        # Correct order of bounding box vertices
        bounding_box = [topmost, leftmost, bottommost, rightmost]
        canvas.delete("convex_hull")
        canvas.create_line(
            topmost.x,
            topmost.y,
            leftmost.x,
            leftmost.y,
            fill="red",
            width=2,
            tags="convex_hull",
        )
        canvas.update_idletasks()
        canvas.after(1)

        canvas.create_line(
            leftmost.x,
            leftmost.y,
            bottommost.x,
            bottommost.y,
            fill="red",
            width=2,
            tags="convex_hull",
        )
        canvas.update_idletasks()
        canvas.after(1)
        canvas.create_line(
            bottommost.x,
            bottommost.y,
            rightmost.x,
            rightmost.y,
            fill="red",
            width=2,
            tags="convex_hull",
        )
        canvas.update_idletasks()
        canvas.after(1)
        canvas.create_line(
            rightmost.x,
            rightmost.y,
            topmost.x,
            topmost.y,
            fill="red",
            width=2,
            tags="convex_hull",
        )
        canvas.update_idletasks()
        canvas.after(1000)

        # Eliminate points inside the bounding box
        remaining_points = [
            point
            for point in candidate_points
            if not isInsideBoundingBox(point, bounding_box)
        ]
        for point in bounding_box:
            remaining_points.append(point)

        for point in remaining_points:
            canvas.create_oval(
                point.x - 3,
                point.y - 3,
                point.x + 3,
                point.y + 3,
                fill="green",
                outline="green",
                tags="convex_hull",
            )
        canvas.create_text(
            500 // 2,
            20,
            text="Points inside the bounding box are ignored.",
            font=("Helvetica", 12),
        )
        canvas.create_text(
            500 // 2,
            40,
            text="Graham Scan is Applied!",
            font=("Helvetica", 12),
        )
        canvas.update_idletasks()
        canvas.after(1000)

        return remaining_points

    def graham_scan():
        if len(points) < 3:
            return

        p0 = min(points, key=lambda point: (point.y, point.x))
        candidate_points = sorted(
            points, key=cmp_to_key(lambda p1, p2: compare(p0, p1, p2))
        )

        stack = []
        stack.append(candidate_points[0])
        stack.append(candidate_points[1])
        stack.append(candidate_points[2])

        for i in range(3, len(candidate_points)):
            while (
                len(stack) > 1
                and orientation(stack[-2], stack[-1], candidate_points[i]) != 2
            ):
                stack.pop()
            stack.append(candidate_points[i])
        return stack

    display_time("", canvas)
    copyPoints = points
    start_time = timeit.default_timer()
    points = quick_elimination(points)
    hull_points = graham_scan()
    end_time = timeit.default_timer()
    elapsed_time = (end_time - start_time) * 1000
    elapsed_time_text = f"Quick Elimination X Graham Scan: {elapsed_time:.2f} ms"
    quick_elimination_drawing(copyPoints)
    display_time(elapsed_time_text, canvas)
    canvas.delete("convex_hull")
    draw_convex_hull(hull_points, canvas, "green")


def convex_hull_method_5(canvas, points):
    def monotone_chain_drawing():
        if len(points) < 3:
            return

        candidate_points = sorted(set(points), key=lambda p: (p.x, p.y))
        canvas.delete("convex_hull")

        upper = []
        for point in candidate_points:
            while len(upper) >= 2 and calculate_det(upper[-2], upper[-1], point) <= 0:
                canvas.create_line(
                    upper[-1].x,
                    upper[-1].y,
                    upper[-2].x,
                    upper[-2].y,
                    fill="orange",
                    width=2,
                    tags="convex_hull",
                )
                canvas.update_idletasks()
                canvas.after(50)
                upper.pop()
            upper.append(point)
            draw_convex_hull_partial(upper, canvas, 10, True, "orange")

        lower = []
        for point in reversed(candidate_points):
            while len(lower) >= 2 and calculate_det(lower[-2], lower[-1], point) <= 0:
                canvas.create_line(
                    lower[-1].x,
                    lower[-1].y,
                    lower[-2].x,
                    lower[-2].y,
                    fill="green",
                    width=2,
                    tags="convex_hull",
                )
                canvas.update_idletasks()
                canvas.after(50)
                lower.pop()
            lower.append(point)
            draw_convex_hull_partial(lower, canvas, 10, True, "green")
            draw_convex_hull_partial(upper, canvas, 10, False, "orange")
        canvas.after(50)

        convex_hull = upper[:-1] + lower[:-1]
        return convex_hull

    def monotone_chain():
        if len(points) < 3:
            return

        # Sort the points lexicographically (tuples are compared lexicographically).
        # Remove duplicates to detect the case we have just one unique point.
        candidate_points = sorted(set(points), key=lambda p: (p.x, p.y))

        # Build lower hull
        lower = []
        for point in candidate_points:
            while len(lower) >= 2 and calculate_det(lower[-2], lower[-1], point) <= 0:
                lower.pop()
            lower.append(point)

        # Build upper hull
        upper = []
        for point in reversed(candidate_points):
            while len(upper) >= 2 and calculate_det(upper[-2], upper[-1], point) <= 0:
                upper.pop()
            upper.append(point)

        # Concatenation of the lower and upper hulls gives the convex hull.
        # Last point of each list is omitted because it is repeated at the beginning of the other list.
        convex_hull = lower[:-1] + upper[:-1]
        return convex_hull

    start_time = timeit.default_timer()
    hull_points = monotone_chain()
    end_time = timeit.default_timer()
    elapsed_time = (end_time - start_time) * 1000
    elapsed_time_text = f"Monotone chain: {elapsed_time:.2f} ms"

    display_time(elapsed_time_text, canvas)
    monotone_chain_drawing()
    draw_convex_hull(hull_points, canvas)


class PointGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point Generator")

        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        self.generate_button = tk.Button(
            root, text="Generate Random Points", command=self.generate_points
        )
        self.generate_button.pack(pady=10)

        self.clear_button = tk.Button(
            root, text="Clear Canvas", command=self.clear_canvas
        )
        self.clear_button.pack(pady=10)

        self.manual_button = tk.Button(
            root, text="Enable Manual Point", command=self.toggle_manual_point
        )
        self.manual_button.pack(pady=10)

        # Horizontal layout for convex hull methods
        self.horizontal_buttons_frame = tk.Frame(root)
        self.horizontal_buttons_frame.pack()

        self.convex_hull_bf_button = tk.Button(
            self.horizontal_buttons_frame,
            text="Brute Force",
            command=lambda: self.run_algorithm(convex_hull_method_1),
        )
        self.convex_hull_bf_button.pack(side=tk.LEFT, padx=5)

        self.convex_hull_2_button = tk.Button(
            self.horizontal_buttons_frame,
            text="Jarvis March",
            command=lambda: self.run_algorithm(convex_hull_method_2),
        )
        self.convex_hull_2_button.pack(side=tk.LEFT, padx=5)

        self.graham_scan_button = tk.Button(
            self.horizontal_buttons_frame,
            text="Graham Scan",
            command=lambda: self.run_algorithm(convex_hull_method_3),
        )
        self.graham_scan_button.pack(side=tk.LEFT, padx=5)

        self.convex_hull_3_button = tk.Button(
            self.horizontal_buttons_frame,
            text="Quick Elimination",
            command=lambda: self.run_algorithm(convex_hull_method_4),
        )
        self.convex_hull_3_button.pack(side=tk.LEFT, padx=5)

        self.convex_hull_4_button = tk.Button(
            self.horizontal_buttons_frame,
            text="Monotone chain",
            command=lambda: self.run_algorithm(convex_hull_method_5),
        )
        self.convex_hull_4_button.pack(side=tk.LEFT, padx=5)

        # Vertical layout for the rest of the buttons
        self.manual_point_enabled = False
        self.canvas.bind("<Button-1>", self.manual_point_click)

        self.points = []

    def run_algorithm(self, algorithm):
        algorithm(self.canvas, self.points)

    def generate_points(self):
        self.clear_canvas()
        self.points = []
        num_points = random.randint(10, 50)
        num_points = random.randint(25, 50)
        for _ in range(num_points):
            x = random.randint(110, 390)
            y = random.randint(110, 390)
            self.points.append(Point(x, y))
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []  # Clear the list of points

    def toggle_manual_point(self):
        self.manual_point_enabled = not self.manual_point_enabled
        if self.manual_point_enabled:
            self.manual_button["text"] = "Disable Manual Point"
        else:
            self.manual_button["text"] = "Enable Manual Point"

    def manual_point_click(self, event):
        if self.manual_point_enabled:
            x, y = event.x, event.y
            self.points.append(Point(x, y))
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = PointGeneratorApp(root)
    root.mainloop()
