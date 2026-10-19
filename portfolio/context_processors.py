from django.conf import settings


def site(request):
    return {
        "profile": settings.PROFILE,
        "site_origin": f"{request.scheme}://{request.get_host()}",
    }
