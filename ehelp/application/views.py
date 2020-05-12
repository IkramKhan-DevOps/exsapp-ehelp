from .tokens import account_activation_token

from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import (
    logout,
    authenticate)
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm
)
from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth import (
    login,
)
from django.utils.encoding import (
    force_bytes,
    force_text
)
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)
from .forms import (
    SignUpForm,
    FormUserProfile,
    FormUserContact,
    FormRequest
)
from ehelp.application.models import (
    Request as RequestModel,
    Account,
    Response,
    Request_Status,
    Queue
)


def view_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Ehelp account.'
            message = render_to_string('application/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(
                request,
                template_name='application/signup_confirm.html',
                context={'message': 'we have sended an account activation link to your email address, i will be '
                                    'expired after some time so check your mail box'}
            )
    else:
        form = SignUpForm()
    return render(request, 'application/signup.html', {'form': form})


def view_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
    else:
        form = AuthenticationForm
    return render(request=request, template_name='application/login.html', context={'form': form})


def view_home(request):
    user_queue = None
    if not request.user.is_authenticated:
        user_requests = RequestModel.objects.all()
    else:
        user_requests = RequestModel.objects.filter(active=True)
        user_queue = Queue.objects.filter(user=request.user)
        for queue in user_queue:
            user_requests = user_requests.exclude(queue=queue)

    context = {
        'user_requests': user_requests.order_by('-created'),
        'user_queue': user_queue
    }
    return render(
        request=request,
        template_name='application/index.html',
        context=context,
        status=200
    )


@login_required
def view_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('/accounts/login/')


@login_required
def view_dashboard(request, pk=0):
    user = request.user
    if pk != 0:
        user = Account.objects.get(pk=pk)

    total_achievement_points = 100000
    achievement_points_percent = int((request.user.points / total_achievement_points) * 100)

    return render(
        request=request, template_name='application/dashboard.html',
        context={
            'user': user,
            'achievement_points_percent': achievement_points_percent,
            'total_achievement_points': total_achievement_points
        },
        status=200
    )


@login_required
def view_profile(request):
    form = FormUserProfile(instance=request.user)
    form_contact = FormUserContact(instance=request.user)

    if request.method == 'POST':

        action = request.GET['action']
        if action == 'profile':
            form = FormUserProfile(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
        elif action == 'contact':
            form_contact = FormUserContact(request.POST, instance=request.user)
            if form_contact.is_valid():
                form_contact.save()

    return render(
        request=request,
        template_name='application/profile.html',
        context={'form': form, 'form_contact': form_contact},
        status=200
    )


@login_required
def view_requests(request):
    return render(
        request=request, template_name='application/requests.html',
        context={
            'user_requests_model': RequestModel.objects.filter(user=request.user)
        },
        status=200
    )


@login_required
def view_add_update_request(request, pk=0):
    if pk != 0:
        if RequestModel.objects.filter(pk=pk, active=True, user=request.user).count() == 0:
            messages.error(request, 'Request not available to View/Update')
            return render(
                request=request, template_name='application/requests.html',
                context={
                    'user_requests_model': RequestModel.objects.filter(user=request.user),
                },
                status=200
            )

    if request.method == 'POST':
        request_form = FormRequest(request.POST)

        if request_form.is_valid():
            desc = request_form.cleaned_data['desc']
            request_category = request_form.cleaned_data['request_category']
            address = request_form.cleaned_data['address']
            city = request_form.cleaned_data['city']
            country = request_form.cleaned_data['country']
            supply = request_form.cleaned_data['supply']
            user = request.user

            if pk == 0:
                request_model = RequestModel(
                    desc=desc, request_category=request_category, address=address, city=city,
                    country=country, supply=supply, user=user
                )
                requester = Account.objects.get(pk=request.user.pk)
                requester.requests += 1
                requester.save()
            else:
                request_model = RequestModel.objects.filter(pk=pk, active=True, user=request.user)[0]
                request_model.desc = desc
                request_model.request_category = request_category
                request_model.address = address
                request_model.city = city
                request_model.country = country
                request_model.supply = supply

            request_model.save()

            messages.success(request, 'Request Added/Updated Successfully')
            return render(
                request=request, template_name='application/requests.html',
                context={
                    'user_requests_model': RequestModel.objects.filter(user=request.user),
                },
                status=200
            )
    else:

        if pk != 0:
            user_request = FormRequest(instance=RequestModel.objects.filter(
                pk=pk,
                active=True,
                user=request.user)[0])
        else:
            user_request = FormRequest()

        return render(
            request=request, template_name='application/add_update_request.html',
            context={
                'user': request.user,
                'user_request': user_request,
            },
            status=200
        )


@login_required
def view_request_description(request, pk):

    try:
        user_request = RequestModel.objects.get(pk=pk)

        ''' WHO SENDS REQUEST'''
        if user_request.user == request.user:
            is_sender = True
        elif Response.objects.filter(request=user_request, user=request.user):
            is_sender = False
        else:
            messages.error(request, 'un-authorize access blocked - not allowed to view request description')
            return redirect('application:dashboard')
    except RequestModel.DoesNotExist:
        messages.error(request, 'unable to access - request not available')
        return redirect('application:requests')

    if request.method == 'POST':

        user_request.delivered = True
        user_request.active = False
        user_request.save()

        hero_response = Response.objects.filter(request=user_request)[0]
        hero_response.request_points = 8
        hero_response.other_points = 0
        hero_response.shipment_points = 0
        if user_request.supply:
            hero_response.shipment_points = 3
        hero_response.desc = request.POST['feedback']

        hero = Account.objects.get(pk=hero_response.user.pk)
        hero.hearts = hero.hearts + 2
        hero.subscribers = hero.subscribers + 1
        hero.responses = hero.responses + 1
        hero.points = hero.points + (
                hero_response.request_points + hero_response.other_points + hero_response.shipment_points
        )
        hero.save()

        messages.success(request,
                         'Congratulations on your request completion - '
                         'someone helped you and became your hero, other one is waiting for your help')
        hero_response.save()
        context = {
            'is_sender': is_sender,
            'user_request': user_request,
            'hero_response': hero_response
        }
        return render(
            request=request,
            template_name='application/request_description.html',
            context=context,
            status=200
        )

    else:
        hero_response = Response.objects.filter(request=user_request)[0]
        context = {
            'is_sender': is_sender,
            'user_request': user_request,
            'hero_response': Response.objects.filter(request=user_request)[0],
            'total': (hero_response.shipment_points + hero_response.request_points + hero_response.other_points)
        }
        return render(
            request=request,
            template_name='application/request_description.html',
            context=context,
            status=200
        )


@login_required
def view_privacy(request):
    if request.method == 'POST':

        error = None
        password = request.POST['password']

        if password is None or password == '':
            error = 'Please Enter the Password to ' + request.GET['account'] + ' account'
        else:
            if not authenticate(username=request.user.email, password=password):
                error = 'Wrong Password unable to ' + request.GET['account'] + ' account'
            else:
                username = request.user.email
                if request.GET['account'] == 'delete':
                    user = request.user
                    user.delete()
                    logout(request)
                    messages.info(request, "account " + username + " deleted successfully")
                    return redirect('/accounts/login/')

                elif request.GET['account'] == 'deactivate':
                    user = request.user
                    user.is_active = False
                    user.save()
                    logout(request)
                    messages.info(request, "account " + username + " deactivated successfully")
                    return redirect('/accounts/login/')
                else:
                    error = 'action not allowed -- please contact ehelp team'

        messages.error(request, error)
        return render(
            request=request,
            template_name='application/privacy.html',
            status=200
        )
    else:
        return render(
            request=request,
            template_name='application/privacy.html',
            status=200
        )


@login_required
def view_queue(request):
    queue_requests = Queue.objects.filter(user=request.user)
    context = {
        'queue_requests': queue_requests
    }
    return render(
        request=request,
        template_name='application/queue.html',
        context=context,
        status=200
    )


@login_required
def view_responses(request):
    responses = Response.objects.filter(active=True, user=request.user)
    context = {
        'responses': responses
    }
    return render(
        request=request,
        template_name='application/responses.html',
        context=context,
        status=200
    )


@login_required
def view_setting(request):
    return render(
        request=request,
        template_name='application/responses.html',
        status=200
    )


# --------------------------------------------------------------------------------------------------

@login_required
def view_delete_request_required(request, pk):
    if RequestModel.objects.filter(
            pk=pk, user=request.user, active=True,
            delivered=False, accepted=False
    ).count() == 1:
        RequestModel.objects.filter(
            pk=pk, user=request.user, active=True,
            delivered=False, accepted=False
        ).delete()

        # TODO UPDATE STATISTICS IN USER PROFILE AND ALL OTHER USES
        messages.success(request, "Request Successfully Deleted")
        return redirect('application:requests')

    else:
        messages.error(request, "Request is not available to view / delete")
        return redirect('application:requests', pk)


@login_required
def view_delete_response_required(request, req_id, res_id):
    try:
        request_user = RequestModel.objects.get(pk=req_id)
        response = Response.objects.get(pk=res_id)
        request_user.delivered = False
        request_user.accepted = False
        request_user.active = True
        request_user.save()
        response.delete()

        # TODO UPDATE STATISTICS IN USER PROFILE AND ALL OTHER USES and other security to
        messages.success(request, "Response Successfully Deleted")
        return redirect('application:responses')

    except RequestModel.DoesNotExist:
        messages.error(request, "Request is used in someplace")
        return redirect('application:dashboard')


@login_required
def view_add_to_queue_required(request, pk):
    try:
        user_request = RequestModel.objects.get(pk=pk)
        if Queue.objects.filter(user=request.user, request=user_request).count() == 0:
            Queue(
                request=user_request,
                user=request.user
            ).save()
            messages.success(request, "Request from " + user_request.user.full_name + " Successfully added to Queue")
        else:
            messages.error(request, "Request " + str(pk) + " already exists")

    except RequestModel.DoesNotExist:
        messages.error(request, "Requested request doesn't exists")
    return redirect('application:home')


@login_required
def view_delete_from_queue_required(request, pk):
    try:
        queue = Queue.objects.get(pk=pk)
        if queue.user == request.user:
            queue.delete()
            messages.success(request, "Request from " + str(queue.request.user.full_name) + " Successfully DEQUEUE")
        else:
            messages.error(request, "un-authorize access blocked - now allowed to delete")

    except RequestModel.DoesNotExist:
        messages.error(request, "Requested request doesn't exists in Queue")
    return redirect('application:queue')


@login_required
def view_add_response_required(request, pk):
    try:
        requester_request = RequestModel.objects.get(pk=pk)
        requester_request.accepted = True
        requester_request.save()

        user = request.user

        Response(
            user=request.user,
            request=requester_request
        ).save()

        for queue in Queue.objects.filter(request=requester_request):
            queue.delete()

    except RequestModel.DoesNotExist:
        messages.error(request, "Requested request doesn't exists")
    return redirect('application:queue')


# --------------------------------------------------------------------------------------------------


def view_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(
            request,
            template_name='application/signup_confirm.html',
            context={
                'message': 'Thank you for your email confirmation, GOOD LUCK! help the needy, make your '
                           'profile, be a reason of someone to smile and become a HERO.'
            }
        )
    else:
        return render(
            request,
            template_name='application/signup_confirm.html',
            context={'message': 'unable to activate account because the activation link is invalid'}
        )
