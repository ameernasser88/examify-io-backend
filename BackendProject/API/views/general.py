import markdown
import os
from django.http import HttpResponse

def index(request):
    with open(os.path.join( os.getcwd(), '..', 'README.md' ), 'r') as file:
        md_text = file.read()
    html = markdown.markdown(md_text)
    return HttpResponse(html)
