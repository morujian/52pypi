from django.shortcuts import render, render_to_response


def about(request):
    return render_to_response("about.html")
