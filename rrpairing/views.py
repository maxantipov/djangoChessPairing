# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from rrpairing.models import Team_tournament, Round, Team_game, Team, Player

def index(request):
    tournament_list = Team_tournament.objects.all()
    context = {'tournament_list': tournament_list}
    return render(request,'rrpairing/index.html',context)

def make_pairings(tourney):
    teams_for_count = tourney.team_set.all() # equipos del torneo
    # si hay equipos impares añado uno llamado Descansa, que será el descanso
    if len(teams_for_count)%2 != 0:
        t = Team(name="Descansa",tournament=tourney)
        t.save()
    teams = tourney.team_set.all()
    team_ids = [t.id for t in teams] # lista de ids de los equipos
    # creo la matriz de emparejamientos incializada a 0
    num_teams = len(team_ids)
    matrix = [[0 for i in range(num_teams)] for j in range(num_teams-1)]

    # creo los emparejamientos
    # primero pongo el último en la primera mesa alternando el color
    last_id = team_ids[-1]
    team_ids = team_ids[:-1]
    for i in range(len(team_ids)):
        if i%2==0:
            matrix[i][1] = last_id
        else:
            matrix[i][0] = last_id

    # relleno la tamble de adelante hacia atras
    team_index = 0
    for i in range(len(team_ids)): # filas
        for j in range(0,num_teams,2):
            if j == 0: # primer emparejamiento
                if matrix[i][j] == 0: # si el lugar está vacío, pongo el id del equipo
                    matrix[i][j] = team_ids[team_index] #asigno el id del equipo que toca
                    team_index += 1 # siguiente equipo
                    if team_index >= len(team_ids): team_index = 0 # si se ha salido de la lista, vuelve al primero
                else:
                    matrix[i][j+1] = team_ids[team_index] #asigno el id del equipo que toca
                    team_index += 1 # siguiente equipo
                    if team_index >= len(team_ids): team_index = 0 # si se ha salido de la lista, vuelve al primero

            else:
                matrix[i][j] = team_ids[team_index] #asigno el id del equipo que toca
                team_index += 1 # siguiente equipo
                if team_index >= len(team_ids): team_index = 0 # si se ha salido de la lista, vuelve al primero

    # relleno lo que falta, de atras hacia adelante
    team_index = 0
    for i in range(len(team_ids)-1,-1,-1):
        for j in range(num_teams-1,-1,-1):
            if matrix[i][j] == 0:
                matrix[i][j] = team_ids[team_index] #asigno el id del equipo que toca
                team_index += 1 # siguiente equipo
                if team_index >= len(team_ids): team_index = 0 # si se ha salido de la lista, vuelve al primero

    # por cada fila de la matriz creo una ronda
    for i in range(len(team_ids)):
        r = Round(tournament = tourney, number = i+1)
        r.save()
        for j in range(0,num_teams,2):
            w_team = tourney.team_set.get(pk=matrix[i][j])
            b_team = tourney.team_set.get(pk=matrix[i][j+1])
            g = Team_game(round = r,
                          white_team = w_team,
                          black_team = b_team)
            g.save()
    tourney.pairing_done = True

    return matrix

def tournament(request, tourn_id):
    tourney = get_object_or_404(Team_tournament, pk=tourn_id)
    teams_list = tourney.team_set.all()
    #sort teams by points
    sorted_teams = []
    for team in teams_list:
        sorted_teams.append((team.count_points(),team.name))
    sorted_teams = sorted(sorted_teams, reverse=True)
    if len(tourney.round_set.all()) == 0:
        pairing_matrix = make_pairings(tourney)
    else:
        pairing_matrix = None
    rounds_list = tourney.round_set.all()
    context = {'rounds_list': rounds_list,
               'nombre_torneo': tourney.name,
               'id_torneo': tourn_id,
               'teams_list':sorted_teams}
    return render(request,'rrpairing/torneo.html',context)

def create_segunda_vuelta(request, tourn_id):
    tourney = get_object_or_404(Team_tournament,pk=tourn_id)
    first_rounds = tourney.round_set.all() #rondas de la primera vuelta
    cant_teams = tourney.team_set.count()
    cant_rounds = tourney.round_set.count()
    if cant_rounds < cant_teams +2: #si solo hay una vuelta crada, crea una segunda
        counter = 0
        for r in first_rounds:
            counter += 1
            cant_games = r.team_game_set.count()
            if cant_games > 0:
                new_r = Round(tournament = tourney, number = cant_rounds + counter)
                new_r.save()
                for game in r.team_game_set.all():
                    old_w_team = game.white_team
                    old_b_team = game.black_team

                    g = Team_game(round = new_r,
                              white_team = old_b_team,
                              black_team = old_w_team)
                    g.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def tournament_print(request, tourn_id):
    tourney = get_object_or_404(Team_tournament, pk=tourn_id)
    rounds_list = tourney.round_set.all()
    context = {'rounds_list': rounds_list,
               'nombre_torneo': tourney.name}
    return render(request,'rrpairing/imprimir_rondas.html',context)

def print_entry_slips(request, round_id):
    round = get_object_or_404(Round, pk=round_id)
    games_list = round.team_game_set.all()
    tourney = round.tournament
    context = {'games_list': games_list,
               'round': round,
               'torneo': tourney.name}
    return render(request,'rrpairing/imprimir_actas.html',context)

def standings_print(request, tourn_id):
    tourney = get_object_or_404(Team_tournament, pk=tourn_id)
    teams_list = tourney.team_set.all()
    #sort teams by points
    sorted_teams = []
    for team in teams_list:
        sorted_teams.append((team.count_points(),team.name))
    sorted_teams = sorted(sorted_teams, reverse=True)
    context = {'teams_list':sorted_teams,
               'nombre_torneo': tourney.name}
    return render(request,'rrpairing/imprimir_clasificacion.html',context)

def results_table(request, tourn_id):
    tourney = get_object_or_404(Team_tournament, pk=tourn_id)
    teams = tourney.team_set.all()
    rounds = tourney.round_set.all()

    context = {'teams': teams,
               'rounds': rounds,
               'nombre_torneo': tourney.name}
    return render(request,'rrpairing/cuadro_resultados.html',context)

def enter_results(request, round_id):
    r = get_object_or_404(Round, pk=round_id)
    num = []
    for game in r.team_game_set.all():
        w_result = (request.POST['w_game_'+str(game.id)])
        b_result = (request.POST['b_game_'+str(game.id)])
        game.white_result = w_result
        game.black_result = b_result
        game.save()
    r.played = True
    r.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def intro_players(request, tourn_id):
    tourney = get_object_or_404(Team_tournament, pk=tourn_id)
    teams_list = tourney.team_set.all()
    context = {"teams_list":teams_list,
               "nombre_torneo":tourney.name}
    return render(request,'rrpairing/intro_jugadores.html',context)

def save_players(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    for i in range (1,8):
        name = request.POST['player_name_'+str(i)]
        surname = request.POST['player_surname_'+str(i)]
        elo = request.POST['player_ELO_'+str(i)]

        if len(name) > 0 and len(elo) > 0:
            p = Player(name=name, surname=surname, ELO=elo, team=team)
            p.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))