from Models import Post
from flask_login import login_user, current_user, login_required, logout_user
from flask import Blueprint, render_template, request
from blog.posts.forms import SearchForm


main = Blueprint('main', __name__)

@main.context_processor
def base():
    form=SearchForm
    return dict(form=form)

@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home.html', title='Home')

@main.route('/admin/')
@login_required
def admin():
    return render_template('admin.html', title='Admin Page')


@main.route('/blogs')
@login_required
def blog_page():
    search_form = SearchForm()
    page=request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', posts=posts, title='Blogs',search_form=search_form)

