# Vercel 部署依赖安装问题修复

## 问题分析

根据 Vercel 日志，错误信息是：
```
ModuleNotFoundError: No module named 'flask'
```

这说明 Vercel 在部署时没有正确安装 `requirements.txt` 中的依赖。

## 可能的原因

1. **`requirements.txt` 文件位置**：必须位于项目根目录（✓ 已确认存在）
2. **文件格式**：`requirements.txt` 格式必须正确（✓ 已确认格式正确）
3. **Vercel 自动检测**：Vercel 应该自动检测 Python 项目并安装依赖

## 解决方案

### 方案 1：确保 requirements.txt 格式正确（已完成）

`requirements.txt` 文件已存在且格式正确，包含所有必要的依赖。

### 方案 2：添加 runtime.txt（已完成）

已创建 `runtime.txt` 文件指定 Python 版本：
```
python-3.9
```

### 方案 3：检查 Vercel 项目设置

1. 登录 Vercel Dashboard
2. 进入项目设置
3. 检查 "Build & Development Settings"
4. 确保 "Framework Preset" 设置为 "Other" 或 "Python"
5. 确保 "Root Directory" 设置为项目根目录

### 方案 4：重新部署

在修复配置后，需要重新部署：

```bash
# 如果使用 Vercel CLI
vercel --prod

# 或者通过 Git push 触发自动部署
git add vercel.json runtime.txt requirements.txt
git commit -m "Fix Vercel deployment dependencies"
git push
```

### 方案 5：检查构建日志

在 Vercel Dashboard 中查看构建日志，确认：
1. Vercel 是否检测到了 `requirements.txt`
2. 是否执行了 `pip install -r requirements.txt`
3. 是否有任何安装错误

## 验证步骤

部署后，检查：
1. 访问应用 URL，应该不再出现 `ModuleNotFoundError`
2. 查看 Vercel 构建日志，确认依赖安装成功
3. 如果仍有问题，检查运行时日志中的详细错误信息

## 注意事项

- `requirements.txt` 必须位于项目根目录
- 确保所有依赖版本兼容
- 测试依赖（如 `pytest`）在生产环境中不会被安装，这是正常的
- 如果使用 `runtime.txt`，确保 Python 版本与本地开发环境兼容

