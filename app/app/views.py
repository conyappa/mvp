from django.contrib.admin import site as admin_site
from django.shortcuts import render


admin_site.site_header = "Con Yappa"
admin_site.site_title = "Con Yappa"


def trigger_exception(_request):
    raise Exception()


def landing_page(request):
    # return redirect("https://www.facebook.com/conyappa/")
    return render(request, "landing_page.html")
