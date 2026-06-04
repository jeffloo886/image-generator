# GPT Image 2 生图网站

使用 GPT Image 2 模型生成高质量图片的 Web 应用。

## 功能特点

- 🎨 使用最新的 GPT Image 2 模型
- 📐 支持多种尺寸（1024x1024、1792x1024、1024x1792）
- ✨ 支持标准和高清两种质量
- 💾 自动保存生成的图片
- 📜 查看历史生成记录
- 📥 一键下载图片

## 安装步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置 OpenAI API Key：
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 OpenAI API Key
export OPENAI_API_KEY=your_api_key_here
```

3. 运行应用：
```bash
python app.py
```

4. 打开浏览器访问：
```
http://localhost:2345
```

## 使用说明

1. 在文本框中输入图片描述
2. 选择图片尺寸和质量
3. 点击"生成图片"按钮
4. 等待生成完成后可以查看和下载图片
5. 历史记录会显示在页面下方

## 注意事项

- 需要有效的 OpenAI API Key
- GPT Image 2 模型需要付费使用
- 生成的图片会保存在 `generated_images` 目录

## 技术栈

- Backend: Flask (Python)
- Frontend: HTML + CSS + JavaScript
- AI Model: GPT Image 2 (OpenAI)