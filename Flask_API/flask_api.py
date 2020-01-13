from flask import jsonify, request, Response
import json
from settings import *

posts = [
    {
        "Author": "Gautam_1",
        "Title": "PUBG",
        "posted_on": 2020,
        "Content": "About PUBG"
    },
    {
        "Author": "Gautam",
        "Title": "Cricket Article",
        "posted_on": 2019,
        "Content": "About Cricket"
    },
{
        "Author": "Gautam",
        "Title": "Python Article",
        "posted_on": 2018,
        "Content": "About Python"
    }
]


@app.route("/posts")
def get_posts():
    return jsonify({"posts": posts})


@app.route("/posts", methods=["POST"])
def add_books():
    request_data = request.get_json()
    if valid_data(request_data):
        new_post = {"Author": request_data["Author"],
                    "Title": request_data["Title"],
                    "posted_on": request_data["posted_on"],
                    "Content": request_data["Content"]
                    }
        posts.insert(0, new_post)
        response = Response("", 201, mimetype="application/json")
        response.headers["Location"] = "/books/" + str(new_post["Title"])
        return response
    else:
        help_message = {
                        "error": "Invalid info",
                        "help": """The json given must be in this format{"Author": request_data["Author"],"Title": 
                        request_data["Title"], "posted_on": request_data["posted_on"], "Content": request_data[
                        "Content"]} """
                        }
        response = Response(json.dumps(help_message), status=400, mimetype="application/json")
        return response


@app.route("/posts/<int:posted_on>")
def get_post_posted_on_date(posted_on):
    return_value = {}
    for post in posts:
        if post["posted_on"] == posted_on:
            return_value['Author'] = post["Author"]
            return_value["Title"] = post["Title"]
            return_value["Content"] = post["Content"]
    return jsonify(return_value)


@app.route("/posts/<int:posted_on>", methods=["PUT"])
def edit_books_posted_on_date(posted_on):
    data_update = request.get_json()
    if not valid_put_data(data_update):
        help_message = {
            "error": "Invalid info",
            "help": """The json given must be in this format{"Author": request_data["Author"],"Title":
                                request_data["Title"], "Content": request_data[
                                "Content"]} """
        }
        response = Response(json.dumps(help_message), status=400, mimetype="application/json")
        return response
    for post in posts:
        if posted_on == post["posted_on"]:
            post["Title"] = data_update["Title"]
            post["Author"] = data_update["Author"]
            post["Content"] = data_update["Content"]
            post["posted_on"] = posted_on
    response = Response("", status=204)
    return response


@app.route("/posts/<int:posted_on>", methods=["PATCH"])
def patch_based_on_date(posted_on):
    patch_data = request.get_json()
    for post in posts:
        if post["posted_on"] == posted_on:
            if "Author" in patch_data:
                post["Author"] = patch_data["Author"]
            if "Title" in patch_data:
                post["Title"] = patch_data["Title"]
            if "Content" in patch_data:
                post["Content"] = patch_data["Content"]
            else:
                help_msg = {
                    "error": "no match",
                    "message": "Please enter values with keys as expected"
                }
                response = Response(json.dumps(help_msg), status=400)
                return response
            response = Response("", status=204)
            response.headers["Location"] = "/posts/" + str(post["posted_on"])
            return response


@app.route("/posts/<int:posted_on>", methods=["DELETE"])
def delete_by_given_data(posted_on):
    index_of_book = 0
    for post in posts:
        if post["posted_on"] == posted_on:
            posts.pop(index_of_book)
            response = Response("", status=204)
            return response
        index_of_book = index_of_book + 1
    help_message = {
        "message": "No data found in the particular year"
    }
    response = Response(json.dumps(help_message), status=404, mimetype='application/json')
    return response


def valid_data(bookobject):
    if "Author" in bookobject and 'Title' in bookobject and 'posted_on' in bookobject and 'Content' in bookobject:
        return True
    else:
        return False


def valid_put_data(bookobject):
    if "Author" in bookobject and 'Title' in bookobject and 'Content' in bookobject:
        return True
    else:
        return False


if __name__ == "__main__":
    app.run(debug=True)



