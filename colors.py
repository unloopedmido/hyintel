def parse_minecraft_text(text: str, base_color: str = None) -> str:
    """
    Returns the MC text but formatted with HTML spans for Minecraft's color and formatting codes
    """
    colors = {
        "0": "#000000",
        "1": "#0000AA",
        "2": "#00AA00",
        "3": "#00AAAA",
        "4": "#AA0000",
        "5": "#AA00AA",
        "6": "#FFAA00",
        "7": "#AAAAAA",
        "8": "#555555",
        "9": "#5555FF",
        "a": "#55FF55",
        "b": "#55FFFF",
        "c": "#FF5555",
        "d": "#FF55FF",
        "e": "#FFFF55",
        "f": "#FFFFFF",
    }
    
    formats = {
        "k": "obfuscated",  # Note: obfuscated doesn't have CSS equivalent, will need JavaScript
        "l": "font-weight: bold;",
        "m": "text-decoration: line-through;",
        "n": "text-decoration: underline;",
        "o": "font-style: italic;",
        "r": "reset"
    }
    
    result = ""
    current_span = False
    current_style = f"color: {base_color};" if base_color else "color: #FFFFFF;"
    
    i = 0
    
    while i < len(text):
        char = text[i]
        
        # Handle special characters
        if char in ["✪", "➊", "➋", "➌", "➍", "➎"]:
            color = "#FFD700" if char == "✪" else "#FF5555"
            result += f"<span style='color: {color};'>{char}</span>"
            i += 1
            continue
            
        # Handle section symbol and color codes
        if char == "§" and i + 1 < len(text):
            if current_span:
                result += "</span>"
                current_span = False
                
            code = text[i + 1].lower()
            
            if code in colors:
                current_style = f"color: {colors[code]};"
            elif code in formats:
                if code == "r":
                    current_style = f"color: {base_color};" if base_color else "color: #FFFFFF;"
                else:
                    current_style += formats[code]
            
            result += f"<span style='{current_style}'>"
            current_span = True
            i += 2  # Skip both the § and the code character
            continue
            
        # Regular character
        if not current_span:
            result += f"<span style='{current_style}'>"
            current_span = True
        
        result += char
        i += 1
        
    if current_span:
        result += "</span>"
    
    return result