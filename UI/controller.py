import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []
        self.forma = None
        self.anno = None


    def fillDDAnno(self):
        anni = self._model.fillDDAnno()
        anniDD = list(map(lambda x: ft.dropdown.Option(text=x, on_click=self.getAnno), anni))
        self._view.ddyear.options = anniDD
        self._view.update_page()


    def fillDDForme(self, anno):
        forme = self._model.fillDDForme(anno)
        formeDD = list(map(lambda x: ft.dropdown.Option(text=x, on_click=self.getForma), forme))
        self._view.ddshape.options = formeDD
        self._view.update_page()
    def handle_graph(self, e):
        if self.forma is None:
            self._view.create_alert("Forma non inserita")
            return
        if self.anno is None:
            self._view.create_alert("Anno non inserita")
            return
        self._model.buildGraph(self.forma, int(self.anno))
        n,e = self._model.graphDetails()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {n} nodi e {e} archi"))
        result = self._model.getPesi()
        for i in result:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {i}, somma pesi sugli archi: {result[i]}"))
        self._view.update_page()


    def handle_path(self, e):
        lunghezza, solBest = self._model.getPercorso()
        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Cammino con distanza {lunghezza}"))
        for i in range(len(solBest)-1):
            self._view.txtOut2.controls.append(ft.Text(f"{solBest[i]} --> {solBest[i+1]} peso: {self._model.grafo[solBest[i]][solBest[i+1]]["weight"]}"
                                                       f" distanza: {self._model.calcolaDistanza((solBest[i], solBest[i+1]))}"))
        self._view.update_page()

    def getAnno(self, e):
        if e.control.text is None:
            pass
        else:
            self.anno = e.control.text
            self.fillDDForme(self.anno)

    def getForma(self, e):
        if e.control.text is None:
            pass
        else:
            self.forma = e.control.text