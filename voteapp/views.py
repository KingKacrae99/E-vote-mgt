from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from .utils import *
from .form import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
# Create your views here.


def home(request):
    return render(request, "poll/home.html")

def Login(request):
    if request.method == 'POST':
        form= LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            send_otp(phone)
            message=f'OTP Code has been sent to the {phone}'
            return redirect('verify_otp', phone=phone)
        else:
            message = f'This number ({phone} is not registered.)'
    else:
        form = LoginForm()

    context={
        'form': form
    }
    return render(request,'poll/Login.html', context)

def verify_otp_view(request, phone):
    message =f'Enter code send to {phone}'
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if verify_otp(phone,otp):
            member = authenticate(request, phone=phone)
            if member:
                login(request,member)
                message ='Login Successful!'
                return redirect('home')
            else:
                message = f'{phone} not found'
        else:
            message = 'invalid OTP'
    context= {
            'phone': phone,
            'message': message
       }
    return render(request, 'poll/verify_otp.html', context)

def Logout_User(request):
    logout(request)
    return redirect('login')

def PollPage(request):
    positions = Position.objects.all()
    candidates = Candidate.objects.all()
  
    context = {
        'positions': positions,
        'candidates': candidates
    }
    return render(request,"poll/polling.html", context)

def Positions(request,slug):
    try:
        select_post = Position.objects.get(slug=slug)
        candidate = select_post.candidates.all()
    except Position.DoesNotExist:
        select_post = None
        candidate = []
    context = {
        'select_post': select_post,
        'candidate': candidate
    }
    return render(request,"poll/vote.html", context)

def CandidatePage(request):
    positions = Position.objects.all()
    context = {
        'positions':positions
    }
    
    return render(request,'poll/candidate.html', context)

def Votes(request, position_slug, candidate_pk ):
    position = get_object_or_404(Position, slug=position_slug)
    candidate = Candidate.objects.get(pk=candidate_pk)

    if request.user.is_authenticated:
        existing_vote = Vote.objects.filter(member=request.user, candidate__position=position).first()

        if request.method == 'POST':
           if existing_vote:
               messages.warning(request, "You have already voted for this position.")
               print(messages.warning)
               return redirect(reverse('position', kwargs={'slug': position_slug}))
           else:
               Vote.objects.create(member=request.user, candidate=candidate, voted=True)
               messages.success(request, f'You successfully voted {candidate.name} for {position.title}')
               return redirect(reverse('position',kwargs={'slug': position_slug}))
    return render(request,"poll/vote.html")