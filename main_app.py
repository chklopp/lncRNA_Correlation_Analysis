import tkinter as tk
from tkinter import messagebox
import os
import importlib.util
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DynamicPlotterApp:
    def __init__(self, root, plugins_dir):
        self.root = root
        self.root.title("Analyseur Dynamique de Génomes")
        self.plugins_dir = plugins_dir
        
        # Configuration de la mise en page (Grid)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # 1. Colonne de gauche : Menu des boutons
        self.sidebar = tk.Frame(self.root, width=200, bg='lightgrey', padx=10, pady=10)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        tk.Label(self.sidebar, text="Analyses", bg='lightgrey', font=('Arial', 12, 'bold')).pack(pady=10)

        # 2. Colonne de droite : Zone graphique
        self.plot_frame = tk.Frame(self.root, bg='white')
        self.plot_frame.grid(row=0, column=1, sticky="nsew")
        
        # Initialisation de la figure Matplotlib
        self.fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 3. Chargement dynamique des boutons
        self.load_plugins()

    def load_plugins(self):
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
            messagebox.showinfo("Info", f"Dossier '{self.plugins_dir}' créé. Ajoutez des scripts dedans.")
            return

        for filename in os.listdir(self.plugins_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                path = os.path.join(self.plugins_dir, filename)
                self.create_plugin_button(path, filename)

    def create_plugin_button(self, path, filename):
        try:
            # Importation dynamique du module
            spec = importlib.util.spec_from_file_location(filename, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Création du bouton avec le nom défini dans le module
            btn_text = getattr(module, "BUTTON_NAME", filename)
            plot_func = getattr(module, "generate_plot", None)

            if plot_func:
                btn = tk.Button(self.sidebar, text=btn_text, 
                                command=lambda: self.run_analysis(plot_func),
                                width=20)
                btn.pack(pady=5)
        except Exception as e:
            print(f"Erreur lors du chargement de {filename}: {e}")

    def run_analysis(self, plot_func):
        # Effacer la figure précédente
        self.fig.clear()
        
        # Exécuter la fonction de tracé du module
        try:
            plot_func(self.fig)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Erreur de calcul", f"Le script a échoué :\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    # Nom du dossier contenant vos scripts d'analyse
    app = DynamicPlotterApp(root, plugins_dir="plugins")
    root.mainloop()
