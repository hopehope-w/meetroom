#!/usr/bin/env python3
"""
二维码生成工具
生成会议室预约系统的访问二维码
"""

import qrcode
import socket
from PIL import Image, ImageDraw, ImageFont
import os


def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        # 连接到一个远程地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.100"  # 默认IP


def generate_qr_code(url, filename="meeting_room_qr.png"):
    """生成二维码图片"""

    # 创建二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 生成二维码图片
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # 创建一个更大的画布，用于添加文字
    canvas_width = 400
    canvas_height = 500
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")

    # 将二维码居中放置
    qr_width, qr_height = qr_img.size
    qr_x = (canvas_width - qr_width) // 2
    qr_y = 50
    canvas.paste(qr_img, (qr_x, qr_y, qr_x + qr_width, qr_y + qr_height))

    # 添加文字
    draw = ImageDraw.Draw(canvas)

    try:
        # 尝试使用系统字体
        title_font = ImageFont.truetype("arial.ttf", 24)
        url_font = ImageFont.truetype("arial.ttf", 16)
        desc_font = ImageFont.truetype("arial.ttf", 14)
    except:
        # 如果没有找到字体，使用默认字体
        title_font = ImageFont.load_default()
        url_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()

    # 标题
    title_text = "211会议室预约系统"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (canvas_width - title_width) // 2
    draw.text((title_x, 10), title_text, fill="black", font=title_font)

    # URL
    url_bbox = draw.textbbox((0, 0), url, font=url_font)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (canvas_width - url_width) // 2
    draw.text((url_x, qr_y + qr_height + 20), url, fill="blue", font=url_font)

    # 说明文字
    desc_lines = [
        "扫描二维码访问预约系统",
        "或在浏览器中输入上方网址",
        "",
        "使用说明：",
        "1. 填写预约人姓名和部门",
        "2. 选择会议开始和结束时间",
        "3. 提交预约等待管理员审批",
        "4. 系统会自动检测时间冲突",
    ]

    y_offset = qr_y + qr_height + 60
    for line in desc_lines:
        if line:  # 非空行
            line_bbox = draw.textbbox((0, 0), line, font=desc_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (canvas_width - line_width) // 2
            draw.text((line_x, y_offset), line, fill="black", font=desc_font)
        y_offset += 25

    # 保存图片
    canvas.save(filename, "PNG", quality=95)
    print(f"二维码已生成: {filename}")
    print(f"访问地址: {url}")
    return filename


def main():
    """主函数"""
    # 获取本机IP
    local_ip = get_local_ip()

    # 生成访问URL
    url = f"http://{local_ip}:8080"

    # 生成二维码
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qr_filename = os.path.join(script_dir, "meeting_room_qr.png")

    generate_qr_code(url, qr_filename)

    print("\n" + "=" * 50)
    print("会议室预约系统二维码生成完成")
    print("=" * 50)
    print(f"二维码文件: {qr_filename}")
    print(f"访问地址: {url}")
    print("\n请将二维码打印并张贴在211会议室门口")
    print("员工可扫码或直接访问网址进行预约")


if __name__ == "__main__":
    main()
