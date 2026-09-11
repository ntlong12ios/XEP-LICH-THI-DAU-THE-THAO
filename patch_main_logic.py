import codecs
import re

with codecs.open('backend/main.py', 'r', 'utf-8') as f:
    text = f.read()

# Fix categories
text = text.replace('cat_id = 3\n                elif "N? TK" in match_code', 'cat_id = 2\n                elif "N? TK" in match_code')
text = text.replace('cat_id = 5\n                else:\n                    fill = cell.fill', 'cat_id = 4\n                else:\n                    fill = cell.fill')
text = text.replace('if fill.start_color.theme == 3: cat_id = 3', 'if fill.start_color.theme == 3: cat_id = 2')
text = text.replace('elif fill.start_color.theme == 9 or fill.start_color.theme == 5: cat_id = 5', 'elif fill.start_color.theme == 9 or fill.start_color.theme == 5: cat_id = 4')
text = text.replace("if fill.start_color.rgb == 'FFFFFF00': cat_id = 4", "if fill.start_color.rgb == 'FFFFFF00': cat_id = 3")

# Fix return message safely
def replacer(m):
    return 'return {"message": f"\\u0110\\u00e3 \\u0111\\u1ed3ng b\\u1ed9 {updates_made} l\\u1ecbch thi \\u0111\\u1ea5u t\\u1eeb Agenda Excel!"}'

text = re.sub(r'return \{"message": f".*? Agenda Excel!"\}', replacer, text)

with codecs.open('backend/main.py', 'w', 'utf-8') as f:
    f.write(text)

print("Patch applied")
