import json
import logging
from datetime import datetime
from urllib import request
from urllib.error import HTTPError, URLError

from config import APP_BASE_URL, FEISHU_WEBHOOK_URL, ROOM_211_NUMBER

logger = logging.getLogger(__name__)


def _format_booking_message(event_name: str, booking: dict) -> str:
    booking_link = f"\n系统地址: {APP_BASE_URL}" if APP_BASE_URL else ""
    department = booking.get("department") or "未填写"
    status = booking.get("status") or "pending"

    return (
        f"{event_name}\n"
        f"会议室: {ROOM_211_NUMBER}\n"
        f"预约人: {booking.get('user_name', '-')}\n"
        f"部门: {department}\n"
        f"开始时间: {booking.get('start_time', '-')}\n"
        f"结束时间: {booking.get('end_time', '-')}\n"
        f"状态: {status}\n"
        f"操作时间: {datetime.utcnow().isoformat()}{booking_link}"
    )


def send_booking_notification(event_name: str, booking: dict) -> bool:
    if not FEISHU_WEBHOOK_URL:
        return False

    payload = json.dumps({'msg_type': 'text', 'content': {'text': _format_booking_message(event_name, booking)}}).encode('utf-8')
    req = request.Request(
        FEISHU_WEBHOOK_URL,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    try:
        with request.urlopen(req, timeout=8) as response:
            response.read()
        return True
    except (HTTPError, URLError, TimeoutError) as exc:
        logger.warning("Feishu notification failed: %s", exc)
        return False
