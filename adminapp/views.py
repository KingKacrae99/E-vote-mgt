from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from voteapp.models import *
from .form import MemberForm, PositionForm, CandidateForm
from django.contrib import messages
import io

# Create your views here.
@login_required
def Dashboard(request):
    members = Member.objects.all()
    candidates = Candidate.objects.all()
    votes = Vote.objects.all()
    positions = Position.objects.all()


    total_members = members.count()
    total_candidates = candidates.count()
    total_votes = votes.count()
    total_post = positions.count()

    context = {
        'total_members': total_members,
        'total_candidates': total_candidates,
        'total_votes': total_votes,
        'total_post': total_post,
        'members': members,
        'candidates': candidates,
        'votes': votes,
        'positions': positions,
    }
    return render(request,'pages/dashboard.html', context)

@login_required
def CreateMembers(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboard')
    else:
        form =MemberForm()

    context={
        'form': form
    }

    return render(request,'pages/Create_member.html',context)

@login_required
def UpdateMember(request,member_phone):
    if request.user.is_authenticated:
        member = get_object_or_404(Member, phone=member_phone)
        form = MemberForm(instance=member)
        if request.method == 'POST':
            form = MemberForm(request.POST or None, instance=member)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated successfully')
                if request.user.is_admin:
                   return redirect('dashboard')
                else:
                    return redirect('home')
            else:
                messages.warning(request, 'Please ensure you fill all required details')
        else:
            form = MemberForm(instance=member)
    context={
        'form': form
    }
    return render(request, 'pages/Create_member.html', context)

@login_required
def CreatePosition(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Post created successfully! ')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid details')
    else:
        form = PositionForm()

    context = {
        'form': form,
    }
    return render(request, 'pages/positionform.html', context)

@login_required
def Update_Position(request,pk):
    position = get_object_or_404(Position, id=pk)
    form= PositionForm(instance=position)
    if request.method == 'POST':
        form =  PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Successful!')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Update not successful')
    else:
        form= PositionForm()
    context= {
        'form':form,
        'position':position
    }
    return render(request, 'pages/positionform.html', context)

@login_required
def Remove_Position(request,pk):
    position = get_object_or_404(Position, id=pk)
    if request.method == 'POST':
        position.delete()
        return redirect('dashboard')
    context = {
        'position': position
    }
    return render(request, 'pages/deletepost.html', context)


def CreateCandidates(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)  # Don't save yet

            # Handle uploaded profile picture
            if 'profile_pic' in request.FILES:
                profile_pic = request.FILES['profile_pic']
                try:
                    # Open and resize the profile picture to 300x300
                    with Image.open(profile_pic) as img:
                        img = img.resize((300, 300))  # Resize to 300x300
                        img_format = img.format or "JPEG"  # Ensure a valid format

                        # Save the resized profile picture to memory
                        profile_pic_io = BytesIO()
                        img.save(profile_pic_io, format=img_format)
                        profile_pic_io.seek(0)

                        # Save the resized image to the candidate
                        resized_name = f"resized_{profile_pic.name}"
                        candidate.profile_pic.save(resized_name, ContentFile(profile_pic_io.read()), save=False)

                        # Generate thumbnail (100x100)
                        img.thumbnail((100, 100))
                        thumb_io = BytesIO()
                        img.save(thumb_io, format="WEBP", quality=85)
                        thumb_io.seek(0)

                        # Save the thumbnail to the candidate
                        thumbnail_name = f"thumbnail_{profile_pic.name}"
                        candidate.thumbnail.save(thumbnail_name, ContentFile(thumb_io.read()), save=False)

                except Exception as e:
                    messages.error(request, f"Error processing image: {e}")
                    return redirect('create_candidate')

            # Save the candidate instance
            candidate.save()
            return redirect('candid')
        else:
            messages.error(request, 'Registration Failed')
    else:
        form = CandidateForm()

    context = {
        'form': form
    }
    return render(request, 'pages/CreateCandidates.html', context)

def Update_candidate(request,pk):
    candidate = get_object_or_404(Candidate, id=pk)
    form = CandidateForm(instance=candidate)
    if request.method =='POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            candidate = form.save(commit=False)  # Don't save yet

            # Handle uploaded profile picture
            if 'profile_pic' in request.FILES:
                profile_pic = request.FILES['profile_pic']
                try:
                    # Open and resize the profile picture to 300x300
                    with Image.open(profile_pic) as img:
                        img = img.resize((300, 300))  # Resize to 300x300
                        img_format = img.format or "JPEG"  # Ensure a valid format

                        # Save the resized profile picture to memory
                        profile_pic_io = BytesIO()
                        img.save(profile_pic_io, format=img_format)
                        profile_pic_io.seek(0)

                        # Save the resized image to the candidate
                        resized_name = f"resized_{profile_pic.name}"
                        candidate.profile_pic.save(resized_name, ContentFile(profile_pic_io.read()), save=False)

                        # Generate thumbnail (100x100)
                        img.thumbnail((100, 100))
                        thumb_io = BytesIO()
                        img.save(thumb_io, format="JPEG")
                        thumb_io.seek(0)

                        # Save the thumbnail to the candidate
                        thumbnail_name = f"thumbnail_{profile_pic.name}"
                        candidate.thumbnail.save(thumbnail_name, ContentFile(thumb_io.read()), save=False)

                except Exception as e:
                    messages.error(request, f"Error processing image: {e}")
                    return redirect('create_candidate')

            candidate.save()
            return redirect('candid')
        else:
            messages.warning(request, 'Pls fill the required field')

    context = {
        'form':form,
        'candidate': candidate
    }
    return render(request, 'pages/CreateCandidates.html', context)

def Remove_Candidate(request,pk):
    candidate = get_object_or_404(Candidate, id=pk)

    if request.method == 'POST':
        candidate.delete()
        return redirect('candid')
    context = {'candidate':candidate}
    return render(request, 'pages/deletecandid.html', context)

def view_result(request):
    positions = Position.objects.all()
    position_with_candidates = []
    for position in positions:
        candidates = sorted(
            position.candidates.all(),
            key=lambda c: c.votes.count(),
            reverse= True
        )
        candidates_with_ranks = [
            {"candidate": candidate, "rank": idx}
            for idx , candidate in enumerate(candidates,1)
        ]
        position_with_candidates.append({
            "position": position,
            "candidates": candidates_with_ranks
        })

    context = {
        'positions': position_with_candidates
    }
    return render(request,"pages/results.html", context)
