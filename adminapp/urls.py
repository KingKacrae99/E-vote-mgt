from django.urls import path
from .views import *

urlpatterns=[
    path("",Dashboard,name='dashboard'),
    path("create_member/", CreateMembers, name='member'),
    path('Update/member/<str:member_phone>', UpdateMember, name= 'update_info'),
    # Position
    path('Position/', CreatePosition, name='position'),
    path('Update/position/<int:pk>', Update_Position, name='update_post'),
    path('Delete/position/<int:pk>', Remove_Position, name='delete_post'),
    # Candidate
    path('Candidate_Reg/', CreateCandidates, name='create_candidacy'),
    path('Update/candidate/<int:pk>', Update_candidate, name='update_candid'),
    path('Delete/candidate/<int:pk>', Remove_Candidate, name='remove_candid'),
    path('Result/', view_result, name='result')
]