import tkinter as tk
from tkinter import messagebox
import os
import importlib.util
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import filedialog, messagebox
# ... (autres imports identiques au script précédent)

class DynamicPlotterApp:
    def __init__(self, root, plugins_dir):
        self.root = root
        self.plugins_dir = plugins_dir
        
        # Le "cerveau" des données : un dictionnaire accessible par tous
        self.expr = {}
        self.fasta = {}
        self.gtf = {}

        # --- Sidebar ---
        self.sidebar = tk.Frame(self.root, width=200, bg='lightgrey', padx=10, pady=10)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Bouton pour charger le fasta
        self.load_btn1 = tk.Button(self.sidebar, text="📁 Charger Fasta", 
                                  command=self.open_fasta_file, bg="gold")
        self.load_btn1.pack(pady=20, fill=tk.X)

        # Bouton pour charger le gtf
        self.load_btn2 = tk.Button(self.sidebar, text="📁 Charger GTF", 
                                  command=self.open_gtf_file, bg="gold")
        self.load_btn2.pack(pady=20, fill=tk.X)

        # Bouton pour charger le fichier d'expression
        self.load_btn3 = tk.Button(self.sidebar, text="📁 Charger Expressions", 
                                  command=self.open_expr_file, bg="gold")
        self.load_btn3.pack(pady=20, fill=tk.X)

        # 2. Colonne de droite : Zone graphique 
        self.plot_frame = tk.Frame(self.root, bg='white')
        self.plot_frame.grid(row=0, column=1, sticky="nsew")

        # --- Zone Graphique ---        
        # Initialisation de la figure Matplotlib
        self.fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 3. Chargement dynamique des boutons        
        self.load_plugins()

    def open_fasta_file(self):
        """Charge un fichier et le stocke dans data_store."""
        file_path = filedialog.askopenfilename(title="Sélectionner le fichier fasta des lncRNA")
        if path:
            self.fasta_data = {}
            for rec in SeqIO.parse(path, "fasta"):
                ref = self.extract_tag(rec.description)
                if ref not in self.fasta_data: self.fasta_data[ref] = []
                self.fasta_data[ref].append(rec)
            messagebox.showinfo("Succès", f"FASTA chargé : {len(self.fasta_data)} groupes REF trouvés.")

    def open_gtf_file(self):
        """Charge un fichier et le stocke dans data_store."""
        file_path = filedialog.askopenfilename(title="Sélectionner le fichier gtf des lncRNA")
        if path:
            self.gtf_data = {}
            with open(path, 'r') as f:
                for line in f:
                    if line.startswith("#") or "\texon\t" not in line: continue
                    ref = self.extract_tag(line)
                    tid = re.search(r'transcript_id "([^"]+)"', line).group(1)
                    cols = line.split('\t')
                    start, end = int(cols[3]), int(cols[4])
                    
                    if ref not in self.gtf_data: self.gtf_data[ref] = {}
                    if tid not in self.gtf_data[ref]: self.gtf_data[ref][tid] = []
                    self.gtf_data[ref][tid].append((start, end))
            messagebox.showinfo("Succès", f"GTF chargé : {len(self.gtf_data)} groupes REF trouvés.")

    def open_expr_file(self):
        """Charge un fichier et le stocke dans data_store."""
        file_path = filedialog.askopenfilename(title="Sélectionner le fichier gtf des lncRNA")
        if file_path:
            try:
                # Exemple : on charge un fichier TSV avec Pandas
                import pandas as pd
                name = os.path.basename(file_path)
                self.expr[name] = pd.read_csv(file_path, sep='\t')
                messagebox.showinfo("Succès", f"Fichier '{name}' chargé !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier :\n{e}")

    def run_analysis(self, plot_func):
        self.fig.clear()
        try:
            # ON PASSE LE DATA_STORE AU PLUGIN ICI
            plot_func(self.fig, self.fasta, self.gtf, self.expr)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Erreur", f"Analyse impossible : {e}")

    # ... (le reste de la méthode load_plugins reste identique)

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

    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    # Nom du dossier contenant vos scripts d'analyse
    app = DynamicPlotterApp(root, plugins_dir="plugins")
    root.mainloop()
