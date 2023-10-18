# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
# Internal:
from .forms import ContactForm
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_user_instance(request):
    """
    retrieves user details if logged in
    """

    user_email = request.user.email
    user = User.objects.filter(email=user_email).first()
    return user


def contact_view(request):
    """
    A function to render contact page,
    provide contact form
    """
    if request.user.is_authenticated:
        email = request.user.email
        contact_form = ContactForm(initial={'email': email})
        if request.method == 'POST':
            contact_form = ContactForm(data=request.POST)

            if contact_form.is_valid():
                contact = contact_form.save(commit=False)

                return render(request, 'contact/message-received.html')
    else:
        contact_form = ContactForm()

    template = 'contact/contact.html'
    context = {
        'contact_form': contact_form
    }
    return render(request, template, context)
