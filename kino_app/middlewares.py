from admin_panel.models import *


def getBanner():
    return BackImg.objects.first()


def baseView(request):
    info = MainPage.objects.first()
    return {
        'banner': getBanner(),
        'pages': Page.objects.all(),
        'number1': info.number,
        'number2': info.number2,
        'seo_text': info.seo_text,
    }
