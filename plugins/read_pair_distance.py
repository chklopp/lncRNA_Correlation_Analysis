import seaborn as sns

BUTTON_NAME = "Read pairs distances"

def extract_tag(figure, text):
    match = re.search(r'REF=([^;\s\n]+)', text)
    return match.group(1) if match else "Unknown"

# --- Fonctions de calcul ---
def get_current_group_seqs(figure):
    ref = figure.ref_entry.get()
    if ref not in figure.fasta_data:
        messagebox.showerror("Erreur", f"Le groupe '{ref}' est introuvable dans le FASTA.")
        return None
    return figure.fasta_data[ref]


def generate_plot(figure, fasta, gtf, expr):
    # 1. Vérifier si des données sont chargées
    if not expr:
        raise ValueError("Aucune donnée chargée. Cliquez sur 'Charger Données'.")

    # 2. Récupérer le premier DataFrame disponible (ou un nom spécifique)
    # Ici, on prend le premier fichier chargé
    first_key = list(expr.keys())[0]
    df = expr[first_key]

    # 3. Générer le graphique
    ax = figure.add_subplot(111)
    
    # On suppose que le fichier est une matrice de distance
    # On utilise sns.heatmap directement sur la figure passée
    sns.heatmap(df.set_index(df.columns[0]), ax=ax, cmap="YlGnBu")
    ax.set_title(f"Analyse de : {first_key}")