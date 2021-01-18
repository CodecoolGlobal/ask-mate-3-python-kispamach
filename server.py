from flask import Flask, render_template, request, redirect
import data_handler

app = Flask(__name__, static_folder="images")


@app.route("/")
@app.route("/list")
def main_page():
    question_list = data_handler.reader('question')
    return render_template("list.html", question_list=question_list)



if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
    )
