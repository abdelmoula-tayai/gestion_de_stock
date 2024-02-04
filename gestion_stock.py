import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import csv
from matplotlib import pyplot as plt

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="store"
)

def afficher_produits():
    cursor.execute("SELECT * FROM product")
    produits = cursor.fetchall()

    for row in tableau_produits.get_children():
        tableau_produits.delete(row)

    for produit in produits:
        tableau_produits.insert("", "end", values=produit)

def ajouter_produit():
    afficher_produits()

def supprimer_produit():
    selected_item = tableau_produits.selection()
    if selected_item:
        afficher_produits()
    else:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à supprimer.")

def modifier_produit():
    selected_item = tableau_produits.selection()
    if selected_item:
        afficher_produits()
    else:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à modifier.")

def exporter_csv():
    cursor.execute("SELECT * FROM product")
    produits = cursor.fetchall()

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nom", "Description", "Prix", "Quantité", "ID Catégorie"])
        writer.writerows(produits)

def afficher_graphique():
    cursor.execute("""
        SELECT c.name, COUNT(p.id_category) as count
        FROM category c
        LEFT JOIN product p ON c.id = p.id_category
        GROUP BY c.name
    """)
    result = cursor.fetchall()

    categories = [row[0] for row in result]
    counts = [row[1] for row in result]
    
    plt.bar(categories, counts)
    plt.xlabel('Catégorie')
    plt.ylabel('Nombre de Produits')
    plt.title('Répartition des Produits par Catégorie')
    plt.show()

fenetre = tk.Tk()
fenetre.title("Gestion de Stock")

colonnes = ("ID", "Nom", "Description", "Prix", "Quantité", "ID Catégorie")
tableau_produits = ttk.Treeview(fenetre, columns=colonnes, show="headings")

for col in colonnes:
    tableau_produits.heading(col, text=col)
    tableau_produits.column(col, width=100)

btn_ajouter = tk.Button(fenetre, text="Ajouter", command=ajouter_produit)
btn_supprimer = tk.Button(fenetre, text="Supprimer", command=supprimer_produit)
btn_modifier = tk.Button(fenetre, text="Modifier", command=modifier_produit)
btn_exporter_csv = tk.Button(fenetre, text="Exporter CSV", command=exporter_csv)
btn_afficher_graphique = tk.Button(fenetre, text="Afficher Graphique", command=afficher_graphique)

tableau_produits.grid(row=0, column=0, columnspan=3)
btn_ajouter.grid(row=1, column=0)
btn_supprimer.grid(row=1, column=1)
btn_modifier.grid(row=1, column=2)
btn_exporter_csv.grid(row=2, column=0)
btn_afficher_graphique.grid(row=2, column=1)

cursor = conn.cursor()

fenetre.mainloop()

conn.close()
