import codecs

with codecs.open('backend/main.py', 'r', 'utf-8') as f:
    text = f.read()

# I will find the spot right after:
#             if cat_id is not None:
# and insert the mapping logic.

mapping_logic = """            if cat_id is not None:
                if match_code == "3-4" or match_code == "Tranh 3-4" or match_code == "Ba-T\\u01b0" or match_code == "Tranh h\\u1ea1ng 3":
                    if cat_id == 1:
                        match_code = "Tranh h\\u1ea1ng 3"
                    elif cat_id == 2:
                        match_code = "Nam 3-4"
                    elif cat_id == 4:
                        match_code = "N\\u1eef 3-4"
                    elif cat_id == 3:
                        match_code = "N.N\\u1eef 3-4"
"""

text = text.replace('            if cat_id is not None:', mapping_logic)

with codecs.open('backend/main.py', 'w', 'utf-8') as f:
    f.write(text)

print("Mapping patch applied.")
