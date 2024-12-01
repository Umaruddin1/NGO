from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Volunteer , Donation
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')

def volunteer_signup(request):
    if request.method == 'POST':
        # Retrieve the posted data from the form
        username = request.POST.get('username')
        name = request.POST.get('name')
        phonenumber = request.POST.get('phonenumber')
        gmail = request.POST.get('gmail')
        password = request.POST.get('password')
        is_admin = request.POST.get('is_admin') == 'on'  # Checkbox value for is_admin

        # Basic validation
        if not username or not name or not phonenumber or not gmail or not password:
            messages.error(request, 'All fields are required!')
            return redirect('volunteer_signup')

        # Password length check (can be customized)
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return redirect('volunteer_signup')

        # Create and save the Volunteer instance
        volunteer = Volunteer(
            username=username,
            name=name,
            phonenumber=phonenumber,
            gmail=gmail,
            password=password,  # NOTE: Here you should hash the password in a real app!
            is_admin=is_admin
        )
        volunteer.save()

        # Show success message
        messages.success(request, 'Volunteer signed up successfully!')
        return redirect('home')  # Redirect to home or another page after successful signup
    else:
        return render(request, 'signup.html')
def check_password(p1,p2):
    if p1 == p2:
        return True
    else:
        return False
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Retrieve the Volunteer object (user) by username
            volunteer = Volunteer.objects.get(username=username)

            # Check if the password is correct using check_password
            if check_password(password, volunteer.password):
                # If password is correct, manually set the session for the logged-in user
                request.session['volunteer_id'] = volunteer.id  # Store user ID in the session
                return redirect('home')  # Redirect to the home page

            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')  # Redirect back to login page if password is incorrect

        except Volunteer.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # Redirect back to login if volunteer does not exist

    return render(request, 'login.html')

from django.shortcuts import render, redirect
from .models import Volunteer, Donation

def donate(request):
    feedback = None  # Variable to store feedback messages

    if request.method == 'POST':
        # Retrieve donation details from the POST request
        username = request.POST.get('username')
        amount = request.POST.get('amount')
        image = request.FILES.get('image')

        # Check if the form has all required fields
        if not amount or not image:
            feedback = 'Both amount and image are required.'
            return render(request, 'donate.html', {'feedback': feedback})

        # Check if amount is valid
        try:
            amount = float(amount)
        except ValueError:
            feedback = 'Invalid donation amount.'
            return render(request, 'donate.html', {'feedback': feedback})

        try:
            volunteer = Volunteer.objects.get(username=username)
        except Volunteer.DoesNotExist:
            feedback = 'Volunteer with this username does not exist.'
            return render(request, 'donate.html', {'feedback': feedback})

        # Create and save the donation entry to the database
        donation = Donation(
            username=volunteer,
            name=volunteer.name,
            amount=amount,
            image=image
        )
        donation.save()

        # Success message
        feedback = 'Thank you for your donation!'
        return render(request, 'donate.html', {'feedback': feedback})

    return render(request, 'donate.html')


# def donation_list(request):

#     donations = Donation.objects.all()  # Get all donations

#     # Handle deletion of a donation
#     if request.method == 'POST' and 'delete' in request.POST:
#         donation_id = request.POST['delete']
#         Donation.objects.get(id=donation_id).delete()  # Delete the donation by ID
#         return redirect('donation_list')  # Redirect to the donation list page after deletion

#     return render(request, 'donation_list.html', {'donations': donations})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Donation

# Donation List View (only shows donations after correct login details are provided)
def donation_list(request):
    donations = Donation.objects.all()  # Get all donations

    # Check if the form is submitted with login details
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        # Check if the credentials match
        if user_id == 'ShahzanKhursheed' and password == 'Shahzan@786':
            # Correct credentials, show donation list
            return render(request, 'donation_list.html', {'donations': donations, 'authenticated': True})
        else:
            # Incorrect credentials
            messages.error(request, 'Invalid login ID or password.')

    return render(request, 'donation_list.html', {'donations': donations, 'authenticated': False})

# Handle the deletion of a donation
def delete_donation(request):
    if request.method == 'POST' and 'delete' in request.POST:
        donation_id = request.POST['delete']
        Donation.objects.get(id=donation_id).delete()  # Delete the donation by ID
        return redirect('donation_list')  # Redirect to the donation list page after deletion
