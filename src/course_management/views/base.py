from django.shortcuts import render


def render_with_default(request, template, context):
    return render(request, template, context)
