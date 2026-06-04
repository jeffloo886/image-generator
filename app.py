from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
import os
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import requests

app = Flask(__name__)


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

# 创建图片保存目录
os.makedirs("generated_images", exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_image():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        size = data.get("size", "1024x1024")
        quality = data.get("quality", "standard")

        if not prompt:
            return jsonify({"error": "请输入图片描述"}), 400

        client = get_openai_client()
        if client is None:
            return jsonify({"error": "请配置 OPENAI_API_KEY"}), 503

        # 调用 GPT Image 2 API
        response = client.images.generate(
            model="gpt-image-2", prompt=prompt, size=size, quality=quality, n=1
        )

        # 获取图片 URL
        image_url = response.data[0].url

        # 下载并保存图片
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))

        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_images/img_{timestamp}.png"
        img.save(filename)

        # 转换为 base64 返回给前端
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        return jsonify(
            {
                "success": True,
                "image": f"data:image/png;base64,{img_base64}",
                "filename": filename,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history")
def get_history():
    try:
        images = []
        if os.path.exists("generated_images"):
            files = sorted(os.listdir("generated_images"), reverse=True)
            for file in files[:20]:  # 最多返回20张
                if file.endswith(".png"):
                    images.append(file)
        return jsonify({"images": images})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/image/<filename>")
def get_image(filename):
    try:
        if ".." in filename or "/" in filename or "\\" in filename:
            return jsonify({"error": "invalid filename"}), 400
        return send_file(f"generated_images/{filename}", mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2345, debug=True)
