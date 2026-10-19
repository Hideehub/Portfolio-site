from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from portfolio.views import render_home

from .forms import ContactForm
from .services import is_rate_limited, send_notification


def contact(request):
    contact_url = f"{reverse('portfolio:home')}#contact"
    if request.method != "POST":
        return redirect(contact_url)

    form = ContactForm(request.POST)
    if is_rate_limited(request):
        form.add_error(None, "You've sent several messages recently. Please try again later.")
        return render_home(request, contact_form=form, status=429)

    if not form.is_valid():
        return render_home(request, contact_form=form, status=400)

    # Bots that fill the honeypot get the same success response, but nothing is saved.
    if not form.is_spam():
        send_notification(form.save())

    messages.success(request, "Thanks for your message. I'll get back to you soon.")
    return redirect(contact_url)
