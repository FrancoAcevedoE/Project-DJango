from datetime import datetime, timedelta
from itertools import chain

from django.shortcuts import render
from django.db.models import F

from projects.models import *
from talks.models import Talk, Act, Day


def home_index(request):
    thematics = Thematic.objects.all()
    days = Day.objects.all()

    talks_first_day = Talk.objects.filter(day='1', is_masterful=False).order_by('start_time', 'end_time')
    talks_second_day = Talk.objects.filter(day='2', is_masterful=False).order_by('start_time', 'end_time')
    talks_third_day = Talk.objects.filter(day='3', is_masterful=False).order_by('start_time', 'end_time')
    acts_first_day = Act.objects.filter(day='1').order_by('start_time', 'end_time')
    acts_second_day = Act.objects.filter(day='2').order_by('start_time', 'end_time')
    acts_third_day = Act.objects.filter(day='3').order_by('start_time', 'end_time')
    masterful_first_day = Talk.objects.filter(day='1', is_masterful=True).order_by('start_time', 'end_time')
    masterful_second_day = Talk.objects.filter(day='2', is_masterful=True).order_by('start_time', 'end_time')
    masterful_third_day = Talk.objects.filter(day='3', is_masterful=True).order_by('start_time', 'end_time')
    context = {"thematics": thematics,
               "days": days,
               "acts_first_day": acts_first_day,
               "acts_second_day": acts_second_day,
               "acts_third_day": acts_third_day,
               "talks_first_day": talks_first_day,
               "talks_second_day": talks_second_day,
               "talks_third_day": talks_third_day,
               "masterful_first_day": masterful_first_day,
               "masterful_second_day": masterful_second_day,
               "masterful_third_day": masterful_third_day
               }
    return render(request, "home_index.html", context)


def project_index(request, thematic):
    thematic_detail = Thematic.objects.get(pk=thematic)
    projects = Project.objects.filter(thematic__pk=thematic).order_by('title')
    context = {"projects": projects, "thematic": thematic_detail}
    return render(request, "project_index.html", context)


def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    context = {"project": project}
    return render(request, "project_detail.html", context)


def home(request):
    startdate = datetime.today() - timedelta(hours=4)
    commissions = Commission.objects.filter(youtube_url__isnull=False,
                                            date_time__gte=startdate).order_by('date_time', 'name')
    conferences = Conference.objects.filter(youtube_url__isnull=False,
                                            date_time__gte=startdate).order_by('date_time', 'name')
    commissions_old = Commission.objects.filter(youtube_url__isnull=False,
                                                date_time__lte=startdate).order_by('date_time', 'name')
    conferences_old = Conference.objects.filter(youtube_url__isnull=False,
                                                date_time__lte=startdate).order_by('date_time', 'name')
    # audiences = Audience.objects.order_by('date_time')
    context = {
        "conferences": conferences,
        "conferences_old": conferences_old,
        # "audiences": audiences,
        "commissions": commissions,
        "commissions_old": commissions_old
    }
    return render(request, 'home.html', context)


def ponencias(request):
    return render(request, 'ponencias_doors.html', {})


def ponencias_mesas(request, eje):
    search_text = request.GET.get("q", "")
    if search_text:
        presentations = Presentation.objects.filter(status=Project.APPROVED, title__contains=search_text, theme=eje)
        template = "ponencias_carrousel.html"
        context = {
            "presentations": presentations,
            "theme": eje
        }
    else:
        commissions = Commission.objects.filter(theme=eje).order_by('name')
        template = "ponencias_mesas.html"
        context = {
            "commissions": commissions,
        }

    return render(request, template, context)


def ponencias_carrousel(request, eje, mesa):
    presentations = Presentation.objects.filter(commission=mesa, status=Project.APPROVED, theme=eje)
    context = {
        "theme": eje,
        "presentations": presentations,
        "mesa": mesa
    }
    return render(request, "ponencias_carrousel.html", context)


def ponencias_individual(request, eje, pk, mesa=0):
    presentations = Presentation.objects.filter(status=Project.APPROVED, pk=pk)
    context = {
        "theme": eje,
        "mesa": mesa,
        "presentations": presentations
    }
    return render(request, "ponencias_individual.html", context)


def experiencias(request):
    return render(request, 'experiencias_doors.html', {})


def experiencias_mesas(request, eje):
    search_text = request.GET.get("q", "")
    if search_text:
        posters = Poster.objects.filter(status=Project.APPROVED, title__contains=search_text, theme=eje)
        video_posters = VideoPoster.objects.filter(status=Project.APPROVED, title__contains=search_text, theme=eje)
        presentations = list(chain(posters, video_posters))
        template = "experiencias_carrousel.html"
        context = {
            "presentations": presentations,
            "theme": eje
        }
    else:
        commissions = Commission.objects.filter(theme=eje).order_by('name')
        template = "experiencias_mesas.html"
        context = {
            "commissions": commissions,
        }

    return render(request, template, context)


def experiencias_carrousel(request, eje, mesa):
    posters = Poster.objects.filter(commission=mesa, status=Project.APPROVED, theme=eje)
    video_posters = VideoPoster.objects.filter(commission=mesa, status=Project.APPROVED, theme=eje)
    presentations = list(chain(posters, video_posters))
    context = {
        "theme": eje,
        "presentations": presentations,
    }
    return render(request, "experiencias_carrousel.html", context)


def experiencias_individual(request, eje, pk, mesa=0):
    presentations = Poster.objects.filter(status=Project.APPROVED, pk=pk)
    if not presentations:
        presentations = VideoPoster.objects.filter(status=Project.APPROVED, pk=pk)
    context = {
        "theme": eje,
        "mesa": mesa,
        "presentations": presentations
    }
    return render(request, "experiencias_individual.html", context)


def talleres(request):
    workshops = Workshop.objects.filter(youtube_url__isnull=False).order_by('date_time')
    context = {
        "workshops": workshops
    }
    return render(request, 'talleres.html', context)


def auditorio_mesas(request):
    startdate = datetime.today() - timedelta(hours=4)
    conferences = Conference.objects.filter(youtube_url__isnull=False,
                                            date_time__gte=startdate).order_by('date_time', 'name')
    conferences_old = Conference.objects.filter(youtube_url__isnull=False,
                                                date_time__lte=startdate).order_by('date_time', 'name')
    commissions = Commission.objects.filter(youtube_url__isnull=False,
                                            date_time__gte=startdate).order_by('date_time', 'name')
    commissions_old = Commission.objects.filter(youtube_url__isnull=False,
                                                date_time__lte=startdate).order_by('date_time', 'name')
    context = {
        'conferences': conferences,
        'conferences_old': conferences_old,
        "commissions": commissions,
        "commissions_old": commissions_old
    }
    return render(request, 'auditorio_mesas.html', context)


def auditorio_videos(request, mesa):
    audiences = Audience.objects.order_by('date_time').filter(commission=mesa)
    context = {
        "audiences": audiences
    }
    return render(request, 'auditorio_videos.html', context)
