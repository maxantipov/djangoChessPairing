# -*- coding: utf-8 -*-
from django.contrib import admin
from rrpairing.models import Team_tournament,Team,Player,Team_game,Round

class Teams_in_line(admin.TabularInline):
    model = Team
    extra = 12

class Players_in_line(admin.TabularInline):
    model = Player
    extra = 6

class Team_tournament_admin(admin.ModelAdmin):
    inlines = [Teams_in_line]

class Team_admin(admin.ModelAdmin):
    inlines = [Players_in_line]

admin.site.register(Team, Team_admin)
admin.site.register(Team_tournament, Team_tournament_admin)
admin.site.register(Team_game)
admin.site.register(Round)
admin.site.register(Player)