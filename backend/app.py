from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_cors import CORS

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库配置 - 使用SQLite文件数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化SQLAlchemy
db = SQLAlchemy(app)

# 创建数据库表
with app.app_context():
    db.create_all()

# RESTful API路由
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)  # 使用本地时间
    due_time = db.Column(db.DateTime, nullable=True)

    default_due_timedelta = timedelta(days=3)

    def to_dict(self):
        # 修复逻辑：只有当due_time为空时才使用默认值
        due_time_value = self.due_time if self.due_time else (self.created_at + self.default_due_timedelta)
        
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'due_time': due_time_value.isoformat()
        }

# 修改创建TODO的API
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    # 创建新的Todo实例
    todo = Todo(title=data['title'].strip())
    
    # 如果提供了截止时间，设置它
    if 'due_time' in data and data['due_time']:
        try:
            # 直接解析前端发送的本地时间（不转换时区）
            # 前端发送的是本地时间的ISO字符串，不带时区信息
            due_time_str = data['due_time']
            if due_time_str.endswith('Z'):
                due_time_str = due_time_str[:-1]  # 移除Z后缀
            todo.due_time = datetime.fromisoformat(due_time_str)
        except ValueError as e:
            return jsonify({'error': f'Invalid due_time format: {str(e)}'}), 400
    
    # 如果没有提供截止时间，due_time保持为None，to_dict()会使用默认值
    
    try:
        db.session.add(todo)
        db.session.commit()
        return jsonify(todo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create todo: {str(e)}'}), 500

# 获取所有TODO的API
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

# 删除TODO的API
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    try:
        db.session.delete(todo)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete todo'}), 500

# 更新TODO状态的API
@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    
    if 'completed' in data:
        todo.completed = bool(data['completed'])
    
    if 'title' in data:
        todo.title = data['title'].strip()
    
    if 'due_time' in data:
        if data['due_time']:
            try:
                due_time_str = data['due_time']
                if due_time_str.endswith('Z'):
                    due_time_str = due_time_str[:-1]
                todo.due_time = datetime.fromisoformat(due_time_str)
            except ValueError:
                return jsonify({'error': 'Invalid due_time format'}), 400
        else:
            todo.due_time = None
    
    try:
        db.session.commit()
        return jsonify(todo.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update todo'}), 500

if __name__ == '__main__':
    app.run(debug=True)