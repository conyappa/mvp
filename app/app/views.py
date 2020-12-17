from django.shortcuts import redirect


def trigger_exception(_request):
    raise Exception()


def landing_page(_request):
    return redirect("https://www.facebook.com/conyappa/")
