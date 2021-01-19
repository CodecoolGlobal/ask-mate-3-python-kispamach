from flask import Flask, render_template, request, redirect
import data_handler
import util
import engine
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="images")


@app.route("/")
@app.route("/list")
def main_page():
    question_list = data_handler.reader('question')
    order_by = request.args.get('order_by', default='submission_time')
    order_direction = request.args.get('order_direction', default='desc')
    question_list = engine.sort_data(order_by, order_direction, question_list)
    return render_template("list.html", question_list=util.date_formatter(question_list))


@app.route("/question/<id>")
def question_page(id=None):
    question_list = data_handler.reader('question')
    question = list(filter(lambda record: record["id"] == id, question_list))[0]
    answer_list = data_handler.reader('answer')
    answers = list(filter(lambda record: record["question_id"] == id, answer_list))
    return render_template("question.html", question=question, answers=answers)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        f = request.files['picture_upload']
        # extension = f.content_type.split("/")
        # print(extension)
        f.save("./images/uploaded_images/" + secure_filename("dicpic." + f.content_type.split("/")[1]))
        return 'file uploaded successfully'
        # return redirect("/")
    return render_template("add_question.html")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id=None):
    answer_list = data_handler.reader('answer')
    answers = list(filter(lambda record: record["id"] != answer_id, answer_list))
    question_id = list(filter(lambda record: record["id"] == answer_id, answer_list))[0]["question_id"]
    data_handler.writer("answer", answers)
    return redirect("/question/" + question_id)


@app.route("/question/<id>/upvote")
def upvote(id=None):
    current_file = data_handler.reader('question')
    for i in range(len(current_file)):
        if current_file[i]['id'] == id:
            current_file[i]['vote_number'] = str(int(current_file[i]['vote_number']) + 1)
    data_handler.writer('question', current_file)
    return redirect('/list')


@app.route("/question/<id>/downvote")
def downvote(id=None):
    current_file = data_handler.reader('question')
    for i in range(len(current_file)):
        if current_file[i]['id'] == id:
            current_file[i]['vote_number'] = str(int(current_file[i]['vote_number']) - 1)
    data_handler.writer('question', current_file)
    return redirect('/list')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
    )
