from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #VANG

#@app.route("/contact/")
#def MaPremiereAPI():
 #   return "<h2>Ma page de contact</h2>"

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histo.html")

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

# --- EXERCICE 6 : API DE DONNÉES GITHUB ---
@app.route('/commits-data/')
def commits_data():
    # ⚠️ IMPORTANT : Remplace ci-dessous par ton pseudo et le nom de ton repo
    # Exemple : 'https://api.github.com/repos/TonyVang/MetsTonNomDeRepoIci/commits'
    url = 'https://api.github.com/repos/{TonyESGI}/{5MCSI_Metriques}/commits'
    
    try:
        response = urlopen(url)
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        
        # Dictionnaire pour compter : { "minute": nombre_de_commits }
        compteur_minutes = {}
        
        for commit in json_content:
            date_string = commit['commit']['author']['date']
            # On utilise l'indice fourni pour transformer le texte en objet Date
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.minute
            
            # On incrémente le compteur pour cette minute
            if minute in compteur_minutes:
                compteur_minutes[minute] += 1
            else:
                compteur_minutes[minute] = 1
        
        # On formate les résultats pour le graphique (liste triée)
        results = []
        for minute, nombre in sorted(compteur_minutes.items()):
            results.append({'minute': minute, 'count': nombre})
            
        return jsonify(results=results)
        
    except Exception as e:
        # En cas d'erreur (repo introuvable, privé, etc.)
        return jsonify({'error': str(e)})

# --- EXERCICE 6 : LA PAGE D'AFFICHAGE ---
@app.route('/commits/')
def graph_commits():
    return render_template("commits.html")

if __name__ == "__main__":
  app.run(debug=True)
