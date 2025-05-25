from manim import *
import math

weirdfunc = lambda x: (2 * math.log(2, math.e) * math.exp(math.sin(x))) / math.log(x + 2, math.e)

PEDDIE_BLUE = RGBA.from_rgb([24, 52, 83])
PEDDIE_GOLD = RGBA.from_rgb([204, 152, 0])

class SurfaceArea(ThreeDScene):
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

    # must have x1 < x2
    def gen_x_axis_truncated_cone(self, axes, x1, y1, x2, y2, color):
        slope = (y1 - y2) / (x1 - x2)
        c = y1 - slope * x1
        function = lambda x : slope * x + c
        cone = Surface(
            lambda u, v: axes.c2p(
                v, function(v) * np.cos(u), function(v) * np.sin(u)
            ),
            u_range = [0, 2 * PI],
            v_range = [x1, x2],
            checkerboard_colors = [color]
        )
        return cone
    
    def gen_x_truncated_cone_riemann(self, function, a, b, subintervals, axes):
        dx = (b - a) / subintervals
        cones = []
        for i in range(subintervals):
            xi = a + i * dx
            color = PEDDIE_BLUE if i % 2 == 0 else PEDDIE_GOLD
            cone = self.gen_x_axis_truncated_cone(
                axes,
                x1 = xi,
                y1 = function(xi),
                x2 = xi + dx,
                y2 = function(xi + dx),
                color = color
            )
            cone.set_opacity(0.8)
            cones.append(cone)
        return cones

    def construct(self):
        text = Tex("Surface Area").scale(2)
        self.play(Write(text))
        self.wait(1)
        self.play(Unwrite(text))

        axes = ThreeDAxes(
            x_range = [0, 6],
            y_range = [-4, 4],
            z_range = [-4, 4],
            y_length = 8,
            z_length = 8,
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
        label.next_to(axes.coords_to_point(2.3, weirdfunc(2.3)), UR, buff=0.2)

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
        self.move_camera(phi=75 * DEGREES, theta=-30 * DEGREES, zoom=0.8, run_time=1.5, frame_center=[0, 0, 0.8])
        self.begin_ambient_camera_rotation(rate=-0.1)
        
        # comment to remove surface
        surface = Surface(
            lambda u, v: axes.c2p(
                v, weirdfunc(v) * np.cos(u), weirdfunc(v) * np.sin(u)
            ),
            u_range = [0, 2 * PI],
            v_range = [0, 5],
            checkerboard_colors = [PEDDIE_BLUE, PEDDIE_GOLD]
        )
        self.play(Create(surface))
        self.wait(1)

        display_text = Tex("How to find the surface area of this surface?")
        display_text.to_edge(UP)
        self.add_fixed_in_frame_mobjects(display_text)
        self.play(Write(display_text))

        self.wait(3)

        display_text_new = Tex(r"Divide surface into \underline{truncated cones}")
        display_text_new.to_edge(UP)
        self.play(Transform(display_text, display_text_new))

        self.wait(1)

        cones = self.gen_x_truncated_cone_riemann(weirdfunc, 0, 5, 5, axes)
        riemann = Group(*cones)
        surface = Group(surface)

        self.play(Transform(surface, riemann))

        self.wait(2)

        display_text_2 = MathTex(r"\text{Surface Area}\approx \sum_{i=1}^{n} \text{Area of Slant}")
        display_text_2.scale(0.7)
        display_text_2.next_to(display_text, DOWN)
        self.add_fixed_in_frame_mobjects(display_text_2)
        self.play(Write(display_text_2))

        self.wait(2)

        individual_cone = Group(cones[1])
        self.play(
            Transform(surface, individual_cone),
        )

        self.play(
            Unwrite(display_text),
            Unwrite(display_text_2),
        )
        # end comment to remove surface
        
        # if removing surface, uncomment below
        # cones = self.gen_x_truncated_cone_riemann(weirdfunc, 0, 5, 5, axes)
        # surface = Group(cones[1])
        # self.add(surface)
        # end uncomment below

        # comment to remove spinning around individual cone
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=-0.25)
        self.move_camera(
            zoom = 0.6,
            run_time = 1.5,
            frame_center = axes.c2p(1.5, 0, 0),
        )
        self.wait(6)
        # end comment

        self.move_camera(
            phi = 0 * DEGREES,
            theta = -90 * DEGREES, 
            zoom = 0.8,
            run_time = 1.5,
            frame_center = axes.c2p(2.5, 0, 0),
        )
        self.set_camera_orientation(zoom=0.8)
        self.stop_ambient_camera_rotation()

        self.wait(1)
        self.play(
            FadeOut(function_plot),
            FadeOut(label)
        )
        
        # comment to skip slant height explanation
        slant_line_start = axes.c2p(1, weirdfunc(1), 0),
        slant_line_end = axes.c2p(2, weirdfunc(2), 0),
        slant_line = Line(start=slant_line_start, end=slant_line_end)

        slant_line_start = slant_line_start[0]
        slant_line_end = slant_line_end[0]

        slant_vector_angle = math.atan((slant_line_end[1] - slant_line_start[1]) / (slant_line_end[0] - slant_line_start[0]))
        slant_vector = [-math.sin(slant_vector_angle), math.cos(slant_vector_angle), 0]

        slant_height_brace = Brace(slant_line, slant_vector, color=YELLOW_B)
        slant_height_brace_text = MathTex(r"S=\text{Slant Height}", color=YELLOW_B)
        slant_height_brace_text.move_to(slant_height_brace)
        slant_height_brace_text.shift(np.array(slant_vector) * 0.6)

        self.play(
            Write(slant_height_brace),
            Write(slant_height_brace_text)
        )

        self.wait(2)

        fake_rectangle_left = self.gen_rectangle(axes, 1, weirdfunc(1), 1, 0, WHITE)
        fake_rectangle_right = self.gen_rectangle(axes, 2, weirdfunc(2), 2, 0, WHITE)

        cone_above_brace = BraceLabel(surface, r"H=\text{Height}", brace_direction=DOWN)
        cone_left_brace = BraceLabel(fake_rectangle_left, r"R=\text{Outer radius}", brace_direction=LEFT, color=BLUE_B)
        cone_left_brace.set_color(BLUE_B)
        cone_right_brace = BraceLabel(fake_rectangle_right, r"r=\text{Inner radius}", brace_direction=RIGHT, color=TEAL_C)
        cone_right_brace.set_color(TEAL_C)

        self.play(Write(cone_above_brace))
        self.wait(1)
        self.play(Write(cone_left_brace))
        self.wait(1)
        self.play(Write(cone_right_brace))

        self.wait(4)

        slant_area_formula_LHS = Tex("Area of Slant")
        slant_area_formula_equal = MathTex("=")

        slant_area_formula = MathTex(r"\pi", "S", "(", "R", "+", "r", ")", tex_environment="gather*", color=WHITE)
        slant_area_formula.set_color_by_tex("S", YELLOW_B)
        slant_area_formula.set_color_by_tex("R", BLUE_B)
        slant_area_formula.set_color_by_tex("r", TEAL_C)
        slant_area_formula_equal.move_to(axes.c2p(4, -2, 0))

        slant_area_formula.next_to(slant_area_formula_equal, DOWN * 1.5)
        slant_area_formula_LHS.next_to(slant_area_formula_equal, UP * 1.5)

        self.play(
            Write(slant_area_formula_LHS),
            Write(slant_area_formula_equal),
            Write(slant_area_formula)
        )

        self.wait(4)

        self.play(FadeIn(function_plot))

        xi_label = MathTex("x_i")
        xi_next_label = MathTex("x_{i+1}")

        xi_label.next_to(axes.c2p(1, -3, 0), DOWN, buff=0.2)
        xi_next_label.next_to(axes.c2p(2, -3, 0), DOWN, buff=0.2)

        cone_above_brace_new = BraceLabel(surface, r"H=\Delta x", brace_direction=DOWN)
        cone_left_brace_new = BraceLabel(fake_rectangle_left, r"R=f(x_i)", brace_direction=LEFT)
        cone_left_brace_new.set_color(BLUE_B)
        cone_right_brace_new = BraceLabel(fake_rectangle_right, r"r=f(x_{i+1})", brace_direction=RIGHT)
        cone_right_brace_new.set_color(TEAL_C)

        self.wait(2)

        self.play(Transform(cone_above_brace, cone_above_brace_new))
        self.wait(2)

        slant_area_formula_new = MathTex(r"\pi", "S", "(", "f(x_i)", "+", "r", ")", tex_environment="gather*")
        slant_area_formula_new.set_color_by_tex("S", YELLOW_B)
        slant_area_formula_new.set_color_by_tex("f(x_i)", BLUE_B)
        slant_area_formula_new.set_color_by_tex("r", TEAL_C)
        slant_area_formula_new.next_to(slant_area_formula_equal, DOWN * 1.5)
        self.play(
            Transform(cone_left_brace, cone_left_brace_new),
            Transform(slant_area_formula, slant_area_formula_new)
        )
        self.wait(2)

        slant_area_formula_new = MathTex(r"\pi", "S", "(", "f(x_i)", "+", "f(x_{i+1})", ")", tex_environment="gather*")
        slant_area_formula_new.set_color_by_tex("S", YELLOW_B)
        slant_area_formula_new.set_color_by_tex("f(x_i)", BLUE_B)
        slant_area_formula_new.set_color_by_tex("f(x_{i+1})", TEAL_C)
        slant_area_formula_new.next_to(slant_area_formula_equal, DOWN * 1.5)
        self.play(
            Transform(cone_right_brace, cone_right_brace_new),
            Transform(slant_area_formula, slant_area_formula_new)
        )

        self.wait(4)

        fake_rectangle_slant = self.gen_rectangle(axes, 2, weirdfunc(1), 2, weirdfunc(2), WHITE)
        cone_slant_brace = Brace(fake_rectangle_slant, RIGHT)
        cone_slant_brace_text = MathTex("f(x_{i+1})", "-", "f(x_i)")
        cone_slant_brace_text.set_color_by_tex("f(x_i)", BLUE_B)
        cone_slant_brace_text.set_color_by_tex("f(x_{i+1})", TEAL_C)
        cone_slant_brace_text.next_to(cone_slant_brace, RIGHT)
        self.play(
            Write(cone_slant_brace),
            Write(cone_slant_brace_text)
        )

        self.wait(4)

        slant_height_brace_text_new = MathTex(r"S=\sqrt{(\Delta x)^2 + \left(f(x_{i+1})-f(x_i)\right)^2}", color=YELLOW_B)
        slant_height_brace_text_new.move_to(slant_height_brace)
        slant_height_brace_text_new.shift(np.array(slant_vector) * 0.8)
        slant_height_brace_text_new.shift(RIGHT * 2)
        self.play(Transform(slant_height_brace_text, slant_height_brace_text_new))

        self.wait(1)

        pythag_text = Tex(r"(Pythagorean\\theorem)", font_size=32, color=YELLOW_B)
        pythag_text.to_corner(UL)
        self.play(FadeIn(pythag_text))

        self.wait(6)

        self.play(FadeOut(pythag_text))

        slant_area_formula_LHS_new = Tex("Area of Slant")
        slant_area_formula_equal_new = MathTex("=")
        slant_area_formula_new = MathTex(r"\pi", r"\sqrt{(\Delta x)^2 + \left(f(x_{i+1})-f(x_i)\right)^2}", "(", "f(x_i)", "+", "f(x_{i+1})", ")", tex_environment="gather*")

        slant_area_formula_new.set_color_by_tex("f(x_i)", BLUE_B)
        slant_area_formula_new.set_color_by_tex("f(x_{i+1})", TEAL_C)
        slant_area_formula_new.set_color_by_tex(r"\Delta", YELLOW_B)

        slant_area_formula_equal_new.move_to(axes.c2p(3.5, -2, 0))
        slant_area_formula_LHS_new.next_to(slant_area_formula_equal_new, UP * 1.5)
        slant_area_formula_new.next_to(slant_area_formula_equal_new, DOWN * 1.5)

        slant_area_formula_LHS_new.scale(0.85)
        slant_area_formula_equal_new.scale(0.85)
        slant_area_formula_new.scale(0.85)

        surface_new = cones[1]
        surface_new.set_opacity(0.2)
        self.play(
            FadeOut(y_label),
            FadeOut(z_label),
            Unwrite(cone_above_brace),
            Transform(surface, Group(surface_new)),
            Transform(slant_area_formula_LHS, slant_area_formula_LHS_new),
            Transform(slant_area_formula_equal, slant_area_formula_equal_new),
            Transform(slant_area_formula, slant_area_formula_new),
        )

        slant_formula_group = Group(
            slant_area_formula_LHS,
            slant_area_formula_equal,
            slant_area_formula,
        )

        slant_formula_box = Rectangle(width=slant_formula_group.width + 0.5, height=slant_formula_group.height + 0.5)
        slant_formula_box.move_to(slant_formula_group)
        self.play(ChangeSpeed(Create(slant_formula_box), speedinfo={0: 0.75}))

        self.wait(4)

        self.play(
            Unwrite(cone_left_brace),
            Unwrite(cone_right_brace),
            Unwrite(cone_slant_brace),
            Unwrite(cone_slant_brace_text),
            Unwrite(slant_height_brace),
            Unwrite(slant_height_brace_text),
            ChangeSpeed(Uncreate(slant_formula_box), speedinfo={0: 0.75})
        )

        self.play(
            FadeOut(slant_area_formula_LHS),
            FadeOut(slant_area_formula_equal),
        )
        self.wait(2)
        # end comment to skip slant height explanation

        # if commenting to skip slant height explanation, uncomment below
        # slant_area_formula = MathTex(r"\pi", r"\sqrt{(\Delta x)^2 + \left(f(x_{i+1})-f(x_i)\right)^2}", "(", "f(x_i)", "+", "f(x_{i+1})", ")", tex_environment="gather*")
        # slant_area_formula.set_color_by_tex("f(x_i)", BLUE_B)
        # slant_area_formula.set_color_by_tex("f(x_{i+1})", TEAL_C)
        # slant_area_formula.set_color_by_tex(r"\Delta", YELLOW_B)
        # slant_area_formula.move_to(axes.c2p(3.5, -2 - 1.5, 0))
        # slant_area_formula.scale(0.85)
        # self.add(slant_area_formula)
        # end uncomment

        cones[1].set_opacity(0.8)
        surface_new = Group(*cones)
        self.play(Transform(surface, surface_new))

        self.wait(2)

        surface_area_approx_text = MathTex(r"\text{Surface Area}\approx \sum_{i=1}^{n} \text{Area of Slant}")
        surface_area_approx_text.scale(0.7)
        surface_area_approx_text.to_edge(UP)
        self.play(Write(surface_area_approx_text))

        self.wait(4)

        surface_area_approx_text_new = MathTex(
            r"\text{SA}\approx \sum_{i=1}^{n}\pi\sqrt{(\Delta x)^2+\left(f(x_{i+1})-f(x_i)\right)^2}(f(x_i)+f(x_{i+1}))"
        )
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.to_edge(UP)
        surface_area_approx_text_new.shift(RIGHT)

        surface_area_approx = Group(surface_area_approx_text, slant_area_formula)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))

        self.wait(4)

        cone_under_dx_label = BraceLabel(cones[2], r"x_{i+1}-x_i", brace_direction=DOWN)
        self.play(Write(cone_under_dx_label))
        self.wait(2)

        cone_under_dx_label_new = BraceLabel(cones[2], r"\Delta x", brace_direction=DOWN)
        self.play(Transform(cone_under_dx_label, cone_under_dx_label_new))
        self.wait(1)
        
        rect_representing_cone = self.gen_rectangle(axes, 2, 0, 3, 0, WHITE)
        cone_under_dx_label_new = BraceLabel(rect_representing_cone, r"\Delta x", brace_direction=DOWN, buff=0.1)
        self.play(Transform(cone_under_dx_label, cone_under_dx_label_new))
        self.wait(2)

        xi_label = MathTex("x_i")
        xi_next_label = MathTex("x_{i+1}")
        xi_label.next_to(axes.c2p(2, -weirdfunc(2), 0), DOWN)
        xi_next_label.next_to(axes.c2p(3, -weirdfunc(3), 0), DOWN, buff=0.5)
        self.play(
            Write(xi_label),
            Write(xi_next_label)
        )
        self.wait(2)
        
        xi_next_label_new = MathTex(r"x_i+\Delta x")
        xi_next_label_new.scale(0.8)
        xi_next_label_new.move_to(xi_next_label)
        self.play(Transform(xi_next_label, xi_next_label_new))
        self.wait(2)

        surface_area_approx_text_new = MathTex(
            r"\text{SA}\approx \sum_{i=1}^{n}",
            r"\pi\sqrt{(\Delta x)^2+\left(f(x_i+\Delta x)-f(x_i)\right)^2}(f(x_i)+f(x_i+\Delta x))"
        )
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        surface_area_approx_text_new.shift(RIGHT * 0.5)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(4)

        prompt_text = Tex("Factor $\Delta x$ from square root...", font_size=36)
        prompt_text.to_corner(DR)
        self.play(Write(prompt_text))
        self.wait(2)

        surface_area_approx_text_new = MathTex(
            r"\text{SA}\approx \sum_{i=1}^{n}",
            r"\pi\sqrt{", r"{(\Delta x)^2}", r"+", r"{(\Delta x)^2}",
            r"\frac{\left(f(x_i+\Delta x)-f(x_i)\right)^2}{(\Delta x)^2}}(f(x_i)+f(x_i+\Delta x))"
        )
        surface_area_approx_text_new.set_color_by_tex(r"\Delta", TEAL_B)
        surface_area_approx_text_new.set_color_by_tex(r"x_i", WHITE)
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        surface_area_approx_text_new.shift(RIGHT * 0.5)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(6)

        surface_area_approx_text_new = MathTex(
            r"\text{SA}\approx \sum_{i=1}^{n}\pi",
            r"\sqrt{(\Delta x)^2}", r"\sqrt{1+\frac{\left(f(x_i+\Delta x)-f(x_i)\right)^2}{(\Delta x)^2}}(f(x_i)+f(x_i+\Delta x))"
        )
        surface_area_approx_text_new.set_color_by_tex(r"\Delta", TEAL_B)
        surface_area_approx_text_new.set_color_by_tex(r"x_i", WHITE)
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(6)

        surface_area_approx_text_new = MathTex(
            r"\text{SA}\approx \sum_{i=1}^{n}\pi",
            r"\Delta x", r"\sqrt{1+\frac{\left(f(x_i+\Delta x)-f(x_i)\right)^2}{(\Delta x)^2}}(f(x_i)+f(x_i+\Delta x))"
        )
        surface_area_approx_text_new.set_color_by_tex(r"\Delta", TEAL_B)
        surface_area_approx_text_new.set_color_by_tex(r"x_i", WHITE)
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        self.play(
            Transform(surface_area_approx, surface_area_approx_text_new),
            Unwrite(xi_label),
            Unwrite(xi_next_label)
        )
        self.wait(4)

        surface_area_approx_text_new = MathTex(
            r"\text{SA}\approx \sum_{i=1}^{n}\pi\Delta x\sqrt{1+\left(\frac{f(x_i+\Delta x)-f(x_i)}{\Delta x}\right)^2}(f(x_i)+f(x_i+\Delta x))"
        )
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(4)
        prompt_text_new = Tex("As the number of cones approaches infinity...", font_size=36)
        prompt_text_new.to_corner(DR)
        self.play(Transform(prompt_text, prompt_text_new))
        self.wait(2)
        
        # surface is the old thing
        # for i in range(61, 62, 1):
        for i in range(6, 62, 5):
            riemann_cones = self.gen_x_truncated_cone_riemann(weirdfunc, 0, 5, i, axes)
            surface_new = Group(*riemann_cones)
            cone_under_dx_label_new = BraceLabel(riemann_cones[round(i / 5 * 2)], r"\Delta x", brace_direction=DOWN)
            self.play(
                Transform(surface, surface_new),
                Transform(cone_under_dx_label, cone_under_dx_label_new)
            )
            self.wait(1)
            
        surface_area_approx_text_new = MathTex(
            r"\text{SA}=\lim_{n\to\infty}\sum_{i=1}^{n}\pi\Delta x\sqrt{1+\left(\frac{f(x_i+\Delta x)-f(x_i)}{\Delta x}\right)^2}(f(x_i)+f(x_i+\Delta x))"
        )
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(2)

        prompt_text_new = Tex(r"... then $\Delta x$ approaches $0$", font_size=36)
        prompt_text_new.to_corner(DR)
        self.play(Transform(prompt_text, prompt_text_new))
        self.wait(2)

        prompt_text_second = Tex(r"... so $x_i+\Delta x$ approaches $x_i$", font_size=36)
        prompt_text_second.next_to(prompt_text_new, UP)
        self.play(Write(prompt_text_second))
        self.wait(2)
        
        surface_area_approx_text_new = MathTex(
            r"\text{SA}=\lim_{n\to\infty}\sum_{i=1}^{n}\pi\Delta x\sqrt{1+\left(\frac{f(x_i+\Delta x)-f(x_i)}{\Delta x}\right)^2}(f(x_i)+f(x_i))"
        )
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(2)

        surface_area_approx_text_new = MathTex(
            r"\text{SA}=\lim_{n\to\infty}\sum_{i=1}^{n}\pi\Delta x\sqrt{1+\left(\frac{f(x_i+\Delta x)-f(x_i)}{\Delta x}\right)^2}(2f(x_i))"
        )
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(2)

        prompt_text_third = Tex(r"... and notice the limit definition of derivative", font_size=36)
        need_move = (prompt_text_third.width - prompt_text_second.width) / 2
        prompt_text_third.next_to(prompt_text_second, UP)
        prompt_text_third.shift(LEFT * need_move)
        self.play(Write(prompt_text_third))
        self.wait(4)
        
        # TODO: draw some kind of rectangle i guess
        surface_area_approx_text_new = MathTex(
            r"\text{SA}=\lim_{n\to\infty}\sum_{i=1}^{n}\pi\Delta x\sqrt{1+\left(f'(x_i)\right)^2}(2f(x_i))"
        )
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(4)

        surface_area_approx_text_new = MathTex(
            r"\text{SA}=\lim_{n\to\infty}\sum_{i=1}^{n}2\pi f(x_i) \Delta x\sqrt{1+\left(f'(x_i)\right)^2}"
        )
        surface_area_approx_text_new.scale(0.7)
        surface_area_approx_text_new.move_to(surface_area_approx)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(2)

        prompt_text_fourth = Tex(r"... this is a Riemann sum", font_size=36)
        need_move = (prompt_text_third.width - prompt_text_fourth.width) / 2
        prompt_text_fourth.next_to(prompt_text_third, UP)
        prompt_text_fourth.shift(RIGHT * need_move)
        self.play(Write(prompt_text_fourth))
        self.wait(3)

        surface_area_approx_text_new = MathTex(
            r"\text{SA}=\int_{a}^{b} 2\pi f(x) \sqrt{1+\left(f'(x)\right)^2}\,\mathrm dx"
        )
        surface_area_approx_text_new.move_to(surface_area_approx)
        self.play(Transform(surface_area_approx, surface_area_approx_text_new))
        self.wait(0.5)

        formula_box = Rectangle(width=surface_area_approx.width + 0.5, height=surface_area_approx.height + 0.5)
        formula_box.move_to(surface_area_approx)
        self.play(ChangeSpeed(Create(formula_box), speedinfo={0: 0.75}))

        self.wait(6)