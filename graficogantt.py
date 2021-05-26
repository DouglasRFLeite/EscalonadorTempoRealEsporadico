# coding: utf-8

from matplotlib import pyplot, cm

#classe que lida com a visualização do diagrama de gantt
#essa classe lida puramente com interface gráfica
#não possui funcionalidade de escalonamento
class GraficoGantt:

    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.x0 = None
        self.x1 = None
        self.xpress = None

    def zoom_factory(self, ax, base_scale, grid):
        def zoom(event):
            cur_xlim = ax.get_xlim()

            xdata = event.xdata

            if event.button == 'up':
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                scale_factor = base_scale
            else:
                scale_factor = 1
                print(event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])

            xlim_min = xdata - new_width * (1-relx)
            if xlim_min < grid[0]:
                xlim_min = grid[0]
            xlim_max = xdata + new_width * (relx)
            if xlim_max > grid[-1]:
                xlim_max = grid[-1]
            if xlim_max - xlim_min < 1:
                xlim_min = int(xlim_min)
                xlim_max = xlim_min+1
            ax.set_xlim([xlim_min, xlim_max])
            ax.figure.canvas.draw()

        fig = ax.get_figure()
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax, grid):
        def onPress(event):
            if event.inaxes != ax: 
                return
            self.cur_xlim = ax.get_xlim()
            self.press = self.x0, event.xdata
            self.x0, self.xpress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: 
                return
            if event.inaxes != ax: 
                return
            dx = event.xdata - self.xpress
            if dx > self.cur_xlim[0]:
                dx = self.cur_xlim[0]
            if dx < self.cur_xlim[1] - grid[-1]:
                dx = self.cur_xlim[1] - grid[-1]
            self.cur_xlim -= dx
            ax.set_xlim(self.cur_xlim)

            ax.figure.canvas.draw()

        fig = ax.get_figure()

        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        return onMotion

    def gerarGantt(self, tasks, limite, escalonador):
        cmap = cm.get_cmap('plasma')
        fig, gantt = pyplot.subplots()
        if escalonador == 1:
            gantt.set_title('Escalonamento Rate Monotonic')
            fig.canvas.set_window_title('Escalonamento Rate Monotonic')
        else:
            gantt.set_title('Escalonamento Earliest Deadline First')
            fig.canvas.set_window_title('Escalonamento Earliest Deadline First')
        gantt.set_ylim(0, len(tasks)-1)
        gantt.set_xlim(0, limite)
        gantt.set_xlabel('Tempo')
        #gantt.set_ylabel('Tarefas')
        gantt.set_yticks(range(1, len(tasks)))
        gantt.set_yticks([i-0.5 for i in range(1, len(tasks))], minor=True)
        #gantt.set_yticklabels(map(lambda x: str(x), reversed(range(1, len(tasks)))))
        gantt.set_yticklabels(['' for _ in range(1, len(tasks))])
        gantt.set_yticklabels(['Tarefa '+str(i) for i in reversed(range(1, len(tasks)))], minor=True)
        gantt.grid(True)
        color = 0.9
        color_inc = 0
        if len(tasks) > 2:
            color_inc = -0.8/(len(tasks)-2)
        verticais = []
        for task in tasks:
            verticais.extend(task.execucoes)
            if task.id != 0:
                gantt.broken_barh(task.execucoes, ((len(tasks)-1)-task.id, 1), facecolors=cmap(color))
                color += color_inc
        verticais = list(map(lambda x: x[0], verticais)) + [limite]
        verticais = sorted(list(set(verticais)))
        gantt.set_xticks(verticais)

        figZoom = self.zoom_factory(gantt, 1.2, verticais)
        figPan = self.pan_factory(gantt, verticais)

        pyplot.show()
