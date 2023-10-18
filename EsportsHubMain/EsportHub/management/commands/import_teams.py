from django.core.management.base import BaseCommand
import json
from EsportHub.models import Team, Player, Videogame
from datetime import datetime

class Command(BaseCommand):
    help = 'Import teams from teams.json file'

    def handle(self, *args, **kwargs):
        with open('teams.json', 'r') as file:
            data = json.load(file)
            
            for team_data in data:
                # Crear o obtener el videojuego
                videogame, created = Videogame.objects.get_or_create(
                    id=team_data['current_videogame']['id'],
                    defaults={
                        'name': team_data['current_videogame']['name'],
                        # Agrega cualquier otro campo necesario para el modelo Videogame aquí
                    }
                )

                if team_data.get('modified_at'):
                    modified_date_team = team_data['modified_at'].replace('Z', '')
                    modified_at_date_team = datetime.fromisoformat(modified_date_team).date()
                else:
                    modified_at_date_team = None

                team, created = Team.objects.get_or_create(
                    id=team_data['id'],
                    defaults={
                        'name': team_data['name']or '',
                        'slug': team_data['slug']or '',
                        'image_url': team_data['image_url'] or '',
                        'location': team_data['location'] or '',
                        'acronym': team_data['acronym'] or '',
                        'modified_at': modified_at_date_team,
                        'current_videogame': videogame
                    }
                )

                for player_data in team_data['players']:
                    if player_data.get('modified_at'):
                        modified_date_player = player_data['modified_at'].replace('Z', '')
                        modified_at_date_player = datetime.fromisoformat(modified_date_player).date()
                    else:
                        modified_at_date_player = None

                    Player.objects.get_or_create(
                        id=player_data['id'],
                        defaults={
                            'name': player_data['name'],
                            'slug': player_data['slug'],
                            'first_name': player_data.get('first_name') or '',
                            'last_name': player_data.get('last_name') or '',
                            'image_url': player_data.get('image_url') or '',
                            'nationality': player_data.get('nationality') or '',
                            'role': player_data.get('role') or '',
                            'age': player_data.get('age'),
                            'birthday': player_data.get('birthday'),
                            'modified_at': modified_at_date_player,
                            'team': team
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Successfully imported teams'))
