from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import MakeUser

from .forms import UserForm, RecordTimeForm


@login_required
def home(request):
    return render(
        request,
        'home.html',
    )


@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profileimg = MakeUser.objects.get(user_id=user_id)
    return render(
        request,
        'user_profile.html',
        context={
            'user': user,
            'image': profileimg,
        }
    )


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            new_user.photo = request.FILES['photo']
            # new_user.save()
            return HttpResponseRedirect(reverse(
                'user_profile', args=[new_user.id]
            ))
    else:
        form = UserForm()

    return render(
        request,
        'create_user.html',
        context={
            'form': form,
        }
    )


@login_required
def record_time(request):
    print 'start'
    if request.method == 'POST':
        print 'validate', request.user.id
        form = RecordTimeForm(request.POST, profile_id=request.user)
        if form.is_valid():
            print form
            form.save()
            return HttpResponseRedirect(reverse(
                'record_time'
            ))

    else:
        form = RecordTimeForm()

    return render(
        request,
        'record_time.html',
        context={
            'form': form,
        }
    )
