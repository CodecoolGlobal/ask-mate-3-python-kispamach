from flask import Flask, render_template, request, redirect
import data_handler
import util
import engine
from werkzeug.utils import secure_filename
from datetime import datetime

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
    referrer = request.headers.get("Referer").split("/")
    if referrer[-2] != 'question':
        question['view_number'] = str(int(question['view_number']) + 1)
    questions_modified = list(map(lambda record: question if record['id'] == id else record, question_list))
    data_handler.writer('question', questions_modified)
    question = util.convert_to_date(question)
    answer_list = data_handler.reader('answer')
    answers = list(filter(lambda record: record["question_id"] == id, answer_list))
    answers = engine.sort_answers("vote_number", "desc", answers)
    answers = util.date_formatter(answers)
    return render_template("question.html", question=question, answers=answers)


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit(question_id):
    questions = data_handler.reader("question")
    question = list(filter(lambda record: record["id"] == question_id, questions))[0]
    if request.method == 'POST':
        question['title'] = request.form['title']
        question['message'] = request.form['message']
        questions = list(map(lambda record: question if record['id'] == question_id else record, questions))
        data_handler.writer('question', questions)
        return redirect('/question/' + question_id)
    return render_template('edit_question.html', question=question)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        questions = data_handler.reader('question')
        question_id = util.generate_id("q")
        f = request.files['picture_upload']
        pic_name = ""
        if f.filename:
            pic_name = "images/uploaded_images/" + secure_filename(question_id + "." + f.content_type.split("/")[1])
            f.save("./" + pic_name)
        new_question = {
            "id": question_id,
            "submission_time": str(int(datetime.now().timestamp())),
            "view_number": "0",
            "vote_number": "0",
            "title": request.form['title'],
            "message": request.form['message'],
            "image": pic_name
        }
        questions.append(new_question)
        data_handler.writer("q", questions)
        return redirect("/question/" + question_id)
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_new_answer(question_id=None):
    answers = data_handler.reader('answer')
    answer_id = util.generate_id("a")
    f = request.files['picture_upload']
    pic_name = ""
    if f.filename:
        pic_name = "images/uploaded_images/" + secure_filename(answer_id + "." + f.content_type.split("/")[1])
        f.save("./" + pic_name)
    new_answer = {
        'id': answer_id,
        "submission_time": str(int(datetime.now().timestamp())),
        "vote_number": "0",
        "question_id": question_id,
        "message": request.form['message'],
        "image": pic_name
    }
    answers.append(new_answer)
    data_handler.writer('answer', answers)
    return redirect('/question/' + question_id)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id=None):
    answer_list = data_handler.reader('answer')
    answers_remaining = list(filter(lambda record: record["id"] != answer_id, answer_list))
    answers_removed = list(filter(lambda record: record["id"] == answer_id, answer_list))
    util.delete_pictures(answers_removed)
    question_id = list(filter(lambda record: record["id"] == answer_id, answer_list))[0]["question_id"]
    data_handler.writer("answer", answers_remaining)
    return redirect("/question/" + question_id)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    question_list = data_handler.reader("question")
    question_remaining = list(filter(lambda record: record["id"] != question_id, question_list))
    removed_question = list(filter(lambda record: record["id"] == question_id, question_list))

    answer_list = data_handler.reader('answer')
    answers_remaining = list(filter(lambda record: record["question_id"] != question_id, answer_list))
    removed_answers = list(filter(lambda record: record["question_id"] == question_id, answer_list))
    util.delete_pictures(removed_answers + removed_question)
    data_handler.writer("answer", answers_remaining)
    data_handler.writer("question", question_remaining)
    return redirect("/")


@app.route("/question/<id>/upvote")
def upvote(id=None):
    current_file = data_handler.reader('question')
    for i in range(len(current_file)):
        if current_file[i]['id'] == id:
            current_file[i]['vote_number'] = str(int(current_file[i]['vote_number']) + 1)
    data_handler.writer('question', current_file)
    referrer = request.headers.get("Referer").split("/")
    if referrer[-2] == 'question':
        return redirect('/question/' + referrer[-1])
    return redirect('/list')


@app.route("/question/<id>/downvote")
def downvote(id=None):
    current_file = data_handler.reader('question')
    for i in range(len(current_file)):
        if current_file[i]['id'] == id:
            current_file[i]['vote_number'] = str(int(current_file[i]['vote_number']) - 1)
    data_handler.writer('question', current_file)
    referrer = request.headers.get("Referer").split("/")
    if referrer[-2] == 'question':
        return redirect('/question/' + referrer[-1])
    return redirect('/list')


@app.route("/answer/<id>/upvote")
def upvote_answer(id=None):
    current_file = data_handler.reader('answer')
    question_id = list(filter(lambda record: record["id"] == id, current_file))[0]['question_id']
    for i in range(len(current_file)):
        if current_file[i]['id'] == id:
            current_file[i]['vote_number'] = str(int(current_file[i]['vote_number']) + 1)
    data_handler.writer('answer', current_file)
    return redirect('/question/' + question_id)


@app.route("/picture/<id>")
def open_up_picture(id):
    referrer = request.headers.get("Referer")
    if id[0] == 'a':
        answer_list = data_handler.reader('answer')
        picture_list = list(filter(lambda record: record["id"] == id, answer_list))[0]
        return render_template("image.html", picture_list=picture_list, referrer=referrer)
    question_list = data_handler.reader("question")
    picture_list = list(filter(lambda record: record["id"] == id, question_list))[0]
    return render_template("image.html", picture_list=picture_list, referrer=referrer)

@app.route("/answer/<id>/downvote")
def downvote_answer(id=None):
    current_file = data_handler.reader('answer')
    question_id = list(filter(lambda record: record["id"] == id, current_file))[0]['question_id']
    for i in range(len(current_file)):
        if current_file[i]['id'] == id:
            current_file[i]['vote_number'] = str(int(current_file[i]['vote_number']) - 1)
    data_handler.writer('answer', current_file)
    return redirect('/question/' + question_id)


if __name__ == "__main__":
    app.run()
