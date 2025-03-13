from django.urls import path
from .views import *

urlpatterns =[
    path("", home, name='home'),
    path("login/", Login, name='login'),
    path("logout/", Logout_User, name='logout'),
    path("verify-otp/<str:phone>/",verify_otp_view, name='verify_otp'),
    path("poll/",PollPage,name='poll'),
    path("Poll/position/<slug:slug>", Positions, name='position'),
    path("candidate/", CandidatePage, name='candid'),
    path("position/vote/<slug:position_slug>/<int:candidate_pk>", Votes,name='vote'),
]