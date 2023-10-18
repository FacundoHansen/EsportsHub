from django.conf import settings
import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from EsportHub.models import Team , UserProfile
from datetime import datetime
from .forms import PasswordChangeForm, RegistrationForm, UserProfileUpdateExtendedForm, UserProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

User = get_user_model()

#########################################################   Inicio de Recuperar contraseña      ########################
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Tu contraseña se ha restablecido correctamente. Ahora puedes iniciar sesión con tu nueva contraseña.",
                )
                return redirect("password_reset_complete")
        else:
            form = PasswordChangeForm(user)
        return render(
            request,
            "registration/password_reset_confirm.html",
            {"validlink": True, "form": form},
        )
    return render(request, "registration/password_reset_confirm.html", {"validlink": False})

def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

class PasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html' 
    email_template_name = 'registration/password_reset_email.html' 
    subject_template_name = 'registration/password_reset_email_subject.html' 
    success_url = 'done' 
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Se ha enviado un correo electrónico con instrucciones para restablecer su contraseña.'
        )
        return response

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()            
            if user:                
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())
                current_site = get_current_site(request)
                reset_url = f"http://{current_site.domain}/reset/{uid}/{token}/"
                subject = 'Restablecimiento de contraseña'
                message = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                send_mail(subject, message, 'contacto@beguirebels.com', [email])                
                messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para restablecer su contraseña.')
                return redirect('login')
            else:
                messages.error(request, 'No se encontró una cuenta con ese correo electrónico.')
    else:
        form = PasswordResetForm()
    return PasswordResetView.as_view()(
        request,
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('password_reset_done')
    )

#########################################################   Fin del Recuperar contraseña        ########################

#########################################################   Login    ###################################################

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil') 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('perfil')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

#########################################################   Fin del login         #####################################



#########################################################   Perfil del usuario           ##############################

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserProfileUpdateExtendedForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            update_session_auth_hash(request, user_form.instance)  
            return redirect('profile')
    else:
        user_form = UserProfileUpdateExtendedForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    followed_teams = user_profile.followed_teams.all()

    return render(request, 'profile.html', {
        'user_form': user_form,
        'password_form': password_form,
        'followed_teams': followed_teams,
    })

@login_required
def profile_update(request):
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user = request.user
            if 'username' in user_form.changed_data:
                user.username = user_form.cleaned_data['username']
            if 'email' in user_form.changed_data:
                user.email = user_form.cleaned_data['email']
            if 'first_name' in user_form.changed_data:
                user.first_name = user_form.cleaned_data['first_name']
            if 'last_name' in user_form.changed_data:
                user.last_name = user_form.cleaned_data['last_name']
            user.save()            
            if 'new_password1' in request.POST and 'new_password2' in request.POST:
                password_form = PasswordChangeForm(user, request.POST)
                if password_form.is_valid():
                    password_form.save()
            return redirect('profile')
    else:
        user_form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })

#########################################################   Fin de perfil de usuario       ############################


#########################################################   Seguir/Dejar de seguir un equipo       ####################

@login_required
def follow_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        user_profile = UserProfile.objects.get(user=request.user)
        if team in user_profile.followed_teams.all():
            user_profile.followed_teams.remove(team)
            message = "Equipo dejado de seguir."
        else:
            user_profile.followed_teams.add(team)
            message = "Equipo seguido exitosamente."
    except Team.DoesNotExist:
        message = "El equipo no existe."

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unfollow_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        request.user.userprofile.followed_teams.remove(team)
        message = "Dejaste de seguir al equipo."
    except Team.DoesNotExist:
        message = "El equipo no existe."

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def search_team(request):
    query = request.GET.get('query', '').strip()
    try:
        teams = Team.objects.filter(name__icontains=query)
    except ValueError:
        teams = []
    return render(request, 'search_results.html', {'teams': teams, 'query': query})

#########################################################   Fin de  Follows teams   ###################################

#########################################################   Resto de pagina  ##########################################

def index(request):
    return render(request,'index.html')

@login_required(login_url='login')
def list_teams(request):
    page = request.GET.get('page', 1)
    teams = Team.objects.all().order_by('-is_active', 'id')
    paginator = Paginator(teams, 50)  
    teams = paginator.get_page(page)
    return render(request, 'teams_list.html', {'teams': teams, 'current_page': int(page)})

@login_required(login_url='login')
def get_team(request, team_id_or_slug):
    try:
        response = requests.get(f"{settings.PANDASCORE_BASE_URL}teams/{team_id_or_slug}", headers=settings.PANDASCORE_HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        return render(request, '404.html', {'message': f"Error al obtener datos del equipo: {e}"})
    team_data = response.json()
    user_profile = UserProfile.objects.get(user=request.user)
    try:
        team_in_db = Team.objects.get(id=team_data['id'])
        is_following = team_in_db in user_profile.followed_teams.all()
    except Team.DoesNotExist:
        is_following = False
    return render(request, 'team_detail.html', {'team': team_data, 'is_following': is_following})

@login_required(login_url='login')
def get_team_matches(request, team_id_or_slug):
    url = f"{settings.PANDASCORE_BASE_URL}teams/{team_id_or_slug}/matches"
    response = requests.get(url, headers=settings.PANDASCORE_HEADERS)
    matches = response.json()
    for match in matches:
        begin_at = match.get('begin_at') 
        if begin_at is not None:
            begin_at_iso = begin_at.replace('Z', '')
            match['begin_at'] = datetime.fromisoformat(begin_at_iso).strftime(' %d-%m-%Y     %H:%M ')
    return render(request, 'team_matches.html', {'matches': matches})

def list_matches_today(request):
    url = f"{settings.PANDASCORE_BASE_URL}matches/upcoming?&page=1&per_page=100"
    response = requests.get(url, headers=settings.PANDASCORE_HEADERS)
    matches = response.json()
    today_str = datetime.now().strftime('%Y-%m-%d')
    matches = [match for match in matches if match['begin_at'] and match['begin_at'].startswith(today_str)] 
    for match in matches:
        match['begin_at_date'] = datetime.fromisoformat(match['begin_at'].replace('Z', '')).strftime('%d-%m-%Y')
        match['begin_at_time'] = datetime.fromisoformat(match['begin_at'].replace('Z', '')).strftime('%H:%M')    
    return render(request, 'matches_today.html', {'matches': matches})


def get_all_upcomming_matches(request):

    page = 1
    url = f"{settings.PANDASCORE_BASE_URL}matches/upcoming?&page={page}&per_page=100"
    response = requests.get(url, headers=settings.PANDASCORE_HEADERS)
    matches = response.json()
    today_str = datetime.now().strftime('%Y-%m-%d')
    matches = [match for match in matches if match['begin_at'] and match['begin_at'].startswith(today_str)]  #AGREGAR ESTO AL FINAL PARA QUE SE MUESTREN LOS PARTIDOS DEL DIA NADA MAS: and match['begin_at'].startswith(today_str)
    for match in matches:
        match['begin_at_date'] = datetime.fromisoformat(match['begin_at'].replace('Z', '')).strftime('%d-%m-%Y')
        match['begin_at_time'] = datetime.fromisoformat(match['begin_at'].replace('Z', '')).strftime('%H:%M')
    return render(request, 'matches_today.html', {'matches': matches})


def list_matches_now(request):
    url = f"{settings.PANDASCORE_BASE_URL}matches/running"
    response = requests.get(url, headers=settings.PANDASCORE_HEADERS)
    matches = response.json()
    return render(request, 'matches_now.html', {'matches': matches})


@login_required(login_url='login')
def get_match(request, match_id_or_slug):
    try:
        response = requests.get(f"{settings.PANDASCORE_BASE_URL}matches/{match_id_or_slug}", headers=settings.PANDASCORE_HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        return render(request, '404.html', {'message': f"Error al obtener datos del partido: {e}"})
    match_data = response.json()
    user_profile = UserProfile.objects.get(user=request.user)
    try:
        team1_in_db = Team.objects.get(id=match_data['opponents'][0]['opponent']['id'])
        is_following_team1 = team1_in_db in user_profile.followed_teams.all()
    except Team.DoesNotExist:
        is_following_team1 = False
    try:
        team2_in_db = Team.objects.get(id=match_data['opponents'][1]['opponent']['id'])
        is_following_team2 = team2_in_db in user_profile.followed_teams.all()
    except Team.DoesNotExist:
        is_following_team2 = False
    context = {
        'match': match_data,
        'is_following_team1': is_following_team1,
        'is_following_team2': is_following_team2,
    }
    return render(request, 'match_detail.html', context)

######################################################### Fin Resto de pagina #########################################################   

#########################################################   TORNEOS    ################################################

login_required(login_url='login')
def list_tournaments(request):
    page = request.GET.get('page', 1)
    query = request.GET.get('query', '').strip()
    url = f"{settings.PANDASCORE_BASE_URL}tournaments?search={query}&page={page}&per_page=100"
    response = requests.get(url, headers=settings.PANDASCORE_HEADERS)
    tournaments = response.json()
    for tournament in tournaments:
        if tournament['begin_at']:
            tournament['begin_at_date'] = datetime.fromisoformat(tournament['begin_at'].replace('Z', '')).strftime('%d-%m-%Y')
            tournament['begin_at_time'] = datetime.fromisoformat(tournament['begin_at'].replace('Z', '')).strftime('%H:%M')
        if tournament['end_at']:
            tournament['end_at_date'] = datetime.fromisoformat(tournament['end_at'].replace('Z', '')).strftime('%d-%m-%Y')
            tournament['end_at_time'] = datetime.fromisoformat(tournament['end_at'].replace('Z', '')).strftime('%H:%M')
    return render(request, 'tournaments_list.html', {'tournaments': tournaments, 'current_page': int(page), 'query': query})

@login_required(login_url='login')
def get_tournament(request, tournament_id):
    url = f"{settings.PANDASCORE_BASE_URL}tournaments/{tournament_id}"
    response = requests.get(url, headers=settings.PANDASCORE_HEADERS)
    tournament = response.json()
    teams = [team_roster['team']['name'] for team_roster in tournament['expected_roster']]
    for match in tournament['matches']:
        match['begin_at_date'] = datetime.fromisoformat(match['begin_at'].replace('Z', '')).strftime('%d-%m-%Y')
        match['begin_at_time'] = datetime.fromisoformat(match['begin_at'].replace('Z', '')).strftime('%H:%M')
    context = {
        'tournament': tournament,
        'teams': teams,
    }
    return render(request, 'tournament_detail.html', context)

@login_required(login_url='login')
def search_tournament(request):
    query = request.GET.get('query', '').strip()
    url = f"{settings.PANDASCORE_BASE_URL}tournaments/{query}" 
    response = requests.get(url, headers=settings.PANDASCORE_HEADERS)                            
    tournaments = response.json()
    return render(request, 'search_tournament_results.html', {'tournaments': tournaments, 'query': query})

######################################################### Fin #########################################################   