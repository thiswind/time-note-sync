# Vercel 部署测试说明

## 问题

Vercel 部署保护（Deployment Protection）已启用，导致自动化测试无法访问部署的应用。

## 解决方案

### 方案 1：禁用部署保护（推荐用于测试）

1. 登录 Vercel Dashboard
2. 进入项目设置
3. 找到 "Deployment Protection" 或 "Security" 设置
4. 禁用部署保护（或设置为 "None"）

### 方案 2：使用本地服务器进行测试（推荐）

运行本地服务器进行 Playwright 测试：

```bash
# 启动本地服务器（在另一个终端）
python3 app.py

# 运行测试（不设置 VERCEL_URL）
npx playwright test --reporter=list
```

### 方案 3：使用 Bypass Token（用于 CI/CD）

如果需要保持部署保护，可以获取 bypass token：

1. 在 Vercel Dashboard 中获取 bypass token
2. 在测试中使用 token 访问：

```bash
VERCEL_BYPASS_TOKEN=your_token npx playwright test
```

然后在测试代码中添加 cookie：

```javascript
await page.context().addCookies([{
  name: 'x-vercel-protection-bypass',
  value: process.env.VERCEL_BYPASS_TOKEN,
  domain: 'time-note-sync-bnlr1148a-thiswinds-projects.vercel.app',
  path: '/'
}]);
```

## 当前建议

**推荐使用方案 2（本地服务器测试）**，因为：
- 不需要修改 Vercel 设置
- 测试速度更快
- 不依赖外部服务
- 可以完全控制测试环境

