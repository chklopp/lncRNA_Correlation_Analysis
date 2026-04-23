import seaborn as sns
from Bio.Align import PairwiseAligner
import numpy as np
import pandas as pd

BUTTON_NAME = "Read pairs distances"


def get_current_group_seqs(fasta_data, ref_entry):
    print(fasta_data[ref_entry])
    if ref_entry not in fasta_data:
        messagebox.showerror("Erreur", f"Le groupe '{ref}' est introuvable dans le FASTA.")
        return None
    return fasta_data[ref_entry]


def dist_seq(fasta):
    if not fasta: return
    n = len(fasta)
    aligner = PairwiseAligner(mode='local')
    matrix = np.zeros((n, n))
    ids = [s.id for s in fasta]

    for i in range(n):
        for j in range(i, n):
            score = aligner.score(fasta[i].seq, fasta[j].seq)
            max_s = max(aligner.score(fasta[i].seq, fasta[i].seq), aligner.score(fasta[j].seq, fasta[j].seq))
            dist = 1 - (score/max_s)
            matrix[i,j] = matrix[j,i] = dist
    return pd.DataFrame(matrix, index=ids, columns=ids)

def generate_plot(figure, fasta, gtf, expr, orthogroup):
    # 1. Vérifier si des données sont chargées
    if not fasta:
        raise ValueError("Aucune donnée chargée. Cliquez sur 'Charger Données'.")

    # 2. Récupérer le premier DataFrame disponible (ou un nom spécifique)
    # Ici, on prend le premier fichier chargé
    # first_key = list(expr.keys())[0]
    # df = expr[first_key]

    # 3. Générer le graphique
    #ref = figure.ref_entry.get()
    ax = figure.add_subplot(111)
    
    matrix = dist_seq(get_current_group_seqs(fasta, orthogroup))
    print(matrix)
    # On suppose que le fichier est une matrice de distance
    # On utilise sns.heatmap directement sur la figure passée
    sns.heatmap(matrix, ax=ax, cmap="YlGnBu")
    #sns.clustermap(matrix)
    figure.tight_layout()
    ax.set_title(f"Analyse de : {orthogroup}")
    ax.tick_params(axis='x', rotation=90)
    #ax.tick_params(axis='y', rotation=90)
    #ax.xticks(rotation=90)
    #ax.yticks(rotation=90)