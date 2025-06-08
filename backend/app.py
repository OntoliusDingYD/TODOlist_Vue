from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库配置 - 使用SQLite文件数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化SQLAlchemy
db = SQLAlchemy(app)

# Todo数据模型
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

# 创建数据库表
with app.app_context():
    db.create_all()

# RESTful API路由
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = Todo(title=data['title'])
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
