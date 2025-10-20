#!/usr/bin/env python3
"""
简单二维码生成工具
"""

import qrcode
import socket

def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.100"

def main():
    # 获取本机IP
    local_ip = get_local_ip()
    url = f"http://{local_ip}:8080"
    
    # 创建二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # 生成图片
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 保存
    filename = "meeting_room_qr.png"
    img.save(filename)
    
    print("="*50)
    print("会议室预约系统二维码生成完成")
    print("="*50)
    print(f"二维码文件: {filename}")
    print(f"访问地址: {url}")
    print("\n请将二维码打印并张贴在211会议室门口")

if __name__ == "__main__":
    main()
