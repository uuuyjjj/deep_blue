from app import app, db, Note, Tag
from datetime import datetime, timedelta

# 使用应用上下文
with app.app_context():
    # 确保数据库表已创建
    db.create_all()
    
    # 检查是否已有示例数据
    if Note.query.first() is None:
        print("添加示例笔记数据...")
        
        # 创建一些示例标签
        tag_python = Tag(name='Python')
        tag_flask = Tag(name='Flask')
        tag_sql = Tag(name='SQL')
        tag_javascript = Tag(name='JavaScript')
        tag_css = Tag(name='CSS')
        
        # 添加标签到数据库
        db.session.add_all([tag_python, tag_flask, tag_sql, tag_javascript, tag_css])
        db.session.commit()
        
        # 创建示例笔记 1: Python基础语法
        note1 = Note(
            title='Python基础语法笔记',
            content='## Python基础语法\n\nPython是一种易学易用的编程语言。\n\n### 变量和数据类型\n\n- 整数: `123`\n- 浮点数: `3.14`\n- 字符串: `"Hello, World!"`\n\n### 控制流\n\n```python\nif condition:\n    # do something\nelif another_condition:\n    # do something else\nelse:\n    # do something different\n```\n\n#Python #编程基础',
            created_at=datetime.utcnow() - timedelta(days=5),
            updated_at=datetime.utcnow() - timedelta(days=2)
        )
        note1.tags.append(tag_python)
        
        # 创建示例笔记 2: Flask入门
        note2 = Note(
            title='Flask Web框架入门',
            content='## Flask入门指南\n\nFlask是一个轻量级的Python Web框架。\n\n### 安装\n\n```bash\npip install flask\n```\n\n### 简单示例\n\n```python\nfrom flask import Flask\napp = Flask(__name__)\n\n@app.route('/')\ndef hello():\n    return "Hello, World!"\n\nif __name__ == '__main__':\n    app.run(debug=True)\n```\n\n### 路由和视图\n- 使用`@app.route()`装饰器定义路由\n- 视图函数返回响应内容\n\n#Flask #Web开发 #Python',
            created_at=datetime.utcnow() - timedelta(days=3),
            next_review=datetime.utcnow() + timedelta(days=1)  # 设置复习时间
        )
        note2.tags.append(tag_flask)
        note2.tags.append(tag_python)
        
        # 创建示例笔记 3: SQL查询基础
        note3 = Note(
            title='SQL查询基础教程',
            content='## SQL查询语句\n\nSQL是用于管理关系型数据库的标准语言。\n\n### 基本查询\n\n```sql\nSELECT column1, column2\nFROM table_name\nWHERE condition;\n```\n\n### 常用操作\n\n- **SELECT**: 选择数据\n- **INSERT**: 插入数据\n- **UPDATE**: 更新数据\n- **DELETE**: 删除数据\n\n### 过滤和排序\n\n```sql\nSELECT * FROM users\nWHERE age > 18\nORDER BY name ASC;\n```\n\n#SQL #数据库',
            created_at=datetime.utcnow() - timedelta(days=1)
        )
        note3.tags.append(tag_sql)
        
        # 创建示例笔记 4: JavaScript DOM操作
        note4 = Note(
            title='JavaScript DOM操作技巧',
            content='## JavaScript DOM操作\n\nDOM (Document Object Model) 是HTML和XML文档的编程接口。\n\n### 选择元素\n\n```javascript\n// 通过ID选择\ndocument.getElementById('elementId');\n\n// 通过类名选择\ndocument.getElementsByClassName('className');\n\n// 通过标签名选择\ndocument.getElementsByTagName('tagName');\n\n// 通过CSS选择器选择\ndocument.querySelector('.class');\ndocument.querySelectorAll('div');\n```\n\n### 事件处理\n\n```javascript\nelement.addEventListener('click', function() {\n    // 处理点击事件\n});\n```\n\n#JavaScript #前端开发',
            created_at=datetime.utcnow(),
            next_review=datetime.utcnow() - timedelta(days=1)  # 已到期需要复习
        )
        note4.tags.append(tag_javascript)
        
        # 创建示例笔记 5: CSS布局技巧
        note5 = Note(
            title='CSS布局技巧总结',
            content='## CSS布局技巧\n\n### Flexbox布局\n\nFlexbox是一种一维布局模型，适合排列行或列的元素。\n\n```css\n.container {\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n}\n```\n\n### Grid布局\n\nGrid是一种二维布局模型，可以同时处理行和列。\n\n```css\n.container {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n    grid-gap: 20px;\n}\n```\n\n#CSS #前端开发',
            created_at=datetime.utcnow()
        )
        note5.tags.append(tag_css)
        
        # 添加所有笔记到数据库
        db.session.add_all([note1, note2, note3, note4, note5])
        db.session.commit()
        
        print("示例数据添加成功！")
    else:
        print("数据库中已有数据，跳过示例数据添加。")