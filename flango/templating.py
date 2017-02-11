from django.shortcuts import render

from flango import request


def render_template(template_name, **context):
    return render(request, template_name, context)
