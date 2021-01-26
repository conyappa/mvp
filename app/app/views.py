from django.shortcuts import redirect, render


def trigger_exception(_request):
    raise Exception()


def landing_page(request):
    # return redirect("https://www.facebook.com/conyappa/")
    return render(request, "landing_page.html")
