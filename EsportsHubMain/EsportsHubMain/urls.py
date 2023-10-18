from django.contrib import admin
from django.urls import path
from EsportHub import views
from django.contrib.auth import views as auth_views
from EsportHub.views import PasswordResetView

urlpatterns = [    
    #Login
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    #Recuperar contraseña:
    path('reset_password/done/', views.password_reset_done, name='password_reset_done'),
    path('reset_password/complete/', views.password_reset_complete, name='password_reset_complete'),    
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),    
    # Pagina Web
    path('torneos/buscar/', views.search_tournament, name='search_tournament'),
    path('equipos/seguir/<int:team_id>/', views.follow_team, name='follow_team'),
    path('equipos/dejar_de_seguir/<int:team_id>/', views.unfollow_team, name='unfollow_team'),
    path('admin/', admin.site.urls),
    path('equipos/', views.list_teams, name='list_teams'),
    path('equipos/buscar/', views.search_team, name='search_team'),
    path('equipos/<str:team_id_or_slug>/', views.get_team, name='get_team'),
    path('equipos/<str:team_id_or_slug>/partidos/', views.get_team_matches, name='get_team_matches'),
    path('search/', views.search_team, name='search_team'),
    path('partidos/', views.list_matches_today, name='list_matches_today'),
    path('partidos_ahora/', views.list_matches_now, name='list_matches_now'),
    path('partidos/<str:match_id_or_slug>/', views.get_match, name='get_match'),
    path('torneos/', views.list_tournaments, name='list_tournaments'),
    path('torneos/<int:tournament_id>/', views.get_tournament, name='get_tournament'),
]
