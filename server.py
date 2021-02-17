from flask import Flask, render_template, request, redirect, session, url_for, flash, escape
import data_handler
import util
from werkzeug.utils import secure_filename
import password_salter


app = Flask(__name__, static_folder="images")

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def index_page():
    question_list = data_handler.list_five_questions()
    email = None
    if 'email' in session:
        email = escape(session['email'])
    return render_template("index.html", question_list=question_list, email=email)


@app.route("/list")
def list_page():
    order_by = request.args.get('order_by', default='submission_time')
    order_direction = request.args.get('order_direction', default='DESC').upper()
    question_list = data_handler.list_all_questions(order_by, order_direction)
    email = None
    if 'email' in session:
        email = escape(session['email'])
    return render_template("list.html", question_list=question_list, email=email)


@app.route("/search")
def search():
    email = None
    if 'email' in session:
        email = escape(session['email'])
    search_phrase = request.args['q'].lower()
    if search_phrase:
        answers_with_sp = data_handler.get_answers_with_sp(search_phrase)

        def modifier(record):
            record['message'] = record['message'].lower().replace(search_phrase, f"<mark>{search_phrase}</mark>")
            return record
        answers_with_sp = list(map(lambda record: modifier(record), answers_with_sp))
        question_list = data_handler.search(search_phrase)
        question_list = list(map(lambda record: modifier(record), question_list))
        return render_template("list.html", question_list=question_list, answers_with_sp=answers_with_sp, email=email)
    return redirect('/')


@app.route("/question/<id>")
def question_page(id=None):
    q_comments = None
    a_comments = None
    tags = data_handler.list_tags(id)
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
    email = None
    if 'email' in session:
        email = escape(session['email'])
    return render_template("question.html", question=question, answers=answer_list, q_comments=q_comments, a_comments=a_comments, tags=tags, email=email)


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit(question_id):
    email = None
    if 'email' in session:
        email_by_question_id = data_handler.get_one_by_id('question', question_id)['email']
        email = escape(session['email'])
        if email == email_by_question_id:
            if request.method == 'POST':
                data_handler.edit_question(question_id, request.form['title'], request.form['message'])
                return redirect('/question/' + question_id)
            question = data_handler.get_one_by_id("question", question_id)
            return render_template('edit_question.html', question=question, email=email)
    return redirect('/')


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    email = None
    if 'email' in session:
        email_by_answer_id = data_handler.get_one_by_id('answer', answer_id)['email']
        email = escape(session['email'])
        if email == email_by_answer_id:
            answer_record = data_handler.get_one_by_id("answer", answer_id)
            if request.method == 'POST':
                data_handler.edit_answer(answer_id, request.form['message'])
                return redirect('/question/' + str(answer_record["question_id"]))
            answer = data_handler.get_one_by_id("answer", answer_id)
            return render_template('edit_answer.html', answer=answer, email=email)
    return redirect('/')


@app.route("/comment/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    email = None
    if 'email' in session:
        email_by_comment_id = data_handler.get_one_by_id('comment', comment_id)['email']
        email = escape(session['email'])
        if email == email_by_comment_id:
            comment_record = data_handler.get_one_by_id("comment", comment_id)
            question_id = comment_record['question_id']
            if comment_record['answer_id']:
                question_id = data_handler.get_one_by_id("answer", comment_record['answer_id'])['question_id']
            if request.method == 'POST':
                data_handler.edit_comment(comment_id, request.form['message'])
                data_handler.increase_comment_edit(comment_id)
                return redirect('/question/' + str(question_id))
            return render_template('edit_comment.html', comment=comment_record, email=email)
    return redirect('/')

@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    email = None
    if 'email' in session:
        user_id = data_handler.get_record_by_email(session['email'])['userid']
        email = escape(session['email'])
        if request.method == "POST":
            question_id = data_handler.new_question(request.form, user_id)
            f = request.files['picture_upload']
            pic_name = ""
            if f.filename:
                pic_name = "images/uploaded_images/" + secure_filename(str(question_id) + "." + f.content_type.split("/")[1])
                f.save("./" + pic_name)
                data_handler.insert_picture("question", question_id, pic_name)
            return redirect("/question/" + str(question_id))
        return render_template("add_question.html", email=email)
    return redirect('/')


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_new_answer(question_id=None):
    if 'email' in session:
        user_id = data_handler.get_record_by_email(session['email'])['userid']
        answer_id = data_handler.new_answer(question_id, request.form, user_id)
        f = request.files['picture_upload']
        pic_name = ""
        if f.filename:
            pic_name = "images/uploaded_images/answer/" + secure_filename(str(answer_id) + "." + f.content_type.split("/")[1])
            f.save("./" + pic_name)
            data_handler.insert_picture("answer", answer_id, pic_name)
        return redirect("/question/" + str(question_id))
    return redirect('/')


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id=None):
    if 'email' in session:
        email_by_answer_id = data_handler.get_one_by_id('answer', answer_id)['email']
        email = escape(session['email'])
        if email == email_by_answer_id:
            answer_record = data_handler.get_one_by_id("answer", answer_id)
            util.delete_pictures([] + [answer_record])
            data_handler.delete_record("comment", "answer_id", answer_id)
            data_handler.delete_record("answer", "id", answer_id)
            return redirect("/question/" + str(answer_record['question_id']))
    return redirect('/')


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    if 'email' in session:
        email_by_question_id = data_handler.get_one_by_id('question', question_id)['email']
        email = escape(session['email'])
        if email == email_by_question_id:
            question_record = data_handler.get_one_by_id("question", question_id)
            answer_records = data_handler.get_many_by_id("answer", "question_id", question_id)
            util.delete_pictures(answer_records + [question_record])
            data_handler.delete_record("question_tag", "question_id", question_id)
            data_handler.delete_record("comment", "question_id", question_id)
            for answer in answer_records:
                data_handler.delete_record("comment", "answer_id", answer["id"])
            data_handler.delete_record("answer", "question_id", question_id)
            data_handler.delete_record("question", "id", question_id)
    return redirect("/list")
            


@app.route("/question/<id>/new-comment", methods=["POST", "GET"])
def new_comment_question(id):
    email = None
    if 'email' in session:
        user_id = data_handler.get_record_by_email(session['email'])['userid']
        email = escape(session['email'])
        if request.method == "GET":
            return render_template("new-comment.html", id=id, record_type="question", email=email)
        else:
            new_comment = request.form['message']
            data_handler.new_comment(new_comment, user_id, question_id=id)
            return redirect('/question/' + str(id))
    return redirect('/')


@app.route("/answer/<id>/new-comment", methods=["POST", "GET"])
def new_comment_answer(id):
    email = None
    if 'email' in session:
        user_id = data_handler.get_record_by_email(session['email'])['userid']
        email = escape(session['email'])
        if request.method == "GET":
            return render_template("new-comment.html", id=id, record_type="answer", email=email)
        else:
            new_comment = request.form['message']
            data_handler.new_comment(new_comment, user_id, answer_id=id)
            answer_record = data_handler.get_one_by_id('answer', id)
            return redirect('/question/' + str(answer_record['question_id']))
    return redirect('/')


@app.route("/<record_type>/<id>/<vote_type>")
def vote(record_type=None, id=None, vote_type=None):
    util.repu_modifier(record_type, id, vote_type)
    data_handler.vote(vote_type, record_type, id)
    referrer = request.headers.get("Referer")
    return redirect(referrer)


@app.route("/picture/<picture_type>/<id>")
def open_up_picture(picture_type, id):
    referrer = request.headers.get("Referer")
    if picture_type == 'answer':
        answer = data_handler.get_one_by_id("answer", id)
        return render_template("image.html", picture_list=answer, referrer=referrer)
    question = data_handler.get_one_by_id("question", id)
    return render_template("image.html", picture_list=question, referrer=referrer)


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def new_tag(question_id):
    email = None
    if 'email' in session:
        email_by_question_id = data_handler.get_one_by_id('question', question_id)['email']
        email = escape(session['email'])
        if email == email_by_question_id:
            existing_tags = data_handler.get_tags()
            if request.method == "GET":
                return render_template("add_tag.html", id=question_id, existing_tags=existing_tags, email=email)
            new_tag = request.form['tag_name'] if request.form['tag_name'] else request.form['existing_tag']
            data_handler.add_new_tag(question_id, new_tag)
            return redirect("/question/" + str(question_id))
    return redirect('/')


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id=None, tag_id=None):
    if 'email' in session:
        email_by_question_id = data_handler.get_one_by_id('question', question_id)['email']
        email = escape(session['email'])
        if email == email_by_question_id:
            data_handler.delete_tag(question_id, tag_id)
            return redirect("/question/" + str(question_id))
    return redirect('/')


@app.route("/comments/<comment_id>/delete")
def delete_comment(comment_id):
    if 'email' in session:
        email_by_comment_id = data_handler.get_one_by_id('comment', comment_id)['email']
        email = escape(session['email'])
        if email == email_by_comment_id:
            comment_record = data_handler.get_one_by_id("comment", comment_id)
            question_id = comment_record['question_id']
            if comment_record['answer_id']:
                question_id = data_handler.get_one_by_id("answer", comment_record['answer_id'])['question_id']
            data_handler.delete_comment(comment_id)
            return redirect('/question/' + str(question_id))
    return redirect('/')


@app.route("/registration", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = password_salter.hash_password(request.form['password'])
        data_handler.add_new_user(email, password)
        return redirect('/')
    return render_template("registration.html")


@app.route("/login", methods=['GET', 'POST'])
def sign_in():
    email = request.form['email']
    password = request.form['password']
    user_record = data_handler.get_record_by_email(email)
    referrer = request.headers.get("Referer")
    if user_record:
        if password_salter.verify_password(password, user_record['password']):
            session['email'] = email
            session['userid'] = user_record['userid']
            return redirect(referrer)
        flash("Incorrect username or password!")
        return redirect(referrer)
    else:
        flash("Username doesn't exists!")
        return redirect(referrer)


@app.route('/acceptance/<answer_id>/<question_id>')
def acceptance(answer_id=None, question_id=None):
    if 'email' in session:
        email_by_question_id = data_handler.get_one_by_id('question', question_id)['email']
        email = escape(session['email'])
        if email_by_question_id == email:
            data_handler.accept_answer(answer_id)
    referrer = request.headers.get("Referer")
    return redirect(referrer)


@app.route("/logout")
def sign_out():
    session.pop("email", None)
    referrer = request.headers.get("Referer")
    return redirect(referrer)


@app.route("/users")
def list_users():
    if 'email' in session:
        email = escape(session['email'])
        users_data = data_handler.list_users()
        return render_template("users.html", email=email, users_data=users_data)
    return redirect('/')


@app.route("/user/<userid>")
def user_profile(userid=None):
    if 'email' in session:
        email = escape(session['email'])
        users_data = data_handler.list_users(userid)
        questions = data_handler.get_many_by_id('question', 'user_id', userid)
        answers = data_handler.get_many_by_id('answer', 'user_id', userid)
        comments = data_handler.get_many_by_id('comment', 'user_id', userid)
        return render_template(
            "users.html", email=email, 
            users_data=users_data,
            questions=questions,
            answers=answers,
            comments=comments)
    return redirect('/')


@app.route("/tags")
def tags():
    email = escape(session['email'])
    tags = data_handler.get_tags()
    return render_template("tags.html", email=email, tags=tags)

if __name__ == "__main__":
    app.run(debug=True)
