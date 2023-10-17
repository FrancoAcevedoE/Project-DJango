from django.shortcuts import render

from talks.models import Talk


def talk_index(request):
    talks = Talk.objects.all().order_by("-start_date_time")
    context = {"talks": talks}
    return render(request, "talk_index.html", context)
