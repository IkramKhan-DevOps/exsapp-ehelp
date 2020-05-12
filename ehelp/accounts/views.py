from django.shortcuts import render

# Create your views here.
def view_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
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
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'application/../../templates/accounts/signup.html', {'form': form})


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

@login_required
def view_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('/accounts/login/')

@login_required
def view_privacy(request):

    if request.method == 'POST':
        password_change_form = PasswordChangeForm(data=request.POST, user=request.user)
        if password_change_form.is_valid():
            password_change_form.save()
            return redirect('/privacy/')
        else:
            return redirect('/privacy/')
    else:
        password_change_form = PasswordChangeForm(user=request.user)
        context = {
            'password_change_form': password_change_form
        }
        return render(
            request=request,
            template_name='application/../../templates/accounts/privacy.html',
            context=context,
            status=200
        )


@login_required
def view_profile(request):
    if request.method == 'POST':
        if request.GET['contact']:
            form = FormUserContact(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
        else:
            form = FormUserProfile(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
        return redirect('application:profile')

    form = FormUserProfile(instance=request.user)
    form_contact = FormUserContact(instance=request.user)
    return render(
        request=request,
        template_name='application/profile.html',
        context={'form': form, 'form_contact': form_contact},
        status=200
    )