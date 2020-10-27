from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('127.0.0.1', port=9200)


#index
@app.route('/')
def index():
    return render_template('index.html')


#route de la requete 
@app.route('/search', methods=['GET', 'POST'])
def search():
    search_term = request.form["input"]
    res = es.search(
        index="flickrphotos", 
        size=20, 
        body={
            
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "title", 
                        "tags"
                    ],
                    "fuzziness" : "AUTO",
                    "prefix_length" : 1
                    
                }
            }
        }
    )
    return render_template('recherche.html', res=res )


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000)