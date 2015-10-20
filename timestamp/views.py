from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import date

from .models import MakeUser, RecordTime

from .forms import UserForm


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
    if request.method == 'POST':
        # Record the time & figure out the status (in/out)
        # Add a new record to the RecordTime model
        # Return all the timestamps for the current day
        # return a JsonResponse

        timerecords = RecordTime.objects.filter(user=request.user).order_by('-tstamp')
        # Returns the current User's time stamps and sorts them in decreasing order

        if timerecords:     # if user has data recorded, then proceed
            dailyrecords = timerecords.exclude(tstamp__lt=date.today())
            # Returns current days time stamps, excludes any prior day's records

            stamplist = []
            for stamps in dailyrecords:
                stamplist.append(stamps.tstamp.strftime("%H:%M %x"))
            #     Iterates through the daily entries of that User on the current day

            timerecord = timerecords[0]
            # Grab the last made entry by the first position

            if timerecord.type == 'O':  # if the type is 'O' then the next type will be 'I'
                nexttype = 'I'

            elif timerecord.type == 'I':    # Look at the type of stamp is
                nexttype = 'O'              # if the type is 'O' then the next type will be 'I'

            newrecord = RecordTime(user=request.user, type=nexttype)
            newrecord.save()
        else:
            # if the user has no data, save user as clocked in
            newrecord = RecordTime(user=request.user, type='I')
            newrecord.save()

        return JsonResponse(

            {'result': True,
             'dailyTimes': stamplist}
        )

    else:
        return render(
            request,
            'record_time.html'
        )
