# Shamelessly copied from http://flask.pocoo.org/docs/quickstart/
from flask import Flask, request, jsonify
from utils import *

# init Flask app
app = Flask(__name__)

@app.route('/', methods=['POST'])
def run():
    cms_version = ""
    cms_plugin = []    
    content = request.json

    domain   = content['domain']
    outputfile = content['outputfile']

    prefix = ["https://www."+str(domain)]
    for y in prefix:
        print ("--------------------------> "+y)
        hb = is_hubspot(y)
        if hb:
            print ("Hubspot detected")    
            write_in_a_file(domain+";Hubspot;;",outputfile)
            #pass        

        wordpress = is_wordpress(y)
        if wordpress:
            print (y+" WordPress detected")
            print (cms_version)
            write_in_a_file(domain+";WordPress;"+str(cms_version)+";"+str(cms_plugin),outputfile)
            #pass

        shopify = is_shopify(y)
        if shopify:
            print (y+" Shopify detected")
            write_in_a_file(domain+";Shopify;;",outputfile)
            #pass

        if not wordpress or not shopify or not hb:
            print ("non detected")
            pass
    return {'message': 'Done!'}


