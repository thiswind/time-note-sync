# 测试指南

## 当前状态

✅ **Phase 1 & 2**: 基础架构已完成
✅ **Phase 3 (MVP)**: 日志条目 CRUD 功能已完成

## 测试环境设置

### 已完成的设置

1. ✅ Python 依赖已安装（Flask, SQLAlchemy, Flask-Login 等）
2. ✅ Node.js 依赖已安装（Vue.js, Vant 等）
3. ✅ 数据库已初始化（SQLite）
4. ✅ 测试用户已创建

### 测试用户信息

- **用户名**: `testuser`
- **密码**: `testpass`

## 启动服务

### 方法 1: 使用启动脚本（推荐）

**启动后端服务**:
```bash
cd backend
conda activate base
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=dev-secret-key
python app.py
```

**启动前端服务**（新终端）:
```bash
cd frontend
npm run dev
```

### 方法 2: 手动启动

后端服务将在 `http://localhost:5000` 运行
前端服务将在 `http://localhost:3000` 运行

## 测试步骤

### 1. 访问应用

打开浏览器访问: `http://localhost:3000`

### 2. 测试功能

#### 创建日志条目
1. 点击右上角的 "+" 按钮
2. 输入内容（必填）
3. 可选：输入标题、选择日期
4. 点击"创建"按钮
5. 验证条目出现在列表中

#### 查看日志列表
1. 在首页查看所有日志条目
2. 切换到"今天"标签查看今天的条目
3. 验证列表显示正确

#### 编辑日志条目
1. 点击列表中的任意条目
2. 修改标题、内容或日期
3. 点击"保存"按钮
4. 验证更改已保存

#### 删除日志条目
1. 打开一个日志条目
2. 点击"删除"按钮
3. 确认删除
4. 验证条目已从列表中移除

### 3. API 测试（可选）

使用 curl 或 Postman 测试 API:

```bash
# 健康检查
curl http://localhost:5000/health

# 登录（需要先实现登录端点）
# 创建日志条目
curl -X POST http://localhost:5000/api/journal/entries \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Entry","content":"Test content","date":"2025-11-17"}'

# 获取日志列表
curl http://localhost:5000/api/journal/entries
```

## 已知问题

1. **认证功能未实现**: 目前 API 端点需要 `@login_required`，但登录页面/端点还未实现
   - **临时解决方案**: 可以暂时注释掉 `@login_required` 装饰器进行测试
   - **或者**: 先实现简单的登录功能

2. **CalDAV 依赖**: caldav 和 ics 库已注释，将在 Phase 5 实现日历同步时安装

## 下一步

- [ ] 实现登录功能（或临时移除认证要求进行测试）
- [ ] 测试所有 CRUD 操作
- [ ] 验证 iOS 风格 UI 显示正确
- [ ] 继续实现 Phase 4（按日期浏览）

## 停止服务

按 `Ctrl+C` 停止服务，或使用：

```bash
# 查找并停止 Flask 进程
pkill -f "python app.py"

# 查找并停止 Vite 进程
pkill -f "vite"
```





