# Netlify 构建设置指南

如果您在 Netlify 的 Build & deploy 页面下找不到 Build settings 选项，请按照以下步骤操作：

## 1. 确认您已选择正确的站点
- 登录 Netlify 后，确保您已在侧边栏中选择了正确的站点
- 在站点概览页面，点击顶部导航栏的 "Site settings"（站点设置）

## 2. 导航到 Build 设置
在 Site settings 中，您可以在左侧菜单中找到 "Build & deploy" 部分。通常情况下，Build settings 应该是这个部分下的第一个选项。

## 3. 如果仍然看不到 Build settings
- 尝试刷新页面（F5 或 Ctrl+R）
- 确认您的 Netlify 账户具有该站点的管理员权限
- 检查 Netlify 界面是否已经更新（Netlify 会定期更新界面布局）

## 4. 替代方法：使用 netlify.toml 文件
由于我们已经在项目根目录创建了 `netlify.toml` 文件，该文件包含了所有必要的构建设置，所以您也可以通过编辑该文件来配置构建参数：

```toml
[build]
  publish = "."  # 发布目录
  command = ""    # 构建命令（留空表示纯静态网站）
```

## 5. 常见问题解决方案
- **Publish directory 设置**：确保 Netlify 控制台中的 Publish directory 与 `netlify.toml` 文件中的 `publish` 值一致（都设置为 "."）
- **自动部署**：在 Continuous deployment 部分启用自动部署功能
- **构建设置冲突**：如果控制台设置与 `netlify.toml` 文件冲突，通常以 `netlify.toml` 文件为准

## 6. 验证部署设置
完成设置后，您可以：
1. 点击 "Deploy site" 手动触发一次部署
2. 检查部署日志，确保没有错误
3. 访问您的 Netlify 域名，确认网站可以正常访问

如果您仍然遇到问题，可以查看 Netlify 的官方文档或联系他们的支持团队。