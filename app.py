from flask import Flask, render_template, request
from deepface import DeepFace
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/match', methods=['GET', 'POST'])
def face_match():
    if request.method == 'POST':
        img1 = request.files['img1']
        img2 = request.files['img2']

        img1_path = os.path.join("static", img1.filename)
        img2_path = os.path.join("static", img2.filename)

        img1.save(img1_path)
        img2.save(img2_path)

        try:
            result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path)
            verified = result["verified"]
            message = "Verified" if verified else "They are not the same."
        except Exception as e:
            message = f"An error occurred: {e}"

        return render_template('result.html', result=message)

    return render_template('index.html', mode='match')


@app.route('/analyze', methods=['GET', 'POST'])
def face_analysis():
    if request.method == 'POST':
        img = request.files['img']
        img_path = os.path.join("static", img.filename)
        img.save(img_path)

        try:
            analysis = DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'race'])
            result = {
                "Gender": analysis[0]["gender"],
                "Age": analysis[0]["age"],
                "Nationality (Race)": analysis[0]["dominant_race"]
            }
        except Exception as e:
            result = {"Error": str(e)}

        return render_template('result.html', result=result)

    return render_template('index.html', mode='analyze')


@app.route('/find', methods=['GET', 'POST'])
def find_face():
    if request.method == 'POST':
        img = request.files['img']
        db_path = request.form['db_path']

        img_path = os.path.join("static", img.filename)
        img.save(img_path)

        try:
            dfs = DeepFace.find(img_path=img_path, db_path=db_path)
            result = "Face Found" if len(dfs) > 0 else "Face Not Found"
        except Exception as e:
            result = f"An error occurred: {e}"

        return render_template('result.html', result=result)

    return render_template('index.html', mode='find')


if __name__ == "__main__":
    app.run(debug=True)

