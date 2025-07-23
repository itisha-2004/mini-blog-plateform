from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from . import blog_bp
from ..models import Post, Comment, db
from .forms import PostForm, CommentForm
from flask import Blueprint

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)

@blog_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.index'))
    return render_template('create_post.html', form=form)

@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(content=form.content.data, user=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blog.post_detail', post_id=post.id))
    return render_template('post_detail.html', post=post, form=form)

@blog_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("Not authorized!")
        return redirect(url_for('blog.index'))
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('blog.post_detail', post_id=post.id))
    return render_template('edit_post.html', form=form)

@blog_bp.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
    else:
        flash("You can only delete your own posts.")
    return redirect(url_for('blog.index'))

@blog_bp.route('/profile')
@login_required
def profile():
    posts = current_user.posts.order_by(Post.id.desc()).all()
    return render_template('profile.html', posts=posts)
