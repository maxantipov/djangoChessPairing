from django.conf.urls import patterns, include, url

from rrpairing import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tourn_id>\d+)/$', views.tournament, name='detail'),
    url(r'^(?P<tourn_id>\d+)/print$', views.tournament_print, name='torneo_print'),
    url(r'^(?P<tourn_id>\d+)/print_s$', views.standings_print, name='standings_print'),
    url(r'^(?P<round_id>\d+)/results$', views.enter_results, name='enter_results'),
    url(r'^(?P<tourn_id>\d+)/jugadores$', views.intro_players, name='intro_players'),
    url(r'^(?P<team_id>\d+)/introducir_jugadores$', views.save_players, name='save_players'),
    url(r'^(?P<tourn_id>\d+)/segunda_vuelta$', views.create_segunda_vuelta, name='segunda_vuelta'),
    url(r'^(?P<round_id>\d+)/actas$', views.print_entry_slips, name='imprimir_actas'),
    url(r'^(?P<tourn_id>\d+)/cuadro$', views.results_table, name='cuadro_resultados'),
)
