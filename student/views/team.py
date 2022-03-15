from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator
from myadmin.models import Info, Organizer, File, Team, Registration, Contest, User





def sc_team_list(request,pIndex):
    user_name = request.session.get('user_name')
    user_id = request.session.get("user_id")
    #拿到用户的所有team记录
    team = Team.objects.filter(use_id=User.objects.get(user_id=user_id).id)
    for ut in team:
        h_c_id = ut.h_c_id