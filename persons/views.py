import json

from django.contrib.auth import logout as do_logout, authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode

from persons.forms import SignUpForm
from persons.models import Person
from places.models import Country
from universities.models import University


def logout(request):
    do_logout(request)
    return HttpResponseRedirect(reverse('home_index'))


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")

            else:
                return HttpResponse(json.dumps({"message": "inactive"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "invalid"}), content_type="application/json")

        # return HttpResponse(json.dumps({"message": "denied"}),content_type="application/json")

    else:
        return HttpResponseRedirect(reverse('home_index'))


def autocomplete_university(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = University.objects.filter(name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.FIELD)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        countries = Country.objects.all().order_by('name')
        universities = University.objects.all().order_by('name')
        context = {'form': form,
                   'universities': universities,
                   'countries': countries}
        return render(request, 'signup.html', context)
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        affiliation = request.POST.get('affiliation')
        document_number = request.POST.get('document_number')
        university_name = request.POST.get('university_name')
        university_id = request.POST.get('university_id')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        country = request.POST.get('country')
        relation = request.POST.get('relation')
        user_type = request.POST.get('user_type')

        data = {'first_name': fname, 'last_name': lname, 'email': email, 'document_number': document_number,
                'password2': password2, 'password1': password1, 'relation': relation, 'user_type': user_type,
                'country': country, 'affiliation': affiliation}
        form = SignUpForm(data=data)
        if form.is_valid():
            user = form.save(commit=False)

            if int(university_id) != -1:
                user.university = University.objects.get(pk=university_id)
            else:
                user.university, created = University.objects.get_or_create(name=university_name)

            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Congreso de Extensión: Confirmación de cuenta'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)

            return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")

        else:
            return HttpResponse(json.dumps({"message": form.errors}), content_type="application/json")
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Person.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Person.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.save()
        admin_group_user = Group.objects.get(name=user.user_type)
        admin_group_user.user_set.add(user.pk)
        admin_group_user.save()
        login(request, user)
        # return HttpResponseRedirect(reverse('home_index'))
        return render(request, 'account_activation_valid.html')
    else:
        return render(request, 'account_activation_invalid.html')
