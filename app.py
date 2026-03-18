from mcp.server.fastmcp import FastMCP
from typing import Literal
import psutil

# MCP 서버 이름 설정
mcp = FastMCP("HouseControl")
@mcp.tool()
def classify_command(
    target: Literal["light", "appliance"]
):
    """
    사용자의 요청이 조명인지 전자제품인지 분류합니다.
    """
    return {"target": target}

@mcp.tool()
def control_light(
    room: Literal["주방", "현관",'안방','작은방','거실','화장실'],#str,
    onoff: Literal["on", "off"]
):
    """
    특정 장소의 조명, 불을 켜거나 끕니다
    가전제품은 제외합니다.

    - room  : 조명을 제어할 장소 이름 (예: 거실, 안방, 침실)
        표준 장소:
        - "주방": 부엌, 키친, kitchen, 조리실을 의미하는 모든 표현
        - "거실": 거실, 리빙룸, living room, 응접실을 의미하는 모든 표현
    
    - onoff: Literal["on", "off"]
        - "on": 조명 켜기
        - "off": 조명 끄기
    
    """
    print(f"[MCP] {room} 조명 → {onoff}")

    # 실제 하드웨어 / API 연동 위치
    # e.g. smart_home.turn_light(room, onoff)

    return {
        "room": room,
        "status": onoff,
        "result": "success"
    }

APPLIANCE_STATE = {}

@mcp.tool()
def control_appliance(
    appliance: Literal['냉장고','세탁기','온수기','TV','전자렌지'],#str,
    action: Literal["on", "off", "toggle", "status"],
    intensity: int = 100
):
    """
    가전 제품을 제어합니다, 특정장소의 조명은 제외합니다.
    
    - appliance: 제어할 가전 이름 (예: TV, 에어컨, 냉장고)
    - action
        - "on" : 가전 켜기
        - "off" : 가전 끄기
        - "toggle" : 가전 상태 토글
        - "status" : 현재 상태 조회
    
    - intensity: 전원 켤 때의 세기(0-100, 기본 100)
    """
    intensity = max(0, min(100, int(intensity)))
    state = APPLIANCE_STATE.get(appliance, {"power": "off", "intensity": 0})

    if action == "status":
        return {"appliance": appliance, "power": state["power"], "intensity": state["intensity"]}

    if action == "toggle":
        new_power = "on" if state["power"] == "off" else "off"
    elif action == "on":
        new_power = "on"
    else:
        new_power = "off"

    new_intensity = intensity if new_power == "on" else 0
    APPLIANCE_STATE[appliance] = {"power": new_power, "intensity": new_intensity}

    print(f"[MCP] {appliance} → {new_power} (intensity={new_intensity})")
    return {"appliance": appliance, "power": new_power, "intensity": new_intensity, "result": "success"}

if __name__ == "__main__":
    mcp.run()