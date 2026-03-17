from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

# =========================
# Database Connection
# =========================
def get_db():
    return sqlite3.connect("database.db")


# =========================
# Initialize Database
# =========================
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS agencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            agency_id INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            season TEXT,
            price INTEGER
        )
    """)

    conn.commit()
    conn.close()


# Run DB init at startup (IMPORTANT)
init_db()


# =========================
# Health Check
# =========================
@app.route("/")
def home():
    return jsonify({"message": "API Running"})


# =========================
# Upload Excel
# =========================
@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        df = pd.read_excel(file)

        conn = get_db()
        cur = conn.cursor()

        for _, row in df.iterrows():
            agency_name = str(row.get("agency", "")).strip()
            agent_name = str(row.get("agent", "")).strip()

            if not agency_name or not agent_name:
                continue

            # Check if agency exists
            cur.execute("SELECT id FROM agencies WHERE name=?", (agency_name,))
            result = cur.fetchone()

            if result:
                agency_id = result[0]
            else:
                cur.execute(
                    "INSERT INTO agencies(name) VALUES(?)",
                    (agency_name,)
                )
                agency_id = cur.lastrowid

            # Insert agent
            cur.execute(
                "INSERT INTO agents(name, agency_id) VALUES(?, ?)",
                (agent_name, agency_id)
            )

        conn.commit()
        conn.close()

        return jsonify({"message": "File uploaded successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# Search Agents
# =========================
@app.route("/agents", methods=["GET"])
def agents():
    try:
        search = request.args.get("search", "")

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            """SELECT agents.name, agencies.name
               FROM agents
               JOIN agencies ON agents.agency_id = agencies.id
               WHERE agents.name LIKE ?""",
            ('%' + search + '%',)
        )

        data = cur.fetchall()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# Add Product
# =========================
@app.route("/products", methods=["POST"])
def add_product():
    try:
        data = request.json

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO products(name, season, price) VALUES(?, ?, ?)",
            (data["name"], data["season"], data["price"])
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Product added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# Commission Calculator
# =========================
@app.route("/commission", methods=["POST"])
def commission():
    try:
        data = request.json

        commission = 10

        if data["season"] == "low":
            commission += 10

        if data["days"] <= 5:
            commission += 5

        if data["price"] > 50000:
            commission += 7

        return jsonify({"commission": commission})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# Run App (Render Compatible)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
