import json
from flask import Flask, render_template, redirect, url_for, request, Response
import requests
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.qparser import MultifieldParser
import whoosh.highlight as highlight




app = Flask(__name__)


def search_corpus(mot):
    tab=[]
    ix = index.open_dir("nurmberg")
    with ix.searcher() as searcher:
        #query = MultifieldParser(["title", "sp","text"], schema=ix.schema).parse(mot)
        query = QueryParser("text", ix.schema).parse(mot)
        res = searcher.search(query,limit=None)
        res.fragmenter = highlight.WholeFragmenter()
        for i in res:
            #tab.append([i['title'],i['sp'],i['text']])
            tab.append(i.highlights("text"))
    return tab




@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search",methods=["POST","GET"])
def search():
    if request.method == "GET":
        q = request.args.get("q")
        res=search_corpus(q)
        return render_template("res.html",res=res,n=len(res))


if __name__ == "__main__":
    app.run(debug=True)