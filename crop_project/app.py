from flask import Flask, render_template, request, send_from_directory
from weather import get_weather
from disease_model import predict_disease
from pest_model import predict_pest_risk
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Create database if not exists
def init_db():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image TEXT,
        disease TEXT,
        pest TEXT,
        confidence REAL,
        solution TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files["image"]
        city = request.form["city"]

        # Get weather automatically
        temp, humidity, rainfall = get_weather(city)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # AI prediction
        disease, confidence, solution = predict_disease(filepath)
        pest = predict_pest_risk(temp, humidity, rainfall)

        # Save prediction to database
        conn = sqlite3.connect("history.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO predictions (image, disease, pest, confidence, solution) VALUES (?,?,?,?,?)",
            (file.filename, disease, pest, confidence, solution)
        )

        conn.commit()
        conn.close()

        return render_template(
            "result.html",
            disease=disease,
            pest=pest,
            solution=solution,
            confidence=confidence,
            image=file.filename,
            temp=temp,
            humidity=humidity,
            rainfall=rainfall
        )

    return render_template("index.html")


# History dashboard
@app.route("/history")
def history():

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    data = cursor.fetchall()

    conn.close()

    return render_template("history.html", data=data)


# Statistics dashboard
@app.route("/stats")
def stats():

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT disease, COUNT(*) FROM predictions GROUP BY disease")
    disease_data = cursor.fetchall()

    cursor.execute("SELECT pest, COUNT(*) FROM predictions GROUP BY pest")
    pest_data = cursor.fetchall()

    conn.close()

    diseases = [row[0] for row in disease_data]
    disease_counts = [row[1] for row in disease_data]

    pests = [row[0] for row in pest_data]
    pest_counts = [row[1] for row in pest_data]

    return render_template(
        "stats.html",
        diseases=diseases,
        disease_counts=disease_counts,
        pests=pests,
        pest_counts=pest_counts
    )


# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)