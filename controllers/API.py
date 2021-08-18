from flask import Flask, request
from flask_cors import cross_origin

from myProject.SendEmail.SendEmail import Mail

from myProject.ImageProcessing.Execute import Execute

app = Flask(__name__)


@app.route('/upload', methods=['GET', 'POST'])
@cross_origin()  # מגשר בין הפייתון לריאקט
def upload_file():  # מקבלת תמונות של ת.ז. וספח ומחזירה לריאקט מילון
    if request.method == 'POST':
        f1 = request.files['first']  # תמונה תעודת זהות
        f2 = request.files['second']  # תמונת ספח
        result = Execute.mainFunc(f1, f2)  # העברת הקבצים לפיענוח
        return result
    else:
        return 'No file'


@app.route('/sendMail', methods=['GET', 'POST'])
@cross_origin()
def sendmail():
    try:
        # יצירת אובייקט המטפל במייל ושולח אותו
        Mail([request.form['to']], request.form['subject'], request.form['content'], list(request.files['form']))
        return '1'
    except:
        return '0'


if __name__ == "__main__":
    app.run(debug=True)  # בריענון של הדף נותן שינויים שלא יצטרכו לפתוח שוב
