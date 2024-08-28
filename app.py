from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Load blog posts from JSON file
def load_posts():
    if os.path.exists('posts.json'):
        with open('posts.json', 'r') as file:
            return json.load(file)
    return []

# Save blog posts to JSON file
def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file)

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        new_post = {
            'id': len(posts) + 1,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post = next((post for post in posts if post['id'] == post_id), None)
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)