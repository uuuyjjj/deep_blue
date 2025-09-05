from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库模型定义
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 与标签的多对多关系
    tags = db.relationship('Tag', secondary='note_tags', backref=db.backref('notes', lazy=True))
    
    # 复习相关字段
    next_review = db.Column(db.DateTime)
    review_count = db.Column(db.Integer, default=0)
    last_reviewed = db.Column(db.DateTime)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# 多对多关系表
note_tags = db.Table('note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# 创建数据库表
with app.app_context():
    db.create_all()

# 主页面路由
@app.route('/')
def index():
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    tags = Tag.query.all()
    return render_template('index.html', notes=notes, tags=tags)

# 创建笔记路由
@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # 提取标签（简单实现，从内容中提取#开头的词）
        tag_names = []
        words = content.split()
        for word in words:
            if word.startswith('#') and len(word) > 1:
                tag_name = word[1:].strip('.,;:!?-()[]{}')
                if tag_name not in tag_names:
                    tag_names.append(tag_name)
        
        new_note = Note(title=title, content=content)
        
        # 添加标签
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            new_note.tags.append(tag)
        
        db.session.add(new_note)
        db.session.commit()
        
        flash('笔记创建成功！')
        return redirect(url_for('index'))
    
    return render_template('create_note.html')

# 编辑笔记路由
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.updated_at = datetime.utcnow()
        
        # 清空现有标签
        note.tags = []
        
        # 提取新标签
        tag_names = []
        words = note.content.split()
        for word in words:
            if word.startswith('#') and len(word) > 1:
                tag_name = word[1:].strip('.,;:!?-()[]{}')
                if tag_name not in tag_names:
                    tag_names.append(tag_name)
        
        # 添加新标签
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            note.tags.append(tag)
        
        db.session.commit()
        
        flash('笔记更新成功！')
        return redirect(url_for('index'))
    
    return render_template('edit_note.html', note=note)

# 删除笔记路由
@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    
    flash('笔记已删除！')
    return redirect(url_for('index'))

# 搜索笔记路由
@app.route('/search', methods=['GET'])
def search_notes():
    query = request.args.get('q', '')
    tag_filter = request.args.get('tag', '')
    
    if query and tag_filter:
        # 按关键词和标签搜索
        notes = Note.query.filter(
            Note.content.like(f'%{query}%') | Note.title.like(f'%{query}%'),
            Note.tags.any(Tag.name == tag_filter)
        ).order_by(Note.updated_at.desc()).all()
    elif query:
        # 仅按关键词搜索
        notes = Note.query.filter(
            Note.content.like(f'%{query}%') | Note.title.like(f'%{query}%')
        ).order_by(Note.updated_at.desc()).all()
    elif tag_filter:
        # 仅按标签搜索
        notes = Note.query.filter(
            Note.tags.any(Tag.name == tag_filter)
        ).order_by(Note.updated_at.desc()).all()
    else:
        # 无搜索条件，返回所有笔记
        notes = Note.query.order_by(Note.updated_at.desc()).all()
    
    tags = Tag.query.all()
    return render_template('index.html', notes=notes, tags=tags, search_query=query, selected_tag=tag_filter)

# 设置复习提醒路由
@app.route('/set_review/<int:note_id>', methods=['POST'])
def set_review(note_id):
    note = Note.query.get_or_404(note_id)
    days = int(request.form.get('days', 1))
    
    from datetime import timedelta
    note.next_review = datetime.utcnow() + timedelta(days=days)
    db.session.commit()
    
    return jsonify({'success': True, 'next_review': note.next_review.strftime('%Y-%m-%d')})

# 标记为已复习路由
@app.route('/mark_reviewed/<int:note_id>')
def mark_reviewed(note_id):
    note = Note.query.get_or_404(note_id)
    note.last_reviewed = datetime.utcnow()
    note.review_count += 1
    
    # 简单的间隔重复算法：每次复习后，下次复习间隔翻倍
    from datetime import timedelta
    days = min(30, 1 * (2 ** (note.review_count - 1)))
    note.next_review = datetime.utcnow() + timedelta(days=days)
    
    db.session.commit()
    flash('已标记为复习完成！')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)