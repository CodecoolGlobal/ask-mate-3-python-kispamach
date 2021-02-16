from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_connection
from datetime import datetime

@database_connection.connection_handler
def list_all_questions(cursor: RealDictCursor, order_by, order_direction):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {order_by} {order_direction}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_one_by_id(cursor: RealDictCursor, data_table, id):
    query = f"""
        SELECT *
        FROM {data_table}
        WHERE id = {id}
    """
    cursor.execute(query)
    return cursor.fetchone()


@database_connection.connection_handler
def get_many_by_id(cursor: RealDictCursor, data_table, column_name, id):
    query = f"""
        SELECT *
        FROM {data_table}
        WHERE {column_name} = {id}
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def increase_view_number(cursor: RealDictCursor, id):
    query = f"""
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = {id}
    """
    cursor.execute(query)


@database_connection.connection_handler
def list_answer_for_question(cursor: RealDictCursor, id):
    query = f"""
        SELECT *
        FROM answer
        WHERE question_id = {id}
        ORDER BY vote_number DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def edit_question(cursor: RealDictCursor, question_id, title, message):
    query = """
        UPDATE question
        SET title = %(title)s, message = %(message)s
        WHERE id = %(id)s
    """
    cursor.execute(query, {'title': title, 'message': message, 'id': question_id})


@database_connection.connection_handler
def edit_comment(cursor: RealDictCursor, comment_id, message):
    query = """
        UPDATE comment
        SET message = %(message)s
        WHERE id = %(id)s
    """
    cursor.execute(query, {'message': message, 'id': comment_id})


@database_connection.connection_handler
def edit_answer(cursor: RealDictCursor, answer_id, message):
    query = """
        UPDATE answer
        SET message = %(message)s
        WHERE id = %(id)s
    """
    cursor.execute(query, {'message': message, 'id': answer_id})


@database_connection.connection_handler
def new_question(cursor: RealDictCursor, form, user_id):
    date = datetime.now().strftime("%b %d %Y %H:%M:%S")
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, user_id)
        VALUES (%(date)s, 0, 0, %(title)s, %(message)s, %(user_id)s)
    """
    cursor.execute(query, {"title": form['title'], "message": form['message'], "user_id": user_id, "date": date})
    cursor.execute('SELECT LASTVAL()')
    return cursor.fetchone()['lastval']


@database_connection.connection_handler
def new_answer(cursor: RealDictCursor, question_id, form):
    date = datetime.now().strftime("%b %d %Y %H:%M:%S")
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message)
        VALUES ('{date}', 0, %(question_id)s, %(message)s)
    """
    cursor.execute(query, {"question_id": question_id, "message": form['message']})
    cursor.execute('SELECT LASTVAL()')
    return cursor.fetchone()['lastval']


@database_connection.connection_handler
def insert_picture(cursor: RealDictCursor, data_table, id, pic_name):
    query = f"""
        UPDATE {data_table}
        SET image = '{pic_name}'
        WHERE id = {id}
    """
    cursor.execute(query)


@database_connection.connection_handler
def delete_record(cursor: RealDictCursor, data_table, column_name, id):
    query = f"""
        DELETE FROM {data_table}
        WHERE {column_name} = {id}
    """
    cursor.execute(query)


@database_connection.connection_handler
def vote(cursor: RealDictCursor, vote, data_table, id):
    number = 1 if vote == "upvote" else -1
    query = f"""
        UPDATE {data_table}
        SET vote_number = vote_number + {number}
        WHERE id = {id}
    """
    cursor.execute(query)


@database_connection.connection_handler
def new_comment(cursor: RealDictCursor, message, question_id=None, answer_id=None):
    date = datetime.now().strftime("%b %d %Y %H:%M:%S")
    column = 'question_id' if question_id else 'answer_id'
    id = question_id if question_id else answer_id
    query = f"""
        INSERT INTO comment ({column}, message, submission_time)
        VALUES ({id}, %(message)s, '{date}')
    """
    cursor.execute(query, {"message": message})


@database_connection.connection_handler
def search(cursor: RealDictCursor, search_phrase):
    search_phrase = f"%{search_phrase}%"
    query = f"""
        SELECT question.id, question.submission_time, question.view_number,
            question.vote_number, question.title, question.message, question.image
        FROM question
        LEFT JOIN answer
        ON question.id = answer.question_id
        WHERE UPPER(CONCAT(title, question.message, answer.message)) LIKE UPPER(%(search_phrase)s)
        GROUP BY question.id
        """
    cursor.execute(query, {"search_phrase": search_phrase})
    return cursor.fetchall()


@database_connection.connection_handler
def increase_comment_edit(cursor: RealDictCursor, comment_id):
    date = datetime.now().strftime("%b %d %Y %H:%M:%S")
    cursor.execute(f"SELECT edited_count FROM comment WHERE id = {comment_id}")
    if cursor.fetchone()['edited_count'] == None:
        query = f"""
            UPDATE comment
            SET edited_count = 1, submission_time = '{date}'
            WHERE id = {comment_id}
        """
    else:
        query = f"""
            UPDATE comment
            SET edited_count = edited_count + 1, submission_time = '{date}'
            WHERE id = {comment_id}
        """
    cursor.execute(query)


@database_connection.connection_handler
def list_tags(cursor: RealDictCursor, question_id):
    query = f"""
        SELECT tag.name, tag.id
        FROM question
        INNER JOIN question_tag
        ON id = question_tag.question_id
        INNER JOIN tag
        ON question_tag.tag_id = tag.id
        WHERE question_id = {question_id}
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def add_new_tag(cursor: RealDictCursor, id, new_tag):
    cursor.execute(f"SELECT name, id FROM tag WHERE name = '{new_tag}'")
    tag_record = cursor.fetchone()
    if tag_record is None:
        query = f"INSERT INTO tag (name) VALUES('{new_tag}')"
        cursor.execute(query)
        cursor.execute('SELECT LASTVAL()')
        last_id = cursor.fetchone()['lastval']
    else:
        last_id = tag_record['id']
    cursor.execute(f"SELECT * FROM question_tag WHERE question_id = {id} AND tag_id = {last_id}")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO question_tag VALUES({id}, {last_id})")


@database_connection.connection_handler
def get_tags(cursor: RealDictCursor):
    cursor.execute("SELECT * FROM tag")
    return cursor.fetchall()


@database_connection.connection_handler
def delete_tag(cursor: RealDictCursor, question_id, tag_id):
    cursor.execute(f"DELETE FROM question_tag WHERE question_id = {question_id} AND tag_id = {tag_id}")


@database_connection.connection_handler
def delete_comment(cursor: RealDictCursor, id):
    cursor.execute(f"DELETE FROM comment WHERE id = {id}")


@database_connection.connection_handler
def list_five_questions(cursor: RealDictCursor):
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_answers_with_sp(cursor: RealDictCursor, search_phrase):
    query = f"""
        SELECT message, question_id
        FROM answer
        WHERE UPPER(message) LIKE UPPER('%{search_phrase}%')
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def add_new_user(cursor: RealDictCursor, email, password):
    date = datetime.now().strftime("%b %d %Y %H:%M:%S")
    query = """
        INSERT INTO users (email, password, registration_time)
        VALUES (%(email)s, %(password)s, %(date)s)
    """
    data = {
        'email': email,
        'password': password,
        'date': date
    }
    cursor.execute(query, data)


@database_connection.connection_handler
def get_record_by_email(cursor: RealDictCursor, email):
    query = """
        SELECT * FROM users
        WHERE email = %(email)s
    """
    data = {
        'email': email
    }
    cursor.execute(query, data)
    return cursor.fetchone()
