def color_text(text, style=None, color=None, backcolor=None):
    styles = {"no effect": 0, "bold": 1, "underline": 2, "negative1": 3, "negative2": 5}
    colors = {"black": 30, "red": 31, "green": 32, "yellow": 33, "blue": 34, "purple": 35, "cyan": 36, "white": 37}
    backcolors = {"black": 40, "red": 41, "green": 42, "yellow": 43, "blue": 44, "purple": 45, "cyan": 46, "white": 47}

    style = styles[style.lower().strip()] if style is not None else ''
    color = f';{colors[color.lower().strip()]}' if color is not None else ''
    backcolor = f';{backcolors[backcolor.lower().strip()]}' if backcolor is not None else ''

    return f"\033[{style}{color}{backcolor}m{text}\033[0m"
