from manim import *
import math

weirdfunc = lambda x: 1.5 * (2.5 / (x + 1) - 0.5)
weirdfunc_inv = lambda y: 2.5 / (y / 1.5 + 0.5) - 1

PEDDIE_BLUE = RGBA.from_rgb([24, 52, 83])
PEDDIE_BLUE_LIGHT = RGBA.from_rgb([24 * 2, 52 * 2, 83 * 2])
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

    def gen_y_axis_parallel_cylinder(self, axes, center_x, center_y, center_z, radius, height, color, show_ends):
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
            stroke_width = 1,
            show_ends = show_ends
        )
        cylinder.move_to(axes.c2p(center_x, center_y, center_z))
        return cylinder
    
    def gen_y_disc_riemann(self, function, a, b, subintervals, axes):
        dy = (b - a) / subintervals
        cylinders = []
        for i in range(subintervals):
            yi = a + i * dy
            color = PEDDIE_BLUE if i % 2 == 0 else PEDDIE_GOLD
            cylinder = self.gen_y_axis_parallel_cylinder(
                axes, 0, yi + dy / 2, 0,
                function(yi + dy), dy, color, True
            )
            cylinder.set_opacity(0.5)
            cylinders.append(cylinder)
        return cylinders

    def gen_y_shell_riemann(self, function, a, b, subintervals, axes, show_ends):
        dx = (b - a) / subintervals
        cylinders = []
        for i in range(0, subintervals - 1):
            xi = a + i * dx
            color = PEDDIE_BLUE_LIGHT if i % 2 == 0 else PEDDIE_GOLD
            value = function(xi + dx)
            cylinder = self.gen_y_axis_parallel_cylinder(
                axes, 0, value / 2, 0,
                xi + dx, value, color, show_ends
            )
            cylinder.set_fill(color)
            cylinder.set_opacity(1)
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
        disc_method_text = Tex("Cylindrical Shells").scale(2)
        self.play(Write(disc_method_text))
        self.wait(1)
        self.play(Unwrite(disc_method_text))

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

        # COMMENT TO SKIP EXPLANATION OF WHY DISC DOESN'T WORK
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
                v * np.cos(u),
                weirdfunc(v),
                v * np.sin(u)
            ),
            u_range = [0, 2 * PI],
            v_range = [0, 4],
            checkerboard_colors = [PEDDIE_BLUE, PEDDIE_GOLD]
        )
        surface.set_opacity(0.5)

        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, gamma=115 * DEGREES, zoom=0.7, frame_center=axes.c2p(0, 1.5, 0), run_time=1.5)
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
        
        cylinders = self.gen_y_disc_riemann(weirdfunc_inv, 0, 3, 9, axes)
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

        temp_cylinder = self.gen_y_axis_parallel_cylinder(axes, 0, 3 / 9, 2.5 / 2, 2.5 / 2, 3 / 9, WHITE, True)
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
        
        self.wait(1)

        radius_brace_label3 = MathTex("f^{-1}(y)", "=", r"\text{Radius}")
        radius_brace_label3.set_color_by_tex("y", BLUE)
        radius_brace_label3.set_color_by_tex("Radius", YELLOW_B)
        radius_brace_label3.scale(0.8)
        radius_brace_label3.move_to(radius_brace_label2)
        need_move = (radius_brace_label3.width - radius_brace_label2.width) / 2
        radius_brace_label3.shift(LEFT * need_move)
        self.add_fixed_in_frame_mobjects(radius_brace_label3)
        self.play(FadeOut(radius_brace_label2), FadeIn(radius_brace_label3))
        self.wait(2)
        
        disc_method_integral_group = Group(
            disc_method_integral,
            radius_brace,
            radius_brace_label3
        )
        
        disc_method_integral_new = MathTex(r"V=\pi\int_{0}^{3}(", r"f^{-1}(y)", r")^2\,\mathrm dy")
        disc_method_integral_new.set_color_by_tex("f", BLUE)
        disc_method_integral_new.to_corner(UR)
        self.play(
            Transform(disc_method_integral_group, Group(disc_method_integral_new)), 
            FadeOut(is_invertible_text)
        )
        self.wait(0.5)

        disc_method_formula_box = Rectangle(width=disc_method_integral_new.width + 0.5, height=disc_method_integral_new.height + 0.5)
        self.add_fixed_in_frame_mobjects(disc_method_formula_box)
        disc_method_formula_box.move_to(disc_method_integral_new)
        self.play(ChangeSpeed(Create(disc_method_formula_box), speedinfo={0: 0.75}))
        self.wait(2)
        
        disc_method_bad_text = Tex(r"\textbf{does not work if \\ $f$ cannot be inverted.}", color=RED)
        disc_method_bad_text.next_to(disc_method_text, DOWN)
        self.add_fixed_in_frame_mobjects(disc_method_bad_text)
        self.play(Write(disc_method_bad_text))
        self.wait(6)

        self.play(
            Unwrite(disc_method_text),
            Unwrite(disc_method_bad_text),
            Uncreate(disc_method_formula_box),
            FadeOut(disc_method_integral_group),
            Unwrite(label_new_new)
        )
        self.play(FadeOut(individual_cylinder))
        # END COMMENT

        surface = Surface(
            lambda u, v: axes.c2p(
                v * np.cos(u),
                weirdfunc(v),
                v * np.sin(u)
            ),
            u_range = [0, 2 * PI],
            v_range = [0, 4],
            checkerboard_colors = [PEDDIE_BLUE, PEDDIE_GOLD]
        )
        surface.set_opacity(0.75)

        # IF COMMENT ABOVE UNCOMMENT BELOW
        # self.play(
        #     FadeIn(axes),
        #     FadeIn(x_label),
        #     FadeIn(y_label),
        #     FadeIn(z_label),
        #     Write(function_plot)
        # )
        # self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, gamma=115 * DEGREES, zoom=0.7, frame_center=axes.c2p(0, 1.5, 0), run_time=1.5)
        # END UNCOMMENT
        
        self.wait(1)

        # COMMENT TO REMOVE TEXT
        self.play(ChangeSpeed(Create(surface), speedinfo={0: 0.75}))
        shell_text = Tex(r"We can use \underline{cylindrical shells} instead.")
        shell_text.to_edge(UP)
        self.add_fixed_in_frame_mobjects(shell_text)
        self.play(Write(shell_text))
        self.wait(4)

        shell_text_new = Tex(r"Divide the solid into \underline{hollow cylinders}")
        shell_text_new.move_to(shell_text)
        self.play(Transform(shell_text, shell_text_new))
        self.wait(4)
        # END COMMENT
    
        surface_more_transparent = Surface(
            lambda u, v: axes.c2p(
                v * np.cos(u),
                weirdfunc(v),
                v * np.sin(u)
            ),
            u_range = [PI / 2, 2 * PI],
            v_range = [0, 4],
            fill_color = WHITE
        )
        surface_more_transparent.set_opacity(0.2)
        self.play(Transform(surface, surface_more_transparent))

        cylinders = self.gen_y_shell_riemann(weirdfunc, 0, 4, 6, axes, True)
        for cylinder in cylinders:
            # COMMENT FOR FASTER RENDERING
            self.play(Create(cylinder))
            self.wait(0.4)
            # END COMMENT

            # IF COMMENTING ABOVE UNCOMMENT
            # self.add(cylinder)
            # END UNCOMMENT
        
        # COMMENT TO REMOVE TEXT
        self.wait(2)
        self.play(Unwrite(shell_text))
        self.wait(2)
        # END COMMENT

        shell_text2 = Tex(r"As the number of shells $\to\infty$...")
        shell_text2.to_edge(UP)
        self.add_fixed_in_frame_mobjects(shell_text2)
        self.play(Write(shell_text2))
        
        self.wait(1)

        cylinders_group = Group(*cylinders)

        # COMMENT TO SKIP RIEMANN
        for i in range(12, 37, 6):
            cylinders_new = self.gen_y_shell_riemann(weirdfunc, 0, 4, i, axes, True)
            cylinders_new_group = Group(*cylinders_new)
            self.play(Transform(cylinders_group, cylinders_new_group))
            self.wait(0.2)
        # END COMMENT
    
        # IF COMMENTING ABOVE UNCOMMENT
        # cylinders_new = self.gen_y_shell_riemann(weirdfunc, 0, 4, 8, axes, True)
        # cylinders_new_group = Group(*cylinders_new)
        # self.play(Transform(cylinders_group, cylinders_new_group))
        # self.wait(1)
        # END UNCOMMENT

        # COMMENT TO REMOVE TEXT
        shell_text3 = Tex(r"then volume of solid $\to\sum \text{volume of each cylindrical shell}$")
        shell_text3.scale(0.8)
        shell_text3.to_edge(UP)
        self.add_fixed_in_frame_mobjects(shell_text3)
        self.play(FadeOut(shell_text2), FadeIn(shell_text3))
        self.wait(4)

        shell_text4 = MathTex(r"V=\lim_{n\to\infty}\sum_{i=1}^{n}", r"\text{volume of shell }i")
        shell_text4.set_color_by_tex("volume", TEAL)
        shell_text4.scale(0.8)
        shell_text4.to_edge(UP)
        self.add_fixed_in_frame_mobjects(shell_text4)
        self.play(FadeOut(shell_text3), FadeIn(shell_text4))
            
        self.wait(6)
        # END COMMENT
        
        self.wait(1)

        cylinders_new = self.gen_y_shell_riemann(weirdfunc, 0, 4, 6, axes, True)
        cylinders_new_group = Group(*cylinders_new)
        self.play(Transform(cylinders_group, cylinders_new_group), Unwrite(shell_text4))
        
        self.wait(2)

        dx = 4 / 6
        individual_cylinder_max_y = weirdfunc(dx * 3)
        individual_cylinder_outside = self.gen_y_axis_parallel_cylinder(
            axes, 0, individual_cylinder_max_y / 2, 0,
            dx * 3, individual_cylinder_max_y, PEDDIE_BLUE_LIGHT, False
        )
        individual_cylinder_outside.set_fill(PEDDIE_BLUE_LIGHT)
        individual_cylinder_outside.set_opacity(1)

        individual_cylinder_inside = self.gen_y_axis_parallel_cylinder(
            axes, 0, individual_cylinder_max_y / 2, 0,
            dx * 2, individual_cylinder_max_y, PEDDIE_BLUE_LIGHT, False
        )
        individual_cylinder_inside.set_fill(PEDDIE_BLUE_LIGHT)
        individual_cylinder_inside.set_opacity(0.8)

        individual_cylinder_top = Surface(
            lambda u, v: axes.c2p(
                v * np.cos(u),
                individual_cylinder_max_y,
                v * np.sin(u)
            ),
            u_range = [0, 2 * PI],
            v_range = [dx * 2, dx * 3],
            fill_color = PEDDIE_BLUE_LIGHT
        )
        individual_cylinder_top.set_opacity(0.8)

        self.add(individual_cylinder_outside, individual_cylinder_inside, individual_cylinder_top)
        self.play(FadeOut(cylinders_group))
        
        self.wait(2)

        height_brace = Brace(individual_cylinder_outside, [1, 0, 0], color=LIGHT_PINK)
        height_brace.rotate(45 * DEGREES, Y_AXIS, axes.c2p(0, 0, 0))
        height_text = MathTex(r"\text{Height}=f(x_i)", color=LIGHT_PINK)
        height_text.next_to(height_brace, np.array([1, 0, 1]))
        height_text.shift(UP * 0.85)
        self.play(Write(height_brace))
        self.add_fixed_in_frame_mobjects(height_text)
        self.play(Write(height_text))
        self.wait(2)

        height_text_new = MathTex(r"\text{Height}=f(x_i)", color=LIGHT_PINK)
        height_text_new.to_corner(DR)
        self.play(Transform(height_text, height_text_new))

        self.play(Unwrite(function_plot), FadeOut(surface), Unwrite(height_brace))
        self.move_camera(phi=-90 * DEGREES, theta=90 * DEGREES, gamma=180 * DEGREES, zoom=0.7, frame_center=axes.c2p(0, dx / 2, 0), run_time=1.5)
        self.wait(1)

        inside_label = MathTex("x_i", color=TEAL)
        inside_label.move_to(axes.c2p(dx * 2, 0, -2.5))
        inside_label.rotate(90 * DEGREES, X_AXIS)
        inside_arrow = Arrow(axes.c2p(dx * 2, 0, -2.5 + 0.4), axes.c2p(dx * 2, 0, 0), stroke_width=3, max_tip_length_to_length_ratio=0.125, buff=0, color=TEAL)
        inside_arrow.rotate(90 * DEGREES, Z_AXIS)
        self.play(Write(inside_label), Write(inside_arrow))
        self.wait(0.5)

        outside_label = MathTex("x_{i+1}", color=RED)
        outside_label.move_to(axes.c2p(dx * 3, 0, 2.5))
        outside_label.rotate(90 * DEGREES, X_AXIS)
        outside_arrow = Arrow(axes.c2p(dx * 3, 0, 2.5 - 0.4), axes.c2p(dx * 3, 0, 0), stroke_width=3, max_tip_length_to_length_ratio=0.125, buff=0, color=RED)
        outside_arrow.rotate(90 * DEGREES, Z_AXIS)
        self.play(Write(outside_label), Write(outside_arrow))
        self.wait(2)

        inside_fake_cylinder = self.gen_y_axis_parallel_cylinder(
            axes, dx * 2 / 2, individual_cylinder_max_y / 2, -dx * 2 / 2,
            dx * 2 / 2, individual_cylinder_max_y, WHITE, True  
        )
        inside_brace = Brace(inside_fake_cylinder)
        inside_brace.rotate(90 * DEGREES, Y_AXIS)
        inside_brace.rotate(90 * DEGREES, Z_AXIS)
        inside_brace.move_to(axes.c2p(2 + 0.4, 0, -dx * 2 / 2))
        inside_brace_text = MathTex("r", color=TEAL)
        inside_brace_text.next_to(inside_brace, np.array([1, 0, 0]))
        inside_brace_text.rotate(90 * DEGREES, X_AXIS)
        self.play(Write(inside_brace), Write(inside_brace_text))
        self.wait(0.5)

        outside_fake_cylinder = self.gen_y_axis_parallel_cylinder(
            axes, dx * 3 / 2, individual_cylinder_max_y / 2, dx * 3 / 2,
            dx * 3 / 2, individual_cylinder_max_y, WHITE, True  
        )
        outside_brace = Brace(outside_fake_cylinder)
        outside_brace.rotate(90 * DEGREES, Y_AXIS)
        outside_brace.rotate(90 * DEGREES, Z_AXIS)
        outside_brace.move_to(axes.c2p(2 + 0.4, 0, dx * 3 / 2))
        outside_brace_text = MathTex("R", color=RED)
        outside_brace_text.next_to(outside_brace, np.array([1, 0, 0]))
        outside_brace_text.rotate(90 * DEGREES, X_AXIS)
        self.play(Write(outside_brace), Write(outside_brace_text))
        self.wait(4)

        cross_section_area_text = MathTex(r"\text{Cross section area}=\pi", "R", r"^2 - \pi", "r", "^2")
        cross_section_area_text.set_color_by_tex("R", RED)
        cross_section_area_text.set_color_by_tex("r", TEAL)
        cross_section_area_text.set_color_by_tex(r"\pi", WHITE)
        old_text_height = cross_section_area_text.height
        cross_section_area_text.rotate(90 * DEGREES, X_AXIS)
        cross_section_area_text.move_to(axes.c2p(-6.5, 0, 4))
        self.play(Write(cross_section_area_text))
        self.wait(4)

        inside_brace_text_new = MathTex("r", "=", "x_i")
        inside_brace_text_new.set_color_by_tex("r", TEAL)
        inside_brace_text_new.set_color_by_tex("x", TEAL)
        inside_brace_text_new.next_to(inside_brace, np.array([1, 0, 0]))
        inside_brace_text_new.rotate(90 * DEGREES, X_AXIS)
        inside_brace_group = Group(inside_brace_text, inside_arrow, inside_label)
        self.play(Transform(inside_brace_group, inside_brace_text_new))
        self.wait(0.5)

        outside_brace_text_new = MathTex("R", "=", "x_{i+1}")
        outside_brace_text_new.set_color_by_tex("R", RED)
        outside_brace_text_new.set_color_by_tex("x", RED)
        outside_brace_text_new.next_to(outside_brace, np.array([1, 0, 0]))
        outside_brace_text_new.rotate(90 * DEGREES, X_AXIS)
        outside_brace_group = Group(outside_brace_text, outside_arrow, outside_label)
        self.play(Transform(outside_brace_group, outside_brace_text_new))
        self.wait(2)

        cross_section_area_text_new = MathTex(r"\text{Cross section area}&=\pi(", "x_{i+1}", r")^2 - \pi(", "x_i", ")^2")
        cross_section_area_text_new.set_color_by_tex("i", TEAL)
        cross_section_area_text_new.set_color_by_tex("i+1", RED)
        cross_section_area_text_new.set_color_by_tex(r"\pi", WHITE)
        need_move_down = (cross_section_area_text_new.height - old_text_height) / 2
        old_text_height = cross_section_area_text_new.height
        cross_section_area_text_new.rotate(90 * DEGREES, X_AXIS)
        cross_section_area_text_new.move_to(cross_section_area_text)
        need_move = (cross_section_area_text_new.width - cross_section_area_text.width) / 2
        cross_section_area_text_new.shift(RIGHT * need_move)
        cross_section_area_text_new.shift([0, 0, -need_move_down])
        self.play(Transform(cross_section_area_text, cross_section_area_text_new))
        self.wait(4)

        cross_section_area_text_new = MathTex(r"\text{Cross section area}&=\pi(", "x_{i+1}", r")^2 - \pi(", "x_i", r")^2 \\ &= \pi \left( (", r"x_{i+1}", r")^2-(", "x_i", r")^2 \right)")
        cross_section_area_text_new.set_color_by_tex("i", TEAL)
        cross_section_area_text_new.set_color_by_tex("i+1", RED)
        cross_section_area_text_new.set_color_by_tex(r"\pi", WHITE)
        cross_section_area_text_new.set_color_by_tex(r"right", WHITE)
        need_move = (cross_section_area_text_new.height - old_text_height) / 2
        old_text_height = cross_section_area_text_new.height
        cross_section_area_text_new.rotate(90 * DEGREES, X_AXIS)
        cross_section_area_text_new.move_to(cross_section_area_text)
        cross_section_area_text_new.shift(RIGHT * (cross_section_area_text_new.width - cross_section_area_text.width) / 2)
        cross_section_area_text_new.shift([0, 0, -need_move])
        self.play(FadeIn(cross_section_area_text_new))
        self.remove(cross_section_area_text)
        cross_section_area_text = cross_section_area_text_new
        self.wait(4)

        individual_cylinder_outside.set_opacity(0.1)
        individual_cylinder_inside.set_opacity(0.1)
        individual_cylinder_top.set_opacity(0.1)
        inside_brace.set_opacity(0.1)
        inside_brace_text.set_opacity(0.1)
        inside_arrow.set_opacity(0.1)
        inside_label.set_opacity(0.1)
        outside_brace.set_opacity(0.1)
        outside_brace_text.set_opacity(0.1)
        outside_arrow.set_opacity(0.1)
        outside_label.set_opacity(0.1)
        axes.set_opacity(0.1)
        z_label.set_opacity(0.1)

        self.wait(1)

        cross_section_area_text_new = MathTex(
            r"\text{Cross section area}&=\pi(x_{i+1})^2 - \pi(x_i)^2 \\ &= \pi \left( (x_{i+1})^2-(x_i)^2 \right) \\",
            r"\text{Volume of shell}", r"&=\pi \left( (", r"x_{i+1}", r")^2-(", "x_i", r")^2 \right)(", r"\text{Height}", ")"
        )
        cross_section_area_text_new.set_color_by_tex("i", TEAL)
        cross_section_area_text_new.set_color_by_tex("i+1", RED)
        cross_section_area_text_new.set_color_by_tex(r"\pi", WHITE)
        cross_section_area_text_new.set_color_by_tex("right", WHITE)
        cross_section_area_text_new.set_color_by_tex("Height", LIGHT_PINK)
        cross_section_area_text_new.set_color_by_tex("Volume", GREEN)
        cross_section_area_text_new.set_color_by_tex("Cross", BLACK)
        need_move = (cross_section_area_text_new.height - old_text_height) / 2
        old_text_height = cross_section_area_text_new.height
        cross_section_area_text_new.rotate(90 * DEGREES, X_AXIS)
        cross_section_area_text_new.move_to(cross_section_area_text)
        cross_section_area_text_new.shift(RIGHT * (cross_section_area_text_new.width - cross_section_area_text.width) / 2)
        cross_section_area_text_new.shift([0, 0, -need_move])
        self.play(Write(cross_section_area_text_new))
        self.wait(4)

        cross_section_area_text_new2 = MathTex(
            r"\text{Cross section area}&=\pi(x_{i+1})^2 - \pi(x_i)^2 \\ &= \pi \left( (x_{i+1})^2-(x_i)^2 \right) \\",
            r"\text{Volume of shell}", r"&=", r"\pi \left( (", r"x_{i+1}", r")^2-(", "x_i", r")^2 \right)", r"f(x_i)"
        )
        cross_section_area_text_new2.set_color_by_tex("i", TEAL)
        cross_section_area_text_new2.set_color_by_tex("i+1", RED)
        cross_section_area_text_new2.set_color_by_tex("f", LIGHT_PINK)
        cross_section_area_text_new2.set_color_by_tex(r"\pi", WHITE)
        cross_section_area_text_new2.set_color_by_tex("right", WHITE)
        cross_section_area_text_new2.set_color_by_tex("Height", LIGHT_PINK)
        cross_section_area_text_new2.set_color_by_tex("Volume", GREEN)
        cross_section_area_text_new2.set_color_by_tex("Cross", BLACK)
        need_move = (cross_section_area_text_new2.height - old_text_height) / 2
        old_text_height = cross_section_area_text_new2.height
        cross_section_area_text_new2.rotate(90 * DEGREES, X_AXIS)
        cross_section_area_text_new2.move_to(cross_section_area_text_new)
        cross_section_area_text_new2.shift(RIGHT * (cross_section_area_text_new2.width - cross_section_area_text_new.width) / 2)
        cross_section_area_text_new2.shift([0, 0, -need_move])
        self.play(
            FadeIn(cross_section_area_text_new2),
            FadeOut(cross_section_area_text_new),
            Unwrite(height_brace),
            Unwrite(height_text)
        )
        cross_section_area_text_new = cross_section_area_text_new2
        self.wait(2)
        
        self.play(
            FadeOut(individual_cylinder_outside),
            FadeOut(individual_cylinder_inside),
            FadeOut(individual_cylinder_top),
            FadeOut(axes),
            FadeOut(z_label),
            FadeOut(inside_brace),
            FadeOut(inside_brace_text),
            FadeOut(inside_label),
            FadeOut(outside_brace),
            FadeOut(outside_brace_text),
            FadeOut(outside_label),
            FadeOut(cross_section_area_text)
        )
        
        cross_section_area_text_new.generate_target()
        cross_section_area_text_new.target.move_to(axes.c2p(0, 0, 6))
        
        self.play(MoveToTarget(cross_section_area_text_new))
        self.wait(4)
        
        formula_text2 = MathTex(
            r"V=\lim_{n\to\infty}\sum_{i=1}^{n}", r"\text{Volume of shell}", r"=", r"\lim_{n\to\infty}\sum_{i=1}^{n}\pi \left( (", r"x_{i+1}", r")^2-(", "x_i", r")^2 \right)", r"f(x_i)"
        )
        formula_text2.set_color_by_tex("i", TEAL)
        formula_text2.set_color_by_tex("i+1", RED)
        formula_text2.set_color_by_tex("f", LIGHT_PINK)
        formula_text2.set_color_by_tex(r"\pi", WHITE)
        formula_text2.set_color_by_tex("right", WHITE)
        formula_text2.set_color_by_tex("infty", WHITE)
        formula_text2.set_color_by_tex("Volume", GREEN)
        formula_text2.rotate(90 * DEGREES, X_AXIS)
        formula_text2.next_to(cross_section_area_text_new, np.array([0, 0, -1]))
        self.play(Write(formula_text2))
        self.wait(4)

        formula_text2_new = MathTex(
            r"V=", r"\lim_{n\to\infty}\sum_{i=1}^{n}\pi \left( (", r"x_{i+1}", r")^2-(", "x_i", r")^2 \right)", r"f(x_i)"
        )
        formula_text2_new.set_color_by_tex("i", TEAL)
        formula_text2_new.set_color_by_tex("i+1", RED)
        formula_text2_new.set_color_by_tex("f", LIGHT_PINK)
        formula_text2_new.set_color_by_tex(r"\pi", WHITE)
        formula_text2_new.set_color_by_tex("right", WHITE)
        formula_text2_new.rotate(90 * DEGREES, X_AXIS)
        formula_text2_new.move_to(formula_text2)
        self.play(Transform(formula_text2, formula_text2_new))
        self.wait(2)

        formula_text2_new = MathTex(
            r"V=", r"\lim_{n\to\infty}\sum_{i=1}^{n}\pi \left( (", r"x_i\hspace{0pt}", "+", r"\Delta x", r")^2-(", "x_i", r")^2 \right)", r"f(x_i)"
        )
        formula_text2_new.set_color_by_tex("i", TEAL)
        formula_text2_new.set_color_by_tex("f", LIGHT_PINK)
        formula_text2_new.set_color_by_tex(r"\pi", WHITE)
        formula_text2_new.set_color_by_tex("right", WHITE)
        formula_text2_new.set_color_by_tex("Delta", RED)
        formula_text2_new.set_color_by_tex("hspace", RED)
        formula_text2_new.rotate(90 * DEGREES, X_AXIS)
        formula_text2_new.move_to(formula_text2)
        self.play(Transform(formula_text2, formula_text2_new))
        self.wait(4)

        formula_text3 = MathTex(
            r"V=", r"\lim_{n\to\infty}\sum_{i=1}^{n}\pi \left( (", r"x_i\hspace{0pt}", ")^2+2(", r"\Delta x", ")(", r"x_i\hspace{0pt}", ")+", "(", r"\Delta x", ")^2-(", "x_i", r")^2 \right)", r"f(x_i)"
        )
        formula_text3.set_color_by_tex("i", TEAL)
        formula_text3.set_color_by_tex("f", LIGHT_PINK)
        formula_text3.set_color_by_tex(r"\pi", WHITE)
        formula_text3.set_color_by_tex("right", WHITE)
        formula_text3.set_color_by_tex("Delta", RED)
        formula_text3.set_color_by_tex("hspace", RED)
        formula_text3.rotate(90 * DEGREES, X_AXIS)
        formula_text3.next_to(formula_text2, np.array([0, 0, -1]))
        self.play(Write(formula_text3))
        self.wait(8)

        formula_text3_new = MathTex(
            r"V=", r"\lim_{n\to\infty}\sum_{i=1}^{n}\pi \left( 2(", r"\Delta x", ")(", "x_i", ")+", "(", r"\Delta x", r")^2\right)", r"f(x_i)"
        )
        formula_text3_new.set_color_by_tex("i", RED)
        formula_text3_new.set_color_by_tex("f", LIGHT_PINK)
        formula_text3_new.set_color_by_tex(r"\pi", WHITE)
        formula_text3_new.set_color_by_tex("right", WHITE)
        formula_text3_new.set_color_by_tex("Delta", RED)
        formula_text3_new.rotate(90 * DEGREES, X_AXIS)
        formula_text3_new.move_to(formula_text3)
        self.play(Transform(formula_text3, formula_text3_new))
        self.wait(4)

        formula_text4 = MathTex(
            r"V=", r"\lim_{n\to\infty}\sum_{i=1}^{n}\pi", "(", r"\Delta x", r")\left( 2(", r"x_i", ")+", r"\Delta x", r"\right)", r"f(x_i)", 
        )
        formula_text4.set_color_by_tex("i", RED)
        formula_text4.set_color_by_tex("f", LIGHT_PINK)
        formula_text4.set_color_by_tex(r"\pi", WHITE)
        formula_text4.set_color_by_tex("left", WHITE)
        formula_text4.set_color_by_tex("right", WHITE)
        formula_text4.set_color_by_tex("Delta", RED)
        formula_text4.rotate(90 * DEGREES, X_AXIS)
        formula_text4.next_to(formula_text3, np.array([0, 0, -1]))
        self.play(Write(formula_text4))
        self.wait(2)
        
        prompt_text = MathTex(r"\text{As }n\to0\text{, }", r"\Delta x", r"\to 0\text{ and }2(", r"x_i", ")+", r"\Delta x", r"\to2(", "x_i", ").")
        prompt_text.set_color_by_tex("x", RED)
        prompt_text.set_color_by_tex("text", WHITE)
        prompt_text.rotate(90 * DEGREES, X_AXIS)
        prompt_text.next_to(formula_text4, np.array([0, 0, -1]))
        prompt_text.shift(RIGHT * 4)
        prompt_text.shift(np.array([0, 0, -3]))
        self.play(Write(prompt_text))
        self.wait(4)

        formula_text4_new = MathTex(
            r"V=", r"\lim_{n\to\infty}\sum_{i=1}^{n}\pi", "(", r"\Delta x", r")(2(", r"x_i", "))", r"f(x_i)", 
        )
        formula_text4_new.set_color_by_tex("i", RED)
        formula_text4_new.set_color_by_tex("f", LIGHT_PINK)
        formula_text4_new.set_color_by_tex(r"\pi", WHITE)
        formula_text4_new.set_color_by_tex("Delta", RED)
        formula_text4_new.rotate(90 * DEGREES, X_AXIS)
        formula_text4_new.move_to(formula_text4)
        self.play(Transform(formula_text4, formula_text4_new))
        self.wait(4)

        formula_text4_new = MathTex(
            r"V=", r"\lim_{n\to\infty}\sum_{i=1}^{n}2\pi", "(", r"\Delta x", r")(", r"x_i", ")", r"f(x_i)", 
        )
        formula_text4_new.set_color_by_tex("i", RED)
        formula_text4_new.set_color_by_tex("f", LIGHT_PINK)
        formula_text4_new.set_color_by_tex(r"\pi", WHITE)
        formula_text4_new.set_color_by_tex("Delta", RED)
        formula_text4_new.rotate(90 * DEGREES, X_AXIS)
        formula_text4_new.move_to(formula_text4)
        self.play(Transform(formula_text4, formula_text4_new))
        self.wait(4)

        formula_text5 = MathTex(
            r"V=", r"\int_{a}^{b} 2\pi", "x", "f(x)", r"\,\mathrm dx" 
        )
        formula_text5.set_color_by_tex("x", RED)
        formula_text5.set_color_by_tex("f", LIGHT_PINK)
        formula_text5.set_color_by_tex(r"\pi", WHITE)
        formula_text5.set_color_by_tex("mathrm", WHITE)
        formula_width, formula_height = formula_text5.width, formula_text5.height
        formula_text5.rotate(90 * DEGREES, X_AXIS)
        formula_text5.next_to(formula_text4, np.array([0, 0, -1]))
        self.play(Write(formula_text5))
        self.wait(0.5)

        final_formula_box = Rectangle(width=formula_width + 0.5, height=formula_height + 0.5)
        final_formula_box.move_to(formula_text5)
        final_formula_box.rotate(90 * DEGREES, X_AXIS)
        self.play(ChangeSpeed(Create(final_formula_box), speedinfo={0: 0.75}))

        self.wait(8)

        # END WORK