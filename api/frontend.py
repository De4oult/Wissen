import jinja2 as jinja


class Frontend:
    def __init__(self) -> None:
        self.environment = jinja.Environment(loader = jinja.FileSystemLoader('./templates/'))
        
        self.layout: str = '''
            <!DOCTYPE html>
            <head>
                <meta charset="utf-8" />
                <title>Wissen</title>
                <script src="https://cdn.tailwindcss.com"></script>
                <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
            </head>
            <body class="bg-slate-100">
                {content}
            </body>
        '''

    def page(self, template: str, data: dict[str, any] = {}) -> str:
        template += '.html' if not template.endswith('.html') else ''

        template = self.environment.get_template(template)

        return self.layout.format(
            content = template.render(data)
        )
    

frontend: Frontend = Frontend()