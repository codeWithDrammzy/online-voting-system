from django.urls import path
from . import views  



urlpatterns = [
    path('', views.home, name="home"),
    path('my-login/', views.my_login, name="my-login"),  
    path('dashboard/', views.dashboard, name="dashboard"),
    path('election/', views.elections, name="election"),
    path('position/', views.positions, name="position"),
    path('candidate/', views.candidates, name="candidate"),
    path('candidate-view/<int:pk>/', views.candidate_view, name="candidate-view"),
    path('update-candidate/<int:pk>/', views.update_candidate, name='update-candidate'),
    path('final-result', views.final_result, name="final-result"),
    path('final-details/<int:position_id>/', views.final_details, name='final-details'),
    

    path("voter", views.voters, name="voter"),
    path('v-dashboard/', views.voter_dashboard, name="v-dashboard"), 
    path('v-vote/', views.v_vote, name="v-vote"), 
    path('candidates-list/<int:position_id>/', views.candidates_list, name="candidates-list"),
    path('vote-candidate/<int:candidate_id>/', views.vote_candidate, name='vote-candidate'),
    path('results/', views.results, name='results'),
    path('results/<int:position_id>/', views.results_detail, name='results_detail'),



    
    path("logout/", views.user_logout, name="logout"),
    path("logout/", views.logout, name="logout"),
    path("delete/<str:model_name>/<int:item_id>/", views.delete_item, name="delete_item"),



]


