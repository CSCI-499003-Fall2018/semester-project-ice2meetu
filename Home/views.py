
from .forms import SignUpForm, Join
from creation.models import Event, Group
from games.models import Game, GameType
import random

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# For email verification process
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import send_mail

creators = [
    {
        'name': 'Kevin',
        'school': 'Hunter College'
    },
    {
        'name': 'Dandan',
        'school': 'Hunter College'
    },
    {
        'name': 'Silvena',
        'school': 'Hunter College'
    },
    {
        'name': 'Kristoff',
        'school': 'Hunter College'
    }
]


def home(request):
    args = {
        'title': 'Ice2MeetU'
    }
    return render(request, 'Home/home.html', args)

def logout(request):
    return render(request, 'Home/home.html', {})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user_email = form.cleaned_data.get('email')
            # TODO: Validate the email
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('Home/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(
                subject, message, to=[user_email]
            )
            email.send()
    
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'Home/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'Home/account_activation_sent.html')

def confirmed_page(request):
    return render(request, 'Home/account_confirmed_page.html')


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()

        return render(request, 'Home/account_confirmed_page.html')
    else:
        return render(request, 'Home/account_activation_invalid.html')


def logon(request):
    if request.method == 'POST':
        user = authenticate(
            username = request.POST.get('username', '').strip(),
            password = request.POST.get('password', ''),
        )

        if user is None:
            messages.error(request, u'Invalid credentials')
        else:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', 'home_creation_page'))
            else:
                messages.error(request, u'User is not active.')

                return render_to_response('Home/login.html', locals(),
                    context_instance=RequestContext(request))
    else:
        return render(request, 'Home/login.html', {})

@login_required(login_url='login/')
def profile(request):
    return render(request, 'Home/home.html', {})

@login_required(login_url='login/')
def join(request):
    if request.method == 'POST':

        form = Join(request.POST)
        try:
            code = form.data['access_code']
            form = Event.objects.get(access_code=code)
        except Event.DoesNotExist:
            content = {
                'form': form,
                'name': 'Invalid Access Code',
                'user' : request.user
            }
            return render(request, 'Home/join.html', content)

        return HttpResponseRedirect('../event/{}/go'.format(form.access_code))
    else:
        form = Join()
    content = {
        'form': form,
        'name': 'Access Code',
        'user' : request.user
    }
    return render(request, 'Home/join.html', content)
