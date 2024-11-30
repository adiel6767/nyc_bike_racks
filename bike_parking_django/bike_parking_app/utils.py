# utils.py
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

# def send_verification_email(request, user):
#     token = default_token_generator.make_token(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     current_site = get_current_site(request)
#     verification_link = reverse('email-verify', kwargs={'uidb64': uid, 'token': token})
#     full_link = f"http://{current_site.domain}{verification_link}"
#     send_mail(
#         'Verify your email address',
#         f'Please verify your email address by clicking the following link: {full_link}',
#         'adiel_rodriguez21@outlook.com',
#         [user.email],
#         fail_silently=False,
#     )

def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    frontend_url = "https://dot-bikerack-frontend.onrender.com/login"
    verification_link = f"{frontend_url}?uid={uid}&token={token}"
    send_mail(
        'Verify your email address',
        f'Please verify your email address by clicking the following link: {verification_link}',
        'adiel_rodriguez21@outlook.com',
        [user.email],
        fail_silently=False,
    )