from django.shortcuts import render,redirect,reverse

from ..models import UWQ


#作品提交权限控制

def f_up(request,pIndex,con_id):
    uwq = UWQ.objects.get(con_id=con_id)
    uwq.status = True
    uwq.stage = 1
    uwq.save()
    return redirect(reverse('match_con_show',args=(pIndex,)))

def f_down(request,pIndex,con_id):
    uwq = UWQ.objects.get(con_id=con_id)
    uwq.status = False
    uwq.stage = 1
    uwq.save()
    return redirect(reverse('match_con_show',args=(pIndex,)))

def s_up(request,pIndex,con_id):
    uwq = UWQ.objects.get(con_id=con_id)
    uwq.stage = 2
    uwq.status = True
    uwq.save()
    return redirect(reverse('match_con_show',args=(pIndex,)))

def s_down(request,pIndex,con_id):
    uwq = UWQ.objects.get(con_id=con_id)
    uwq.status = False
    uwq.stage = 2
    uwq.save()
    return redirect(reverse('match_con_show',args=(pIndex,)))

def t_up(request,pIndex,con_id):
    uwq = UWQ.objects.get(con_id=con_id)
    uwq.stage = 3
    uwq.status = True
    uwq.save()
    return redirect(reverse('match_con_show',args=(pIndex,)))

def t_down(request,pIndex,con_id):
    uwq = UWQ.objects.get(con_id=con_id)
    uwq.status = False
    uwq.stage = 3
    uwq.save()
    return redirect(reverse('match_con_show',args=(pIndex,)))