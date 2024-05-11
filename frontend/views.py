from django.shortcuts import render


def index(request, *args, **kwargs):
    """
    Returns the rendered index.html template.

    :param request: The request for the index page.
    :param args: Any extra arguments.
    :param kwargs: Any extra keyword arguments.
    :return: The rendered index page.
    """
    return render(request, "index.html")
