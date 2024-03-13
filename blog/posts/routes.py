from flask import Blueprint, abort, request, render_template, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user, current_user, login_required, logout_user
from Models import User, Post
from blog import db, mail, ckeditor
from blog.posts.forms import PostForm, SearchForm
from blog.posts.utils import *


posts= Blueprint('posts', __name__)

@posts.route("/search_results")
def search_results():
        search_query = request.args.get('search', '')
 
        results = Post.query.filter(
        (Post.title.ilike(f"%{search_query}%")) |
        (Post.author.has(User.username.ilike(f"%{search_query}%"))) |
        (Post.content.ilike(f"%{search_query}%"))
    ).all()
        results = results.order_by(Post.title).all()
        return render_template('search_results.html', results=results, search_query=search_query)



@posts.route('/post/new', methods =['POST', 'GET'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data, image_file=save_picture_post(form.image_file.data), content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('main.blog_page'))
    return render_template("new_post.html", form=form, title='New Post', legend='Create New Post')


@posts.route('/post/<int:post_id>', methods =['POST', 'GET'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html',title=post.title, post=post, legend=' Post')


@posts.route('/post/<int:post_id>/update', methods =['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('updatepost.html', form=form, title='Update Post', legend='Update Post')



@posts.route('/post/<int:post_id>/delete', methods =['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('main.blog_page'))


