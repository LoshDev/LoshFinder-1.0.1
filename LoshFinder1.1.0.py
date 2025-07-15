import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk
import time
import json
import csv

#CLASSE POO
class ApplicationRecherche:
    #FENETRE/TITRE TKINTER
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("LoshFinder  V 1.1.0")
        self.racine.minsize(900, 550)
        self.configurer_theme_sombre()
        self.creer_widgets()
        self.configurer_grille()
    #THEME SOMBRE
    def configurer_theme_sombre(self):
        self.couleur_fond = "#1e1e1e"
        self.couleur_texte = "#ffffff"
        self.couleur_accent = "#fdd835"
        self.entree_fond = "#2e2e2e"
        self.entree_bordure = "#3c3c3c"

        self.racine.configure(bg=self.couleur_fond)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TButton",
                             background=self.entree_fond,
                             foreground=self.couleur_texte,
                             padding=6,
                             relief="flat")
        self.style.map("TButton",
                       background=[("active", "#3c3c3c")])

        self.style.configure("TLabel",
                             background=self.couleur_fond,
                             foreground=self.couleur_texte)

        self.style.configure("TEntry",
                             fieldbackground=self.entree_fond,
                             foreground=self.couleur_texte)

        self.style.configure("TListbox",
                             background=self.entree_fond,
                             foreground=self.couleur_texte)
    #GRILLE POUR LES BOUTON ET LES INPUTSS
    def configurer_grille(self):
        self.racine.grid_rowconfigure(2, weight=1)
        self.racine.grid_columnconfigure(1, weight=1)
        self.racine.grid_columnconfigure(2, weight=1)

    #BOUTON/INPUTS 
    def creer_widgets(self):
        self.label_dossier = ttk.Label(self.racine, text="Dossier :")
        self.label_dossier.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entree_dossier = ttk.Entry(self.racine, width=60)
        self.entree_dossier.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        self.bouton_parcourir = ttk.Button(self.racine, text="Parcourir", command=self.parcourir_dossier)
        self.bouton_parcourir.grid(row=0, column=2, padx=10, pady=10)

        self.label_recherche = ttk.Label(self.racine, text="Rechercher :")
        self.label_recherche.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entree_recherche = ttk.Entry(self.racine, width=60)
        self.entree_recherche.grid(row=1, column=1, padx=10, pady=10, sticky="we")

        self.bouton_rechercher = ttk.Button(self.racine, text="Rechercher", command=self.lancer_recherche)
        self.bouton_rechercher.grid(row=1, column=2, padx=10, pady=10)

        self.liste_fichiers = tk.Listbox(self.racine, width=40, height=20, bg=self.entree_fond,
                                         fg=self.couleur_texte, bd=1, relief=tk.FLAT,
                                         highlightthickness=1, highlightbackground=self.entree_bordure)
        self.liste_fichiers.grid(row=2, column=0, padx=(10, 5), pady=10, sticky="ns")
        self.liste_fichiers.bind("<<ListboxSelect>>", self.selection_fichier)

        self.texte_resultats = scrolledtext.ScrolledText(self.racine, width=80, height=20, bg=self.entree_fond,
                                                         fg=self.couleur_texte, insertbackground=self.couleur_texte,
                                                         relief=tk.FLAT, wrap=tk.WORD, borderwidth=1)
        self.texte_resultats.grid(row=2, column=1, columnspan=2, padx=(5, 10), pady=(10, 5), sticky="nsew")
        self.texte_resultats.tag_config('highlight', background=self.couleur_accent, foreground="#000000")

        self.label_stats = ttk.Label(self.racine, text="")
        self.label_stats.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

        self.bouton_exporter = ttk.Button(self.racine, text="Exporter", command=self.exporter_resultats)
        self.bouton_exporter.grid(row=3, column=2, padx=10, pady=(0, 10), sticky="e")
    #FONCTION RECHERCHE DU DOSSIER
    def parcourir_dossier(self):
        dossier = filedialog.askdirectory()
        if dossier:
            self.entree_dossier.delete(0, tk.END)
            self.entree_dossier.insert(0, dossier)
    #FONCTION RECHERCHE DANS DOSSIER
    def lancer_recherche(self):
        dossier = self.entree_dossier.get()
        recherche = self.entree_recherche.get()

        if not dossier or not recherche:
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier et entrer une recherche.")
            return

        self.texte_resultats.delete(1.0, tk.END)
        self.supprimer_surbrillance()
        self.label_stats.config(text="")

        self.texte_resultats.insert(tk.END, "Recherche en cours...\n")
        self.racine.update()

        Thread(target=self.recherche_fichiers_parallel, args=(dossier, recherche)).start()
    #STAZTISTIQUES 
    def recherche_fichiers_parallel(self, dossier, recherche):
        self.resultats = {}
        nb_fichiers = 0
        lignes_trouvees = 0
        debut = time.time()

        tous_les_fichiers = []
        for racine, _, fichiers in os.walk(dossier):
            for fichier in fichiers:
                if fichier.endswith(".txt"):
                    tous_les_fichiers.append(os.path.join(racine, fichier))
        #lectture plus simple
        def chercher_dans_fichier(chemin):
            lignes = []
            try:
                with open(chemin, "r", encoding='utf-8') as f:
                    for ligne in f:
                        if recherche.lower() in ligne.lower():
                            formaté = ' | '.join(part for part in ligne.strip().split(',') if part and part.lower() not in ('<blank>', 'null'))
                            lignes.append(formaté)
            except UnicodeDecodeError:
                pass
            return os.path.basename(chemin), lignes

        with ThreadPoolExecutor(max_workers=20) as executeur:
            for fichier, lignes in executeur.map(chercher_dans_fichier, tous_les_fichiers):
                if lignes:
                    self.resultats[fichier] = lignes
                    lignes_trouvees += len(lignes)
                nb_fichiers += 1

        temps = time.time() - debut

        self.texte_resultats.delete(1.0, tk.END)

        if not self.resultats:
            self.texte_resultats.insert(tk.END, "Aucun résultat trouvé.\n")
        else:
            self.liste_fichiers.delete(0, tk.END)
            self.liste_fichiers.insert(tk.END, "Tout")
            for fichier in self.resultats:
                self.liste_fichiers.insert(tk.END, fichier)
            self.texte_resultats.insert(tk.END, f"Recherche terminée. {len(self.resultats)} fichiers avec résultats.\n")

        self.label_stats.config(text=f"Fichiers analysés : {nb_fichiers} | Fichiers trouvés : {len(self.resultats)} | Lignes trouvées : {lignes_trouvees} | Temps : {temps:.2f}s")
        self.racine.update()
        self.afficher_resultats("Tout")
    #afficher les resultat dans la box
    def afficher_resultats(self, fichier_cle):
        self.texte_resultats.delete(1.0, tk.END)
        if fichier_cle == "Tout":
            for fichier in self.resultats:
                for ligne in self.resultats[fichier]:
                    self.texte_resultats.insert(tk.END, f"{ligne}\n")
        else:
            for ligne in self.resultats[fichier_cle]:
                self.texte_resultats.insert(tk.END, f"{ligne}\n")
        self.appliquer_surbrillance(self.entree_recherche.get())
    #EXPORT BOUTON 
    def exporter_resultats(self):
        if not self.texte_resultats.get(1.0, tk.END).strip():
            messagebox.showinfo("Info", "Aucun résultat à exporter.")
            return

        chemin = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Fichier texte", "*.txt"),
                ("Fichier CSV", "*.csv"),
                ("Fichier JSON", "*.json")
            ]
        )
        if not chemin:
            return

        try:
            if chemin.endswith(".txt"):
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write(self.texte_resultats.get(1.0, tk.END))

            elif chemin.endswith(".csv"):
                with open(chemin, "w", encoding="utf-8", newline='') as f:
                    writer = csv.writer(f)
                    for fichier, lignes in self.resultats.items():
                        for ligne in lignes:
                            writer.writerow([fichier, ligne])

            elif chemin.endswith(".json"):
                with open(chemin, "w", encoding="utf-8") as f:
                    json.dump(self.resultats, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("Succès", "Résultats exportés avec succès !")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export : {e}")

    def appliquer_surbrillance(self, recherche):
        debut = "1.0"
        while True:
            debut = self.texte_resultats.search(recherche, debut, tk.END, nocase=1)
            if not debut:
                break
            fin = f"{debut}+{len(recherche)}c"
            self.texte_resultats.tag_add('highlight', debut, fin)
            debut = fin

    def supprimer_surbrillance(self):
        self.texte_resultats.tag_remove('highlight', '1.0', tk.END)
#SELEC FICHIER A GAUCHE BOX (.txt, .csv, etcc)
    def selection_fichier(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            fichier_cle = event.widget.get(index)
            self.afficher_resultats(fichier_cle)
#START
if __name__ == "__main__":
    racine = tk.Tk()
    app = ApplicationRecherche(racine)
    racine.mainloop()
