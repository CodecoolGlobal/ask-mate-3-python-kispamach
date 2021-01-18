from flask import Flask, render_template, request, redirect
import data_handler
import util
import engine

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
    return render_template("question.html", question=question)


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
