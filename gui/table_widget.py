import tkinter as gui

# http://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter
class TableWidget(gui.Frame):
    def __init__(self, parent):
        # use black background so it "peeks through" to
        # form grid lines
        gui.Frame.__init__(self, parent, background="black")

    def set_rows(self, rows):
        non_widget_col = 5
        self._widgets = []
        ii = 0
        jj = 0
        for row in rows:
            current_row = []
            for column in row:
                if jj < non_widget_col:
                    if ii > 0:
                        column.config(borderwidth=0)
                        column.grid(row=ii, column=jj, sticky="nsew", padx=1, pady=1)
                        current_row.append(column)
                    else:
                        label = gui.Label(self, text=column, borderwidth=0, width=10)
                        label.grid(row=ii, column=jj, sticky="nsew", padx=1, pady=1)
                        current_row.append(column)
                jj += 1
            jj = 0
            ii += 1
            self._widgets.append(current_row)

        for column in range(0, non_widget_col):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)