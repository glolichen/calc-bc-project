from manim import *
import math

weirdfunc = lambda x: (2 * math.log(2, math.e) * math.exp(math.sin(x))) / math.log(x + 2, math.e)

PEDDIE_BLUE = RGBA.from_rgb([24, 52, 83])
PEDDIE_GOLD = RGBA.from_rgb([204, 152, 0])

class Disc(ThreeDScene):
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
        # text = Tex("Disc Method").scale(2)
        # self.play(Write(text))
        # self.wait(1)
        # self.play(Unwrite(text))

        axes = ThreeDAxes(
            x_range = [0, 6],
            y_range = [-4, 4],
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

        # comment to remove rendering solid
        # self.wait(2)
        #
        # self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        # self.begin_ambient_camera_rotation(rate=0.15)
        #
        # surface = Surface(
        #     lambda u, v: axes.c2p(
        #         v, weirdfunc(v) * np.cos(u), weirdfunc(v) * np.sin(u)
        #     ),
        #     u_range = [0, 2 * PI],
        #     v_range = [0, 5],
        #     fill_color = RED
        # )
        # surface.set_fill(RED)
        # self.play(Create(surface))
        # self.wait(2)
        #
        # self.move_camera(
        #     phi = 0 * DEGREES,
        #     theta = -90 * DEGREES, 
        #     zoom = 0.8,
        #     run_time = 1.5
        # )
        # self.set_camera_orientation(zoom=0.8)
        # self.stop_ambient_camera_rotation()
        #
        # self.wait(0.5)
        #
        # self.play(Uncreate(surface))
        # self.wait(2)
        # end comment to remove rendering solid

        integral_text = MathTex("A=\\int_{a}^{b} f(x)\\,\\mathrm dx", color=BLUE)
        integral_text.next_to(axes.coords_to_point(2.5, 0), DOWN, buff=0.2)
        integral_text.shift(RIGHT)
        integral_text.shift(RIGHT)
        self.play(Write(integral_text))

        riemann_text = MathTex("A\\approx \\sum_{i=1}^{n}f(x_i)\\Delta x", color=YELLOW_B)
        riemann_text.next_to(integral_text, DOWN, buff=0.2)

        riemann_rects = self.gen_riemann(weirdfunc, 0, 5, 5, axes)
        particular_rect = riemann_rects[1]
        particular_rect_under_brace = BraceLabel(particular_rect, r"\Delta x")
        particular_rect_right_brace = BraceLabel(particular_rect, r"f(x_i)", brace_direction=RIGHT)
        
        riemann = Group(*riemann_rects)
        self.play(
            FadeIn(riemann),
            Write(riemann_text)
        )
        self.wait(0.5)
        self.play(
            Write(particular_rect_under_brace),
            Write(particular_rect_right_brace)
        )

        # comment to remove riemann animation
        self.wait(1)
        self.remove(riemann)
        for i in range(6, 62, 5):
            riemann_rects_new = self.gen_riemann(weirdfunc, 0, 5, i, axes)
            riemann_new = Group(*riemann_rects_new)
            riemann_text_new = MathTex("A\\approx \\sum_{i=1}^{" + str(i) + "}f(x_i)\\Delta x", color=YELLOW_B)
            riemann_text_new.next_to(integral_text, DOWN, buff=0.2)

            particular_rect_new = riemann_rects_new[i // 5]
            particular_rect_under_brace_new = BraceLabel(particular_rect_new, r"\Delta x")
            particular_rect_right_brace_new = BraceLabel(particular_rect_new, r"f(x_i)", brace_direction=RIGHT)

            self.play(ChangeSpeed(AnimationGroup(
                Transform(riemann, riemann_new), 
                Transform(riemann_text, riemann_text_new),
                Transform(particular_rect_under_brace, particular_rect_under_brace_new),
                Transform(particular_rect_right_brace, particular_rect_right_brace_new),
            ), speedinfo={0: 2 if i < 25 else 5}, rate_func=linear))
            self.wait(0.1)

        riemann_text_new = MathTex("A=\\lim_{n\\to\\infty} \\sum_{i=1}^{n}f(x_i)\\Delta x", color=YELLOW_B)
        riemann_text_new.next_to(integral_text, DOWN, buff=0.2)
        self.play(
            Transform(riemann_text, riemann_text_new),
            FadeOut(particular_rect_under_brace),
            FadeOut(particular_rect_right_brace),
        )
        # end comment to remove riemann animation

        self.wait(2)

        riemann_rects_new = self.gen_riemann(weirdfunc, 0, 5, 10, axes)
        riemann_new = Group(*riemann_rects_new)
        riemann_text_new = MathTex("A \\approx \\sum_{i=1}^{10}f(x_i)\\Delta x", color=YELLOW_B)
        riemann_text_new.next_to(integral_text, DOWN, buff=0.2)

        particular_rect_new = riemann_rects_new[2]
        particular_rect_under_brace_new = BraceLabel(particular_rect_new, r"\Delta x")
        particular_rect_right_brace_new = BraceLabel(particular_rect_new, r"f(x_i)", brace_direction=RIGHT)

        self.play(
            Transform(riemann, riemann_new), 
            Transform(riemann_text, riemann_text_new),
        )
        self.wait(0.5)
        self.play(
            Write(particular_rect_under_brace_new),
            Write(particular_rect_right_brace_new),
        )

        self.wait(2)

        self.play(ChangeSpeed(AnimationGroup(
            Unwrite(riemann_text), Unwrite(integral_text), Unwrite(label)
        ), speedinfo = {0: 2}))
        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        self.begin_ambient_camera_rotation(rate=0.25)

        # comment to remove discs
        self.wait(0.5)
        cylinders = self.gen_x_cylinder_riemann(weirdfunc, 0, 5, 10, axes)
        self.add(riemann.copy())
        self.play(Transform(riemann, cylinders))
        # end comment to remove discs

        self.wait(2)
        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES + 0.25 * 2, zoom=0.6, run_time=1.5, frame_center=[0, 0, 3])
            
        disc_info1 = MathTex("\\text{Cylinder radius}=\\text{Rectangle height}=f(x_i)")
        disc_info1.scale(0.8)
        disc_info1.to_edge(UP)
        self.add_fixed_in_frame_mobjects(disc_info1)
        self.play(Write(disc_info1))

        disc_info2 = MathTex("\\text{Cylinder height}=\\text{Rectangle width}=\\Delta x")
        disc_info2.scale(0.8)
        disc_info2.next_to(disc_info1, DOWN)
        self.add_fixed_in_frame_mobjects(disc_info2)
        self.play(Write(disc_info2))

        self.wait(4)


class DiscText(Scene):
    def construct(self):
        # disc_info1 = MathTex("\\text{Cylinder radius}=\\text{Rectangle height}=f(x_i)")
        # disc_info2 = MathTex("\\text{Cylinder height}=\\text{Rectangle width}=\\Delta x")
        # disc_info3 = MathTex("\\implies \\text{Cylinder volume}=\\pi (f(x_i))^2 \\Delta x")
        # disc_info4 = MathTex("\\implies \\sum_{i=1}^{n}\\text{Cylinder volume}=\\sum_{i=1}^{n}\\pi (f(x_i))^2 \\Delta x")
        # disc_info5 = MathTex("\\implies \\sum_{i=1}^{n}\\text{Cylinder volume}=\\int_{a}^{b} \\pi (f(x))^2\\,\\mathrm dx")
        # 
        # disc_info1.move_to([0, 0, 0])
        # disc_info2.next_to(disc_info1, DOWN, buff=0.2)
        # disc_info3.next_to(disc_info2, DOWN, buff=0.2)
        # disc_info4.next_to(disc_info3, DOWN, buff=0.2)
        # disc_info5.next_to(disc_info4, DOWN, buff=0.2)
        # 
        # self.play(
        #     Write(disc_info1),
        #     Write(disc_info2),
        #     Write(disc_info3),
        #     Write(disc_info4),
        #     Write(disc_info5),
        # )

        info1 = MathTex(
            r"\text{Radius of cylinder }i&=\text{Rectangle height}=f(x_i)=r \\" \
            r"\text{Height of cylinder }i&=\text{Rectangle width}=\Delta x=h"
        )
        info1.move_to([0, 0, 0])

        info2 = MathTex(r"\implies \text{Volume of cylinder }i=\pi r^2 h=\pi (f(x_i))^2 \Delta x")
        info2.next_to(info1, DOWN, buff=0.2)

        info3 = MathTex(r"\implies \sum_{i=1}^{n}\text{Volume of cylinder }i=\sum_{i=1}^{n}\pi (f(x_i))^2 \Delta x")
        info3.next_to(info2, DOWN, buff=0.2)

        info4 = MathTex(r"\implies \text{Volume of $n$ cylinders}=\sum_{i=1}^{n}\pi (f(x_i))^2 \Delta x")
        info4.next_to(info2, DOWN, buff=0.2)

        info5 = MathTex(r"\implies \lim_{n\to\infty}\text{Volume of $n$ cylinders}=\lim_{n\to\infty}\sum_{i=1}^{n}\pi (f(x_i))^2 \Delta x")
        info5.next_to(info2, DOWN, buff=0.2)

        info6 = MathTex(r"\implies \text{Volume of solid of revolution}=\lim_{n\to\infty}\sum_{i=1}^{n}\pi (f(x_i))^2 \Delta x")
        info6.next_to(info2, DOWN, buff=0.2)

        info7 = MathTex(r"\text{Volume of solid of revolution}=\int_{a}^{b}\pi (f(x))^2 \,\mathrm dx")
        info7.next_to(info2, DOWN, buff=0.2)

        self.play(Write(info1))
        self.wait(1)
        self.play(Write(info2))
        self.wait(1)
        
        self.play(Write(info3))
        self.wait(3)
        self.play(Transform(info3, info4))
        self.wait(3)
        self.play(Transform(info3, info5))
        self.wait(3)
        self.play(Transform(info3, info6))
        self.wait(3)
        self.play(Transform(info3, info7))

        box = Rectangle(width=info7.width + 0.5, height=info7.height + 0.5)
        box.move_to(info7)
        self.play(ChangeSpeed(Create(box), speedinfo={0: 0.75}))

        self.wait(8)