import csv
import engine

FILE_OF_ANSWER = "answer.csv"
FILE_OF_QUESTION = "question.csv"
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]


def reader(file):
    if file == "answer":
        filename = FILE_OF_ANSWER
    else:
        filename = FILE_OF_QUESTION
    with open(filename, "r") as csv_file:
        return [record for record in csv.DictReader(csv_file)]


def writer(file, data):
    if file == "answer":
        filename = FILE_OF_ANSWER
        headers = ANSWER_HEADERS
    else:
        filename = FILE_OF_QUESTION
        headers = QUESTION_HEADERS

    with open(filename, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for record in data:
            writer.writerow(record)
