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
    order_by = request.args.get('order_by', default='submission_time')
    order_direction = request.args.get('order_direction', default='DESC').upper()
    question_list = data_handler.list_all_questions(order_by, order_direction)
    return render_template("list.html", question_list=question_list)


@app.route("/search")
def search():
    search_phrase = request.args['q']
    question_list = data_handler.search(search_phrase)
    return render_template("list.html", question_list=question_list)
    

@app.route("/question/<id>")
def question_page(id=None):
    q_comments = None
    a_comments = None
    referrer = request.headers.get("Referer").split("/")
    if referrer[-2] != 'question':
        data_handler.increase_view_number(id)
    question = data_handler.get_one_by_id("question", id)
    answer_list = data_handler.list_answer_for_question(id)
    q_comments = data_handler.get_many_by_id("comment", "question_id", id)
    if len(answer_list) != 0:
        a_comments = {}
        for answer in answer_list:
            comments_for_answer = data_handler.get_many_by_id("comment", "answer_id", answer['id'])
            if len(comments_for_answer) != 0:
                a_comments[answer['id']] = comments_for_answer
    return render_template("question.html", question=question, answers=answer_list, q_comments=q_comments, a_comments=a_comments)


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit(question_id):
    if request.method == 'POST':
        data_handler.edit_question(question_id, request.form['title'], request.form['message'])
        return redirect('/question/' + question_id)
    question = data_handler.get_one_by_id("question", question_id)
    return render_template('edit_question.html', question=question)


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer_record = data_handler.get_one_by_id("answer", answer_id)
    if request.method == 'POST':
        data_handler.edit_answer(answer_id, request.form['message'])
        return redirect('/question/' + str(answer_record["question_id"]))
    answer = data_handler.get_one_by_id("answer", answer_id)
    return render_template('edit_answer.html', answer=answer)


@app.route("/comment/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment_record = data_handler.get_one_by_id("comment", comment_id)
    question_id = comment_record['question_id']
    if comment_record['answer_id']:
        question_id = data_handler.get_one_by_id("answer", comment_record['answer_id'])['question_id']
    if request.method == 'POST':
        data_handler.edit_comment(comment_id, request.form['message'])
        data_handler.increase_comment_edit(comment_id)
        return redirect('/question/' + str(question_id))
    return render_template('edit_comment.html', comment=comment_record)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        question_id = data_handler.new_question(request.form)
        f = request.files['picture_upload']
        pic_name = ""
        if f.filename:
            pic_name = "images/uploaded_images/" + secure_filename(str(question_id) + "." + f.content_type.split("/")[1])
            f.save("./" + pic_name)
            data_handler.insert_picture("question", question_id, pic_name)
        return redirect("/question/" + str(question_id))
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_new_answer(question_id=None):
    answer_id = data_handler.new_answer(question_id, request.form)
    f = request.files['picture_upload']
    pic_name = ""
    if f.filename:
        pic_name = "images/uploaded_images/answer/" + secure_filename(str(answer_id) + "." + f.content_type.split("/")[1])
        f.save("./" + pic_name)
        data_handler.insert_picture("answer", answer_id, pic_name)
    return redirect("/question/" + str(question_id))


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id=None):
    answer_record = data_handler.get_one_by_id("answer", answer_id)
    util.delete_pictures([] + [answer_record])
    data_handler.delete_record("answer", "id", answer_id)
    return redirect("/question/" + str(answer_record['question_id']))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    question_record = data_handler.get_one_by_id("question", question_id)
    answer_records = data_handler.get_many_by_id("answer", "question_id", question_id)
    util.delete_pictures(answer_records + [question_record])
    data_handler.delete_record("answer", "question_id", question_id)
    data_handler.delete_record("question", "id", question_id)
    return redirect("/")


@app.route("/question/<id>/new-comment", methods=["POST", "GET"])
def new_comment_question(id):
    if request.method == "GET":
        return render_template("new-comment.html", id=id, record_type="question")
    new_comment = request.form['message']
    data_handler.new_comment(new_comment, question_id=id)
    return redirect('/question/' + str(id))


@app.route("/answer/<id>/new-comment", methods=["POST", "GET"])
def new_comment_answer(id):
    if request.method == "GET":
        return render_template("new-comment.html", id=id, record_type="answer")
    new_comment = request.form['message']
    data_handler.new_comment(new_comment, answer_id=id)
    answer_record = data_handler.get_one_by_id('answer', id)
    return redirect('/question/' + str(answer_record['question_id']))


@app.route("/<record_type>/<id>/<vote_type>")
def vote(record_type=None, id=None, vote_type=None):
    data_handler.vote(vote_type, record_type, id)
    referrer = request.headers.get("Referer").split("/")
    if referrer[-2] in ['question', 'answer']:
        return redirect('/question/' + referrer[-1])
    return redirect('/list')


@app.route("/picture/<picture_type>/<id>")
def open_up_picture(picture_type, id):
    referrer = request.headers.get("Referer")
    if picture_type == 'answer':
        answer = data_handler.get_one_by_id("answer", id)
        return render_template("image.html", picture_list=answer, referrer=referrer)
    question = data_handler.get_one_by_id("question", id)
    return render_template("image.html", picture_list=question, referrer=referrer)


if __name__ == "__main__":
    app.run(debug=True)
