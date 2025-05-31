from manim import *
import math

weirdfunc = lambda x: 1.5 * (2.5 / (x + 1) - 0.5)
weirdfunc_inv = lambda y: 2.5 / (y / 1.5 + 0.5) - 1

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

    def gen_y_axis_parallel_cylinder(self, axes, center_x, center_y, center_z, radius, height, color):
        face1 = axes.c2p(center_x, center_y - height / 2, center_z)
        face2 = axes.c2p(center_x, center_y + height / 2, center_z)
        real_height = abs(face2[1] - face1[1])
        
        point3 = axes.c2p(center_x + radius, center_y, center_z)
        real_radius = abs(point3[0] - face1[0])

        cylinder = Cylinder(
            radius = real_radius,
            height = real_height,
            direction = Y_AXIS,
            fill_color = color,
            stroke_color = color,
            stroke_width = 1
        )
        cylinder.move_to(axes.c2p(center_x, center_y, center_z))
        return cylinder
    
    def gen_y_cylinder_riemann(self, function, a, b, subintervals, axes):
        dy = (b - a) / subintervals
        cylinders = []
        for i in range(subintervals):
            yi = a + i * dy
            color = PEDDIE_BLUE if i % 2 == 0 else PEDDIE_GOLD
            cylinder = self.gen_y_axis_parallel_cylinder(
                axes, 0, yi + dy / 2, 0,
                function(yi + dy), dy, color
            )
            cylinder.set_opacity(0.5)
            cylinders.append(cylinder)
        return cylinders

    def gen_riemann(self, function, a, b, subintervals, axes):
        dx = (b - a) / subintervals
        rects = []
        for i in range(subintervals):
            xi = a + i * dx
            rect = self.gen_rectangle(axes, xi, 0, xi + dx, function(xi + dx), BLUE_E)
            rects.append(rect)
        return rects

    def construct(self):
        # disc_method_text = Tex("Cylindrical Shells").scale(2)
        # self.play(Write(disc_method_text))
        # self.wait(1)
        # self.play(Unwrite(disc_method_text))

        axes = ThreeDAxes(
            x_range = [-5, 5],
            y_range = [-1, 4],
            z_range = [-5, 5],
            x_length = config.frame_height + 2.5,
            z_length = config.frame_height + 2.5,
        ).scale(0.8)

        x_label = axes.get_x_axis_label(Tex("$x$"))
        y_label = axes.get_y_axis_label(Tex("$y$"))
        z_label = axes.get_z_axis_label(Tex("$z$"))

        function_plot = axes.plot(
            weirdfunc,
            x_range = [0, 4],
            color = BLUE
        )

        label = MathTex("y = f(x)", color=BLUE)
        label.next_to(axes.c2p(1, weirdfunc(1)), UR, buff=0.2)

        self.set_camera_orientation(zoom=0.8)

        self.play(
            FadeIn(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(z_label),
            Write(function_plot),
            Write(label)
        )
        
        self.wait(2)
        
        surface = Surface(
            lambda u, v: axes.c2p(
                v * np.cos(u),    # x = r cos(u)
                weirdfunc(v),
                v * np.sin(u)     # z = r sin(u)
            ),
            u_range = [0, 2 * PI],
            v_range = [0, 4],
            checkerboard_colors = [PEDDIE_BLUE, PEDDIE_GOLD]
        )
        surface.set_opacity(0.5)

        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES, gamma=115 * DEGREES, zoom=0.7, frame_center=axes.c2p(0, 1.5, 0), run_time=1.5)
        # self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        # self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(1)
        self.play(
            ChangeSpeed(Create(surface), speedinfo={0: 0.5}),
            FadeOut(label)
        )
        self.play(Unwrite(function_plot))
        
        self.wait(4)
        
        disc_method_text = Tex("Using the disc method...")
        disc_method_text.to_edge(UP)
        self.add_fixed_in_frame_mobjects(disc_method_text)
        self.play(Write(disc_method_text))

        self.wait(4)
        
        cylinders = self.gen_y_cylinder_riemann(weirdfunc_inv, 0, 3, 9, axes)
        surface_group = Group(surface)
        cylinders_group = Group(*cylinders)
        function_plot = axes.plot(
            weirdfunc,
            x_range = [0, 4],
            color = BLUE
        )
        self.play(
            Transform(surface_group, cylinders_group),
            Write(function_plot)
        )
        
        self.wait(4)
        
        individual_cylinder = cylinders[0]
        disc_method_text_new = Tex("Using the disc method...")
        disc_method_text_new.to_corner(UL)
        self.play(
            FadeOut(surface_group),
            FadeIn(individual_cylinder),
            Transform(disc_method_text, disc_method_text_new)
        )
        
        label_new = MathTex("y", "=", "f(x)", color=BLUE)
        label_new.next_to(axes.c2p(1, weirdfunc(1)), UR, buff=0.2)
        self.add_fixed_in_frame_mobjects(label_new)
        self.play(Write(label_new))
        
        self.wait(2)

        temp_cylinder = self.gen_y_axis_parallel_cylinder(axes, 0, 3 / 9, 2.5 / 2, 2.5 / 2, 3 / 9, WHITE)
        radius_brace = Brace(temp_cylinder, UP, color=YELLOW_B)
        radius_brace.rotate(90 * DEGREES, Y_AXIS, axes.c2p(0, 3 / 9, 2.5 / 2))
        
        radius_brace_label = MathTex(r"\text{Radius}", color=YELLOW_B)
        radius_brace_label.next_to(radius_brace, UP)
        radius_brace_label.scale(0.8)
        radius_brace_label.shift(LEFT)
        radius_brace_label.shift(UP / 4)
        self.add_fixed_in_frame_mobjects(radius_brace_label)

        self.play(Write(radius_brace), Write(radius_brace_label))
        self.wait(2)

        disc_method_integral = MathTex(r"V=\pi\int_{0}^{3}(", r"\text{Radius}", r")^2\,\mathrm dy")
        disc_method_integral.set_color_by_tex("Radius", YELLOW_B)
        disc_method_integral.to_corner(UR)
        self.add_fixed_in_frame_mobjects(disc_method_integral)
        self.play(Write(disc_method_integral))
        self.wait(4)

        radius_brace_label2 = MathTex("x", "=", r"\text{Radius}")
        radius_brace_label2.set_color_by_tex("x", BLUE)
        radius_brace_label2.set_color_by_tex("Radius", YELLOW_B)
        radius_brace_label2.scale(0.8)
        radius_brace_label2.move_to(radius_brace_label)
        need_move = (radius_brace_label2.width - radius_brace_label.width) / 2
        radius_brace_label2.shift(LEFT * need_move)
        self.add_fixed_in_frame_mobjects(radius_brace_label2)
        self.play(FadeOut(radius_brace_label), FadeIn(radius_brace_label2))
        self.wait(2)

        is_invertible_text = Tex(r"(if $f$ is invertible...)", font_size=36)
        is_invertible_text.to_corner(DR)
        self.add_fixed_in_frame_mobjects(is_invertible_text)
        self.play(Write(is_invertible_text))
        self.wait(1)

        label_new_new = MathTex("x=f^{-1}(y)", color=BLUE)
        label_new_new.move_to(label_new)
        self.add_fixed_in_frame_mobjects(label_new_new)
        self.play(FadeOut(label_new), FadeIn(label_new_new))
        
        self.wait(4)

        radius_brace_label3 = MathTex("f^{-1}(y)", "=", r"\text{Radius}")
        radius_brace_label3.set_color_by_tex("y", BLUE)
        radius_brace_label3.set_color_by_tex("Radius", YELLOW_B)
        radius_brace_label3.scale(0.8)
        radius_brace_label3.move_to(radius_brace_label2)
        need_move = (radius_brace_label3.width - radius_brace_label2.width) / 2
        radius_brace_label3.shift(LEFT * need_move)
        self.add_fixed_in_frame_mobjects(radius_brace_label3)
        self.play(FadeOut(radius_brace_label2), FadeIn(radius_brace_label3))
        self.wait(4)
        
        # self.wait(4)
        # self.gen_rec

        self.wait(4)
