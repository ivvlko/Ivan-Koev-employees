import os
import pandas as pd

from flask import Flask, render_template, request, redirect

from datetime import datetime

from utils import calculate_pairs_working_time_together, handle_different_datetypes


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def page():
    data = []

    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return redirect(request.url)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath)

            df['DateFrom'] = handle_different_datetypes(df['DateFrom'])
            df['DateTo'] = df['DateTo'].fillna(datetime.today().strftime('%Y-%m-%d'))
            df['DateTo'] = handle_different_datetypes(df['DateTo'])

            df.dropna(subset=['DateFrom', 'DateTo'], inplace=True)

            data = calculate_pairs_working_time_together(df)
        except Exception as e:
            return f"Error processing file: {e}"

    return render_template('page.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
