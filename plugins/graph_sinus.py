import seaborn as sns
from Bio.Align import PairwiseAligner
import numpy as np
import pandas as pd

BUTTON_NAME = "Multi alignment distance"


def get_current_group_seqs(fasta_data, ref_entry):
    print(fasta_data[ref_entry])
    if ref_entry not in fasta_data:
        messagebox.showerror("Erreur", f"Le groupe '{ref}' est introuvable dans le FASTA.")
        return None
    return fasta_data[ref_entry]


def dist_msa(fasta):
    # Note: Simulation d'une matrice MSA (nécessite normalement un outil externe)
    #messagebox.showinfo("Info", "Calcul MSA simulé (utilise l'alignement global Biopython).")
    if not fasta: return
    n = len(fasta)
    aligner = PairwiseAligner(mode='global')
    matrix = np.zeros((n, n))
    ids = [s.id for s in fasta]

    for i in range(n):
        for j in range(i, n):
            score = aligner.score(fasta[i].seq, fasta[j].seq)
            matrix[i,j] = matrix[j,i] = 1 - (score / max(len(fasta[i]), len(fasta[j])))
    return pd.DataFrame(matrix, index=ids, columns=ids)
    #self.plot_matrix(pd.DataFrame(matrix, index=[s.id for s in fasta]), "Distance MSA")

def generate_plot(figure, fasta, gtf, expr, orthogroup):
    # 1. Vérifier si des données sont chargées
    if not fasta:
        raise ValueError("Aucune donnée chargée. Cliquez sur 'Charger Données'.")

    #ref = figure.ref_entry.get()
    ax = figure.add_subplot(111)
    
    matrix = dist_msa(get_current_group_seqs(fasta, orthogroup))
    print(matrix)

    if matrix.isnull().values.any():
        print("Warning: NaN détectés. Remplacement par 0.")
        matrix = matrix.fillna(0)

    cmap="viridis"
    z_score=None

    # On suppose que le fichier est une matrice de distance
    # On utilise sns.heatmap directement sur la figure passée
    sns.clustermap(1 - matrix, 
        cmap=cmap, 
        standard_scale=z_score, # Normalise entre 0 et 1 si besoin
        method='ward',          # Méthode de clustering robuste
        metric='euclidean', 
        figsize=(10, 8),
        annot=False             # Mettre à True pour afficher les valeurs
    )
    #sns.clustermap(matrix)
    figure.tight_layout()
    ax.set_title(f"Analyse de : {orthogroup}")
    ax.tick_params(axis='x', rotation=90)
