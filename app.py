from flask import Flask, render_template, request, flash, url_for, redirect
import psycopg2 as psy


def ConnexionDB():
    try:

        connection = psy.connect(user="postgres", password="po",
                                 host="localhost",
                                 port="5432",
                                 database="flask"
                                 )
        return connection
    except (Exception) as error:
        print("Problème de connexion au serveur PostgreSQL", error)


connection = ConnexionDB()
curseur = connection.cursor()


app = Flask(__name__)  # permet de localiser les ressources cad les templates


@app.route('/')
def index():
    return render_template("index.html")


""" ************************ """
""" Apprenant """
""" ************************ """


@app.route('/ajout_apprenant')
def affiche_form_apprenant():
    curseur = connection.cursor()
    curseur.execute("select * from promotion ")
    x = curseur.fetchall()

    return render_template("ajout_apprenant.html", apprenant=x)


@app.route('/ajout_apprenant', methods=["POST", "GET"])
def ajouter_apprenant():
    if request.method == "POST":
        id_promo = request.form["promo"]
        prenom = request.form["firstname"]
        nom = request.form["lastname"]
        sex = request.form["sex"]
        mail = request.form["mail"]
        date_naiss = request.form["datenaissance"]

        curseur.execute("select max(id_app) from apprenant")
        x = curseur.fetchone()
        connection.commit()
        m = x[0] + 1
        matricule = "SA000"+str(m)

        ajouter_apprenant = "INSERT INTO apprenant (matricule,prenom,nom,sex,date_naiss, mail, id_promo, statut) VALUES (%s,%s,%s,%s,%s,%s,%s,'Inscrit')"

        curseur.execute(ajouter_apprenant, (matricule, prenom, nom, sex, date_naiss, mail, id_promo))

        connection.commit()

        return redirect(url_for('ajouter_apprenant'))


""" Liste des apprenants """


@app.route('/modifier_apprenant')
def lister_apprenant():
    curseur.execute("""select id_app,matricule, prenom, nom, sex, date_naiss, mail, promotion.nom_promo from apprenant, promotion
                         where apprenant.id_promo = promotion.id_promo order by 2 """)
    app = curseur.fetchall()
    connection.commit()
    curseur.execute(" select id_promo, nom_promo from promotion ")
    promo = curseur.fetchall()
    connection.commit()

    return render_template('modifier_apprenant.html', app=app, promo=promo)


""" Modifier apprenant """


@app.route('/modifier_apprenant', methods=["GET", "POST"])
def modifier_apprenant():
    if request.method == "POST":
        sex = request.form["sex"]
        mail = request.form["mail"]
        id_promo = request.form["promo"]
        id_app = request.form["id_app"]
        matricule = request.form["matricule"]
        prenom = request.form["firstname"]
        nom = request.form["lastname"]
        date_naiss = request.form["datenaissance"]

        modifier_app = "UPDATE apprenant SET matricule = %s, prenom = %s, nom = %s, sex = %s, date_naiss =%s, mail = %s, id_promo = %s WHERE id_app = %s"
        curseur.execute(modifier_app, (matricule, prenom, nom, sex, date_naiss, mail, id_promo, id_app))
        connection.commit()

        return redirect(url_for('lister_apprenant'))

""" Annuler Inscription """

@app.route('/annuler_inscription')
def lister_apprenant_():
    curseur.execute("""select id_app,matricule, prenom, nom, sex, date_naiss, mail, promotion.nom_promo from apprenant, promotion
                         where apprenant.id_promo = promotion.id_promo and statut in ('Inscrit', 'Suspendu') order by 2 """)
    _app_ = curseur.fetchall()
    connection.commit()
    """ curseur.execute(" select id_promo, nom_promo from promotion ")
    promo = curseur.fetchall()
    connection.commit() """

    return render_template('annuler_inscription.html', _app_=_app_)





@app.route('/annuler_inscription/<string:id_app>', methods=["GET", "POST"])
def annuler_inscription(id_app):
     curseur.execute("update apprenant set statut = 'Annulé' where id_app = %s", (id_app,))   
     connection.commit()

     return redirect(url_for('annuler_inscription'))

""" ************************************************************** """


""" Suspendre Inscription """

@app.route('/suspendre_inscription')
def _lister_apprenant_():
    curseur.execute("""select id_app,matricule, prenom, nom, sex, date_naiss, mail, promotion.nom_promo from apprenant, promotion
                         where apprenant.id_promo = promotion.id_promo and statut = ('Inscrit', 'Suspendu') order by 2 """)
    app_ = curseur.fetchall()
    connection.commit()
    
    return render_template('suspendre_inscription.html', app_=app_)





@app.route('/suspendre_inscription/<string:id_app>', methods=["GET", "POST"])
def suspendre_inscription(id_app):
     curseur.execute("update apprenant set statut = 'Suspendu' where id_app = %s", (id_app,))   
     connection.commit()

     return redirect(url_for('suspendre_inscription'))






""" ************************ """
""" Referentiel """
""" ************************ """
@app.route('/ajout_referentiel')
def afffche_form_ref():

    return render_template("ajout_referentiel.html")


@app.route('/ajout_referentiel', methods=["POST"])
def ajouter_referentiel():
    if request.method == "POST":
        nom = request.form["libelle"]
        ajouter_referentiel = "INSERT INTO referentiel (nom_ref) VALUES (%s)"
        curseur.execute(ajouter_referentiel, (nom,))
        connection.commit()

        return redirect(url_for('ajouter_referentiel'))


""" liste referentiels """
@app.route('/modifier_referentiel')
def lister_referentiel():
    curseur.execute(" select *  from referentiel ")
    liste = curseur.fetchall()
    connection.commit()
    return render_template('modifier_referentiel.html', data=liste)


""" modifier referentiel """


@app.route('/modifier_referentiel', methods=["POST"])
def modifier_referentiel():
    if request.method == "POST":
        id_ref = request.form["id_ref"]
        nom = request.form["libelle"]
        sql = "UPDATE referentiel SET  nom_ref = %s WHERE id_ref = %s"
        data = (nom, id_ref)
        curseur.execute(sql, data)
        connection.commit()

        return redirect(url_for('modifier_referentiel'))


""" ************************ """
""" Promo """
""" ************************ """
@app.route('/ajout_promo')
def affiche_form_promo():
    connection = ConnexionDB()
    curseur = connection.cursor()
    curseur.execute("select * from referentiel ")
    y = curseur.fetchall()
    return render_template("ajout_promo.html", ref=y)


@app.route('/ajout_promo', methods=["POST"])
def ajouter_promo():
    if request.method == "POST":
        ref = request.form["referentiel"]
        nom = request.form["nom"]
        debut = request.form["datedebut"]
        fin = request.form["datefin"]
        ajouter_promo = "INSERT INTO promotion (nom_promo, date_debut, date_fin, id_ref) VALUES (%s,%s,%s,%s)"
        curseur.execute(ajouter_promo, (nom, debut, fin, ref))
        connection.commit()
        return redirect(url_for('ajouter_promo'))


""" liste promo """
@app.route('/modifier_promo')
def lister_promo():
    curseur.execute("""select id_promo, nom_promo, date_debut, date_fin, referentiel.nom_ref from promotion, referentiel
                         where promotion.id_ref = referentiel.id_ref order by referentiel.nom_ref""")
    promo = curseur.fetchall()
    connection.commit()
    curseur.execute(" select id_ref, nom_ref from referentiel ")
    ref = curseur.fetchall()
    connection.commit()

    return render_template('modifier_promo.html', promo=promo, ref=ref)


""" modifier promo """


@app.route('/modifier_promo', methods=["POST", "GET"])
def modifier_promo():

    if request.method == "POST":
        id_promo = request.form["id_promo"]
        ref = request.form["referentiel"]
        nom = request.form["nom"]
        debut = request.form["datedebut"]
        fin = request.form["datefin"]
        modif_promo = "UPDATE promotion SET nom_promo = %s, date_debut = %s, date_fin = %s, id_ref = %s where id_promo = %s"
        curseur.execute(modif_promo, (nom, debut, fin, ref, id_promo))
        connection.commit()

        return redirect(url_for('lister_promo'))


if __name__ == '__main__':  # si le fichier est executer alors execute le bloc
    app.run(debug=True)  # debug=True relance le serveur à chaque modification
