from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

import jwt
import string
from datetime import datetime, timezone
from hiq.utils import send_verification_email, verification_code_generator


class HomePage(Page):
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    heading = models.TextField(
        null=False,
        blank=False,
    )

    sub_heading = models.TextField(
        null=False,
        blank=False,
        default='',
    )

    secondary_heading = models.TextField(
        null=False,
        blank=False,
        default='',
    )

    homepage_content = RichTextField()

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('heading'),
        FieldPanel('sub_heading'),
        FieldPanel('secondary_heading'),
        FieldPanel('homepage_content'),
    ]

class Profile(models.Model):

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        default=1
    )

    birthday = models.DateField(
        null=True,
        blank=True,
    )

    validation_key = models.TextField(
        null=True,
        blank=True,
        default='',
    )

    validation_datetime = models.DateTimeField()

    email_verified = models.BooleanField(
        default=False,
    )

    authorized = models.BooleanField(
        default=False
    )

class LogoutPage(Page):
    def serve(self, request):
        logout(request)
        return redirect('/')

class SignupPage(Page):

    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

    def valid_password(self, password):
        valid = True
        special_chars = string.punctuation
        if len(password) < 8:
            valid = False

        if not any(char.isdigit() for char in password):
            valid = False

        if not any(char in special_chars for char in password):
            valid = False

        return valid



    def serve(self, request):
        if request.method == 'POST':
            form_error = ''
            request.session['profile_info'] = request.POST
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                form_error = 'Passwords do not match'

            if first_name == '' or last_name == '' or email == '' or password == '':
                form_error = "Please fill out the entire form"

            if len(User.objects.filter(email=email)) >= 1:
                form_error = "A user with that email address already exists"

            if form_error != '':
                request.session['form_error'] = form_error
                return super().serve(request)
            # Everything checks out, create the user and generate the
            # email verification token and send email
            else:
                user = User.objects.create_user(email, email, password, first_name=first_name, last_name=last_name)
                login(request, user)
                email_code = verification_code_generator()
                now = datetime.now(timezone.utc)
                profile = Profile.objects.create(user=user, validation_key=email_code, validation_datetime=now, authorized=False, email_verified=False)
                send_verification_email(email, email_code)
                profile.save()
                return redirect('/verify-email')

        else:
            request.session['form_error'] = ''
            if request.user.is_authenticated:
                return redirect('/verify-email')
            return super().serve(request)


class VerifyEmailPage(Page):
    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

    def serve(self, request):
        if request.method == 'GET':
            request.session['verify_key_error'] = ''
            try:
                if not request.user.is_authenticated:
                    return redirect('/signup')
                elif request.user.profile_set.get().email_verified:
                    return redirect('/assessment')
                else:
                    return super().serve(request)
            except Exception as e:
                return redirect('/logout')

        if request.method == 'POST':
            verify_key_error = ''
            user_profile = request.user.profile_set.get()
            actual_validation_key = user_profile.validation_key
            validation_key_datetime = user_profile.validation_datetime
            now = datetime.now(timezone.utc)

            if ((now-validation_key_datetime).seconds)/60 > 15:
                verify_key_error = 'This code has expired, please request a new one'

            submitted_key = str(request.POST.get('verify_code'))

            if submitted_key != actual_validation_key:
                verify_key_error = 'This code is invalid'

            if verify_key_error == '':
                user_profile.email_verified = True
                user_profile.save()
                return redirect('/assessment')
            else:
                request.session['verify_key_error'] = verify_key_error

            return super().serve(request)

class AssessmentPage(Page):
    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

    def serve(self, request):
        if request.method == 'GET':
            if not request.user.is_authenticated:
                return redirect('/signup')

            if not request.user.profile_set.get().email_verified:
                return redirect('/verify-email')

            return super().serve(request)
