from flask import Flask, request, jsonify
import sqlite3, pandas as pd

app = Flask(__name__)

def db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return "API Running"

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    df = pd.read_excel(file)
    conn = db(); cur = conn.cursor()
    for _, r in df.iterrows():
        cur.execute("INSERT INTO agencies(name) VALUES(?)", (r["agency"],))
        aid = cur.lastrowid
        cur.execute("INSERT INTO agents(name, agency_id) VALUES(?,?)", (r["agent"], aid))
    conn.commit(); conn.close()
    return {"status":"uploaded"}

@app.route("/agents")
def agents():
    s = request.args.get("search","")
    conn=db();cur=conn.cursor()
    cur.execute("SELECT agents.name, agencies.name FROM agents JOIN agencies ON agents.agency_id=agencies.id WHERE agents.name LIKE ?", ('%'+s+'%',))
    data=cur.fetchall(); conn.close()
    return jsonify(data)

@app.route("/products", methods=["POST"])
def add_product():
    d=request.json
    conn=db();cur=conn.cursor()
    cur.execute("INSERT INTO products(name,season,price) VALUES(?,?,?)",(d["name"],d["season"],d["price"]))
    conn.commit(); conn.close()
    return {"status":"added"}

@app.route("/commission", methods=["POST"])
def commission():
    d=request.json
    c=10
    if d["season"]=="low": c+=10
    if d["days"]<=5: c+=5
    if d["price"]>50000: c+=7
    return {"commission":c}

