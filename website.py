from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


class Website():
    def __init__(self):
        self.main()

    def main(self):
        app = Flask(__name__)

        @app.route("/")
        def upload_file():
            return render_template("index.html")

        @app.route("/uploader", methods=["GET", "POST"])
        def uploader_file():
            if request.method == "POST":
                f = request.files["file"]
                f.save(secure_filename(f.filename))
                return "file uploaded successfully"

        app.run(debug=True)


if __name__=="__main__":
    ws = Website()
