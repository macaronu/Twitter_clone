from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import SignupForm, PasswordForm
from django.views.generic import FormView

# Views for signing up

def signupPage(request):
    session_form_data1 = request.session.get('form_data1')
    form = SignupForm(session_form_data1)
    if request.method == "POST":
        form = SignupForm(request.POST)
        print (form.errors.as_data())
        if form.is_valid():
            request.session['form_data1'] = request.POST
            return redirect('signup:create_password')

    return render(request, 'signup/signup.html', {'form':form})

def passwordPage(request):
    session_form_data1 = request.session.get('form_data1')
    # session expired or invalid access
    if session_form_data1 is None:
        return redirect('signup:signup')
    # default form
    form = PasswordForm(session_form_data1)
    # user inputs password
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            request.session['form_data2'] = request.POST
            return redirect('signup:confirm')
    return render(request, 'signup/password.html', {'form':form})

def signupConfirm(request):
    session_form_data2 = request.session.get('form_data2')
    if session_form_data2 is None:
        return redirect('signup:signup')

    form = PasswordForm(session_form_data2)
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            del request.session['form_data1']
            del request.session['form_data2']
            form.save()
            return redirect('signup:thanks')
    return render(request, 'signup/signupConfirm.html', {'form':form})

def thanks(request):
    return render(request,'signup/thanks.html')


"""
def signupConfirm(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {'user':user}
    return render(request, 'signup/signupConfirm.html', context)
"""

"""
def signupPage(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        print (form.is_valid())
        if form.is_valid():
            print("yay")
            return redirect('signup:create_password')
    context = {'form':form}
    return render(request, 'signup/signup.html', context)

class signupPage(FormView):
    template_name = 'signup/signup.html'
    form_class = SignupForm
    def get_initial(self):
        initial = super().get_initial()
        initial = self.request.session.get('form_data1')
        print(initial)
        return initial
    def form_valid(self, form):
        self.request.session['form_data1'] = self.request.POST
        return redirect('signup:create_password')

class passwordPage(FormView):
    template_name = 'signup/password.html'
    form_class = PasswordForm
    
    def session_invalid(self):
        session_form_data = request.session.get('form_data1')
        if session_form_data is None:
            return redirect('signup:signup')

    def get_initial(self):
        initial = super().get_initial()
        initial = self.request.session.get('form_data1')
        print(initial)
        return initial

    def form_valid(self, form):
        self.request.session['form_data2'] = self.request.POST
        return redirect('signup:confirm')
"""