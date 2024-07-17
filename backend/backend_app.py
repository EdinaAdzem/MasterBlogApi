from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """add post endpoint"""
    data = request.get_json()
    if 'title' not in data or 'content' not in data:
        missing_fields = []
        if 'title' not in data:
            missing_fields.append('title')
        if 'content' not in data:
            missing_fields.append('content')
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400  # handle errors

    # add a new post
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


# delete endpoint
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """delete post endpoint"""
    global POSTS
    # first attempt to find the post
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({"message": f"Post  id {post_id} has been deleted successfully."}), 200
        # handle user entering the wrong id
    return jsonify({"error": f"Post id {post_id} does not exist!!!."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    update_post = None

    # locate the posts
    for post in POSTS:
        post['title'] = data.get('title', post['title'])  # update title
        post['content'] = data.get('content', post['content'])  # update content
        updated_post = post
        break

    # handle the errors
    if updated_post:
        return jsonify(updated_post), 200
    else:
        return jsonify({"Some Error": f"post id {post_id}does not exist"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
