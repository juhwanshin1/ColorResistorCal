from rich.console import Console
from rich.text import Text

console = Console()

def format_resistance(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000}MΩ", "MΩ"
    elif value >= 1_000:
        return f"{value / 1_000}kΩ", "kΩ"
    return f"{value}Ω", "Ω"

def calculate_tolerance(nominal, measured):
    return abs((measured - nominal) / nominal * 100)

def resistor_value():
    color_codes = {
        "검정": 0, "갈색": 1, "빨강": 2, "주황": 3, "노랑": 4,
        "초록": 5, "파랑": 6, "보라": 7, "회색": 8, "흰색": 9
    }
    multiplier_codes = {
        "검정": 1, "갈색": 10, "빨강": 100, "주황": 1_000, "노랑": 10_000,
        "초록": 100_000, "파랑": 1_000_000, "보라": 10_000_000,
        "회색": 100_000_000, "흰색": 1_000_000_000, "금": 0.1, "은": 0.01
    }
    tolerance_codes = {
        "갈색": 1, "빨강": 2, "초록": 0.5, "파랑": 0.25,
        "보라": 0.1, "회색": 0.05, "금": 5, "은": 10
    }
    rich_colors = {
        "검정": "black", "갈색": "bright_black", "빨강": "red", "주황": "bright_red", 
        "노랑": "yellow", "초록": "green", "파랑": "blue", "보라": "magenta", 
        "회색": "bright_white", "흰색": "white", "금": "bright_yellow", "은": "cyan"
    }
    
    console.print("사용 가능한 색상:")
    color_list = [Text(color, style=rich_colors[color]) for color in color_codes.keys()]
    console.print(*color_list, Text("금", style="bright_yellow"), Text("은", style="cyan"))
    
    colors = input("\n저항기의 색상을 공백으로 구분하여 입력하세요 (4개 또는 5개): ").split()
    
    if len(colors) not in [4, 5]:
        return "잘못된 입력입니다. 4개 또는 5개의 색상을 입력하세요."
    
    band_count = len(colors)
    
    try:
        # 색상을 입력받을 때 색상에 맞는 스타일 적용
        colored_input = Text()
        for color in colors:
            colored_input.append(f"{color} ", style=rich_colors.get(color, "white"))
        
        console.print(f"입력된 색상: {colored_input}")  # 색상 적용된 텍스트 출력
        
        if band_count == 4:
            value = (color_codes[colors[0]] * 10 + color_codes[colors[1]]) * multiplier_codes[colors[2]]
            tolerance = tolerance_codes.get(colors[3], None)
        else:
            value = (color_codes[colors[0]] * 100 + color_codes[colors[1]] * 10 + color_codes[colors[2]]) * multiplier_codes[colors[3]]
            tolerance = tolerance_codes.get(colors[4], None)
        
        formatted_value, unit = format_resistance(value)
        
        # 이후 출력은 기본 색상으로 출력
        if tolerance is not None:
            console.print(f"저항값: {formatted_value} ±{tolerance}%", style="white")
        else:
            console.print(f"저항값: {formatted_value}", style="white")
        
        measured_value = float(input(f"실제 측정된 저항값을 입력하세요 ({unit} 단위): "))
        measured_value *= 1_000_000 if unit == "MΩ" else 1_000 if unit == "kΩ" else 1
        
        error = calculate_tolerance(value, measured_value)
        
        # 측정값과 오차율도 기본 색상으로 출력
        console.print(f"측정값: {format_resistance(measured_value)[0]}", style="white")
        console.print(f"오차율: {error:.2f}%", style="white")
        
        return "계산 완료"
        
    except KeyError:
        return "유효하지 않은 색상이 포함되어 있습니다."
    except ValueError:
        return "잘못된 입력입니다. 숫자를 입력하세요."

# 실행 예시
print(resistor_value())
