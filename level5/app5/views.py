from django.shortcuts import render
from app5.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(req):
    return render(req, "app5/index.html")

@login_required
def special(req):
    return HttpResponse("You are logged in. Nice!")


@login_required
def user_logout(req):
    logout(req)
    return HttpResponseRedirect(reverse('index'))


def login(req):

    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(req,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(req, 'basic_app/login.html', {})




def register(req):
    registered = False
    if req.method == "POST":
        user_form = UserForm(data=req.POST)
        profile_form = UserProfileInfoForm(data=req.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()


            profile =profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(req,'app5/register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
