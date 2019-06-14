from flask import Flask
from SPARQLWrapper import SPARQLWrapper, JSON
import os
from dotenv import load_dotenv
from flask import request
from flask import abort


app = Flask(__name__)
load_dotenv()

# Set Up SPARQL Connection
sparql = SPARQLWrapper(os.getenv('SPARQL_ENDPOINT'))
sparql.setReturnFormat(JSON)
sparql.addDefaultGraph('http://localhost:8890/reach-it')

@app.route('/productcategory/', methods=['GET'])
def get_product_category():
    product_name = request.args.get('product_name')
    print(product_name)
    """Get category of product given product name.
    Args:
        product_name (str): The product name. It should be url encoded, for example "Charcoal, sack" -> Charcoal%2C%20sack

    Returns:
        str: The category of queried product name.
    """
    q = ( f"""
    PREFIX reachIT: <http://www.reach-it.com/ontology/>
    SELECT str(?c) as ?type
        WHERE {{
                ?product reachIT:productName ?productName.
                ?product reachIT:belongsToCategory ?t.
                ?t reachIT:categoryName ?c .
                FILTER (lang(?c)='en' and lang(?productName)='en' and ?productName="{product_name}"@en)
        }}
    ORDER BY  DESC(?type)
    LIMIT 1
    """)
    try:
        sparql.setQuery(q)
        query_results = sparql.query().convert()
        return query_results["results"]["bindings"][0]["type"]["value"]
    except IndexError:
        return abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)