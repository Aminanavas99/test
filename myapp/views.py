from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from myapp.models import User, Role,Recipe
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import logging
from myapp.forms import ProfilePictureForm,RecipeForm

import json
# Create your views here.




@csrf_exempt
def register(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        role_name = request.POST.get('role')
        email = request.POST.get('email')

        
        try:
            role = Role.objects.get(role=role_name)
        except Role.DoesNotExist:
            return HttpResponse('Role does not exist')

        new_user = User.objects.create(name=name,email=email, role=role)
        new_user.save()
        
        # return HttpResponse('registered successfully')
        return redirect(reg_view)
    else:
        return render(request, 'register.html')
    


def reg_view(request):
    return render(request,'reg_view.html')


ADMIN_USERNAME = 'ADMIN'

ADMIN_ROLE_NAME = 'admin'



@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        logging.debug(f"Login attempt with name: {name}")
        
        if not name:
            logging.debug("No name provided in the request.")
            return HttpResponse('No name provided')
        
        if name == ADMIN_USERNAME:
            admin_role, created = Role.objects.get_or_create(role=ADMIN_ROLE_NAME)
            # Ensure the admin user exists
            admin_user, created = User.objects.get_or_create(
                name=ADMIN_USERNAME,
                defaults={'role': admin_role}
            )
            # Set session role for admin
            request.session['role'] = 'admin'
            request.session['user_id'] = 0  # Assuming 0 for admin as a special ID
            request.session['name'] = ADMIN_USERNAME
            logging.debug("Admin user logged in.")
            return render(request,'admin_dashboard.html')  # Change this to your admin dashboard URL or view
        
        try:
            user = User.objects.get(name=name)
            
            logging.debug(f"User found: {user.name}")
            
            request.session['role'] = user.role.role
            request.session['user_id'] = user.id
            request.session['name'] = user.name
            return redirect('index')  # Change this to your user dashboard URL or view
        except User.DoesNotExist:
            logging.debug(f"No user found with name: {name}")
            return HttpResponse('User not found')
    else:
        return render(request, 'login.html')




# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
        
#         logging.debug(f"Login attempt with name: {name}")
        
#         if not name:
#             logging.debug("No name provided in the request.")
#             return HttpResponse('No name provided')
        
#         if name == ADMIN_USERNAME:
#             admin_role, created = Role.objects.get_or_create(role=ADMIN_ROLE_NAME)
#             # Ensure the admin user exists
#             admin_user, created = User.objects.get_or_create(
#                 name=ADMIN_USERNAME,
#                 defaults={'role': admin_role}
#             )
#             # Set session role for admin
#             request.session['role'] = 'admin'
#             request.session['user_id'] = 0  # Assuming 0 for admin as a special ID
#             logging.debug("Admin user logged in.")
#             return render(request,'admin_dashboard.html')  # Change this to your admin dashboard URL or view
        
#         try:
#             user = User.objects.get(name=name)
            
#             logging.debug(f"User found: {user.name}")
            
#             request.session['role'] = user.role.role
#             request.session['user_id'] = user.id
#             return redirect('dashboard')  # Change this to your user dashboard URL or view
#         except User.DoesNotExist:
#             logging.debug(f"No user found with name: {name}")
#             return HttpResponse('User not found')
#     else:
#         return render(request, 'login.html')



@csrf_exempt
def create_role(request):
    roles_to_create = ['user', 'admin', 'moderator']
   
    for role in roles_to_create:
        if not Role.objects.filter(role=role).exists():
            Role.objects.create(role=role)
            
    return HttpResponse({"message": "Roles have been created"})

# def dashboard(request):
#     if 'user_id' not in request.session:
#         return redirect('login')

#     user_id = request.session['user_id']
#     user = User.objects.get(id=user_id)
#     role = request.session.get('role')

#     # if role == 'admin':
#     #     return render(request, 'admin_dashboard.html', {'user': user})
#     if role == 'moderator':
#         return render(request, 'moderator_dashboard.html', {'user': user})
#     else:
#         return render(request, 'user_dashboard.html', {'user': user})



# def dashboard(request):
#     if 'user_id' not in request.session:
#         return redirect('login')

#     user_id = request.session['user_id']
#     user = User.objects.get(id=user_id)
#     role = request.session.get('role')

#     if request.method == 'POST':
#         form = ProfilePictureForm(request.POST, request.FILES, instance=user)
#         recipe_form = RecipeForm(request.POST, request.FILES)
#         # initializes the form with the POST data and uploaded files, and associates
#         #  it with the current user.
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#         if recipe_form.is_valid():
#             recipe = recipe_form.save(commit=False)
#             recipe.created_by = user
#             recipe.save()
#             return redirect('dashboard')
#     else:
#         form = ProfilePictureForm(instance=user)
#         recipe_form = RecipeForm()

#     context = {
#         'user': user,
#         'role': role,
#         'form': form,
#         'recipe_form': recipe_form,
#     }

#     # if role == 'admin':
#     #     return render(request, 'admin_dashboard.html', context)
#     if role == 'moderator':
#         return render(request, 'moderator_dashboard.html', context)
#     else:
#         return render(request, 'user_dashboard.html', context)



def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    role = request.session.get('role')

    if request.method == 'POST':
        profile_form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        recipe_form = RecipeForm(request.POST, request.FILES)
        
        if 'upload_profile_picture' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                return redirect('dashboard')
        
        if 'add_recipe' in request.POST:
            if recipe_form.is_valid():
                recipe = recipe_form.save(commit=False)
                recipe.created_by = user
                recipe.save()
                return redirect('dashboard')
    else:
        profile_form = ProfilePictureForm(instance=user)
        recipe_form = RecipeForm()

    context = {
        'user': user,
        'role': role,
        'profile_form': profile_form,
        'recipe_form': recipe_form,
    }

    if role == 'moderator':
        return render(request, 'moderator_dashboard.html', context)
    else:
        return render(request, 'user_dashboard.html', context)
    


def admin_dashboard(request):
    if request.session.get('role') != 'admin':
        return HttpResponseForbidden("You do not have access to this page.")
    # if request.user.role.role == 'admin':
    #     pending_recipes = Recipe.objects.filter(verified=False)
    #     return render(request, 'admin_dashboard.html', {'recipes': pending_recipes})
    
    return render(request, 'admin_dashboard.html')
    



    

def logout_view(request):
    logout(request)
    return redirect(index)

# 
def account(request):
    return render(request,'account.html')


def index(request):
    return render(request,'index.html')




def add_rec(request):
    if 'user_id' not in request.session:
        return redirect('login')

    role = request.session.get('role')
    if role != 'moderator':
        return redirect('dashboard')

    # Fetch recipes added by moderators
    recipes = Recipe.objects.filter(created_by__role=3)

    context = {
        'recipes': recipes,
    }

    # return render(request, 'moderator_recipes.html', context)
    return render(request,'recipes.html',context)


def view_rec(request):
    return render(request,'single-recipe.html')




# -----------------recipe submission-----------------------------


# @login_required
# def submit_recipe(request):
#     if request.method == 'POST':
#         form = RecipeForm(request.POST)
#         if form.is_valid():
#             recipe = form.save(commit=False)
#             recipe.created_by = request.user
#             recipe.save()
#             return redirect('dashboard')
#     else:
#         form = RecipeForm()
#     return render(request, 'submit_recipe.html', {'form': form})

# @login_required
# def approve_recipe(request, recipe_id):
#     if request.user.role.role == 'admin':
#         recipe = Recipe.objects.get(id=recipe_id)
#         recipe.verified = True
#         recipe.approved_by = request.user
#         recipe.save()
#         return redirect('admin_dashboard')
#     else:
#         return redirect('dashboard')

# @login_required
# def admin_dashboard(request):
#     if request.user.role.role == 'admin':
#         pending_recipes = Recipe.objects.filter(verified=False)
#         return render(request, 'admin_dashboard.html', {'recipes': pending_recipes})
#     else:
#         return redirect('dashboard')

