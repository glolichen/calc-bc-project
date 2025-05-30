from manim import *
import math

weirdfunc = lambda x: math.sqrt(x + 0.1) + 0.3

PEDDIE_BLUE = RGBA.from_rgb([24, 52, 83])
PEDDIE_GOLD = RGBA.from_rgb([204, 152, 0])

class Shell(ThreeDScene):
    # x's and y's in terms of axes coordinates
    def gen_rectangle(self, axes, x1, y1, x2, y2, color):
        point1 = axes.c2p(x1, y1)
        point2 = axes.c2p(x2, y2)
        height = abs(point2[1] - point1[1])
        width = abs(point2[0] - point1[0])
        rect = Rectangle(height = height, width = width, color = color)
        rect.set_fill(color, 0.5)
        rect.move_to(axes.c2p((x1 + x2) / 2, (y1 + y2) / 2))
        return rect

    def gen_x_axis_parallel_cylinder(self, axes, center_x, center_y, center_z, radius, height, color):
        face1 = axes.c2p(center_x - height / 2, center_y, center_z)
        face2 = axes.c2p(center_x + height / 2, center_y, center_z)
        real_height = abs(face2[0] - face1[0])

        cylinder = Cylinder(
            radius = radius,
            height = real_height,
            direction = X_AXIS,
            fill_color = color,
            stroke_color = PEDDIE_GOLD,
            stroke_width = 1
        )
        cylinder.move_to(axes.c2p(center_x, center_y, center_z))
        return cylinder
    
    def gen_x_cylinder_riemann(self, function, a, b, subintervals, axes):
        dx = (b - a) / subintervals
        cylinders = []
        for i in range(subintervals):
            xi = a + i * dx
            # color = PEDDIE_BLUE if i % 2 == 0 else PEDDIE_GOLD
            color = YELLOW_D
            cylinder = self.gen_x_axis_parallel_cylinder(
                axes, xi + dx / 2, 0, 0,
                function(xi + dx), dx, color
            )
            cylinder.set_opacity(0.5)
            cylinders.append(cylinder)
        return Group(*cylinders)

    def gen_riemann(self, function, a, b, subintervals, axes):
        dx = (b - a) / subintervals
        rects = []
        for i in range(subintervals):
            xi = a + i * dx
            rect = self.gen_rectangle(axes, xi, 0, xi + dx, function(xi + dx), BLUE_E)
            rects.append(rect)
        return rects

    def construct(self):
        text = Tex("Cylindical Shell").scale(2)
        self.play(Write(text))
        self.wait(1)
        self.play(Unwrite(text))

        axes = ThreeDAxes(
            x_range = [-5, 5],
            y_range = [-1, 4],
        ).scale(0.8)

        x_label = axes.get_x_axis_label(Tex("$x$"))
        y_label = axes.get_y_axis_label(Tex("$y$"))
        z_label = axes.get_z_axis_label(Tex("$z$"))

        function_plot = axes.plot(
            weirdfunc,
            x_range = [0, 5],
            color = BLUE
        )

        label = MathTex("y = f(x)", color=BLUE)
        label.next_to(axes.coords_to_point(3, weirdfunc(3)), UL, buff=0.2)

        self.set_camera_orientation(zoom=0.8)

        self.play(
            FadeIn(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(z_label),
            Write(function_plot),
            Write(label)
        )

        # comment to remove rendering solid
        self.wait(2)

        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        self.begin_ambient_camera_rotation(rate=-0.15)

        surface = Surface(
            lambda u, v: axes.c2p(
                v * np.cos(u),    # x = r cos(u)
                weirdfunc(v),
                v * np.sin(u)     # z = r sin(u)
            ),
            u_range = [0, 2 * PI],
            v_range = [0, 5],
            fill_color = RED
        )
        surface.set_fill(RED)
        self.play(Create(surface), FadeOut(label))
        self.wait(8)

        self.move_camera(
            phi = 0 * DEGREES,
            theta = -90 * DEGREES, 
            zoom = 0.8,
            run_time = 1.5
        )
        self.set_camera_orientation(zoom=0.8)
        self.stop_ambient_camera_rotation()

        self.wait(0.5)