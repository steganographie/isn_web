from flask import Flask, jsonify, render_template, request

import shutil
from PIL import Image  # Depuis le module PIL, importer image, permet d'effectuer des actions sur des images
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/SomeFunction')
def SomeFunction():
    nom_image = input("Entrez le chemin de l'image avec son nom et format : ")
    img = Image.open(nom_image)
    l, h = img.size
    r, g, b = img.split()
    red = list(r.getdata())
    green = list(g.getdata())
    blue = list(b.getdata())
    red_sum = sum(red)
    green_sum = sum(green)
    blue_sum = sum(blue)
    taille = [red_sum, green_sum, blue_sum]
    taille.sort(reverse=False)
    if taille[0] == red_sum:
        couleur_acc = list(r.getdata())
        print("Couleur la moins presente : rouge")
    if taille[0] == green_sum:
        couleur_acc = list(g.getdata())
        print("Couleur la moins presente : vert")
    if taille[0] == blue_sum:
        couleur_acc = list(b.getdata())
        print("Couleur la moins presente : bleu")
    c = input("Entrez le texte qui sera encode dans l'image : ")
    u = len(c)
    v = bin(u)[2:].rjust(8, "0")
    ascii = [bin(ord(i))[2:].rjust(8, "0") for i in c]
    a = ''.join(ascii)
    for j in range(8):
        couleur_acc[j] = 2 * int(couleur_acc[j] // 2) + int(v[j])
    for k in range(8 * u):
        couleur_acc[k + 8] = 2 * int(couleur_acc[k + 8] // 2) + int(a[k])
    couleur_modifiee = Image.new("L", (l, h))
    couleur_modifiee.putdata(couleur_acc)
    if taille[0] == red_sum:
        imgnew = Image.merge('RGB', (couleur_modifiee, g, b))
    if taille[0] == green_sum:
        imgnew = Image.merge('RGB', (r, couleur_modifiee, b))
    if taille[0] == blue_sum:
        imgnew = Image.merge('RGB', (r, g, couleur_modifiee))
    nom_repertoire = input("Entrez le repertoire dans lequel vous souhaitez enregistrer l'image : ")
    imgnew.save("image_avec_message_code.png")
    shutil.copy2("image_avec_message_codé.png", nom_repertoire)
    os.remove("image_avec_message_codé.png")


if __name__ == '__main__':
    app.run(debug=True)
