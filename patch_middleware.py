import os

path = r'd:\APP LONG VIET\XEP LICH THI DAU THE THAO\backend\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

middleware_code = """
# Vercel ASGI Prefix Stripper
class StripAPIPrefixMiddleware:
    def __init__(self, app):
        self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["path"].startswith("/api/"):
            scope = dict(scope)
            scope["path"] = scope["path"][4:]
        await self.app(scope, receive, send)

app = StripAPIPrefixMiddleware(app)
"""

if 'StripAPIPrefixMiddleware' not in content:
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + middleware_code + '\n')
    print('Added middleware')
else:
    print('Middleware already exists')
