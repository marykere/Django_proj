from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() #hashes password, and we can view the registered user from the admin page
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created. Please log in!')
            return redirect('login')

    else: 
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        #adding fields of request.POST and instance ensures data is posted once user& profile update forms are filled
        user_form = UpdateUserForm(request.POST, instance=request.user) 
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        #passing an empty string into forms like user_form = UpdateUserForm(), the update fields were empty. 
        if user_form.is_valid() and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('profile') 
        #redirecting to the profile avoids the GET problem -->"confirm form resubmission?" basically creates another POST request
        
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render (request, 'users/profile.html', context)

# class CustomPasswordResetView(PasswordResetView):
#     email_template_name = 'registration/custom_password_reset_email.html'
#     subject_template_name = 'registration/custom_password_reset_subject.txt'


