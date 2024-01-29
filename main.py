from collections import deque
import flet as ft


class PointCounter(ft.UserControl):
    def build(self):
        self.cur_exo_disp = ft.TextField(expand=True, on_submit=self.set_note)
        self.points_labels = ft.Text(expand=True)
        self.total_labels = ft.Text(width=110)
        self.points:list[int|float] = [0]
        self.add_buttons = [
            ft.OutlinedButton(str(x), on_click=self.adder(x), width=150, height=70) for x in [0.25, 0.5, 0.75, 1, 2, 3, 4, 5, 10]
        ]
        self.rem_buttons = [
            ft.OutlinedButton(str(x), on_click=self.adder(x), width=150, height=70) for x in [-0.25, -0.5, -0.75, -1, -2, -3, -4, -5, -10]
        ]

        self.logs_txt = ""
        self.logs_disp = ft.Text("", theme_style=ft.TextThemeStyle.BODY_LARGE)

        self.undo_list = deque()

        # application's root control (i.e. "view") containing all other controls
        self.update_disp(False)
        return ft.Column(
            controls=[ 
                ft.Row([ft.Text("Compteur de points")]),
                ft.Row([self.points_labels, self.total_labels]),
                ft.Row([self.cur_exo_disp]),
                ft.ResponsiveRow([ft.Column(col={"xs": 4, "sm": 3, "md": 2, "xl": 1}, controls=[c]) for c in self.add_buttons]),
                ft.ResponsiveRow([ft.Column(col={"xs": 4, "sm": 3, "md": 2, "xl": 1}, controls=[c]) for c in self.rem_buttons]),
                ft.Row([
                    ft.FilledButton("Exo", expand=True, height=70, on_click=self.exo),
                    ft.FilledButton("Next", expand=True, height=70, on_click=self.suivant),
                    ft.FilledButton("Undo", expand=True, height=70, on_click=self.undo)
                ]),
                ft.Row([ft.Column([self.logs_disp], scroll=ft.ScrollMode.AUTO)])
            ])
    
    def save_for_undo(self):
        self.undo_list.appendleft(self.points.copy())
        if len(self.undo_list) > 100:
            self.undo_list.pop()

    def undo(self, e):
        if self.undo_list:
            self.points = self.undo_list.popleft()
            self.update_disp()
    
    def update_disp(self, update=True):
        self.cur_exo_disp.value = str(self.points[-1])
        self.points_labels.value = ", ".join([str(x) for x in self.points])
        self.total_labels.value = str(sum(self.points))
        self.logs_disp.value = self.logs_txt
        if update: self.update()
    
    def adder(self, x:float|int):
        def add(e):
            self.save_for_undo()
            self.points[-1] += x
            self.update_disp()
        
        return add
    
    
    def set_note(self, e):
        if self.cur_exo_disp.value:
            a = float(self.cur_exo_disp.value)
            self.save_for_undo()
            self.points[-1] = a
            self.update_disp()


    def exo(self, e):
        self.save_for_undo()
        self.points.append(0)
        self.update_disp()

    def suivant(self, e):
        self.save_for_undo()
        self.logs_txt = f"{sum(self.points)}: {self.points}\n" + self.logs_txt
        self.points = [0]
        self.update_disp()


def main(page: ft.Page):
    page.title = "Compteur de point"
    page.add(PointCounter())
    return

ft.app(target=main)

