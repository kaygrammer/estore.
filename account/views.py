from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import Loginform, UserRegistrationForm, UserEditForm, ProfileEditForm
from shop.models import Product,Category
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator


@login_required()
def dashboard(request,  category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)[:9]
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    paginator = Paginator(products, 6)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'category': category,
               'categories': categories,
               'products': products,
               'page' : page}
    return render(request, 'shop/product/index.html', context)



def user_login(request):
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("dashboard")
                else:
                    return HttpResponse('Disable account')
            else:
                return HttpResponse('invalid login')
    else:
        form = Loginform()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
