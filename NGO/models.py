from django.db import models

class Volunteer(models.Model):
    # Username field
    username = models.CharField(max_length=255, unique=True)
    
    # Name field
    name = models.CharField(max_length=255)
    
    # Phone number field (assuming a simple phone number format)
    phonenumber = models.CharField(max_length=15)  # You can adjust the length depending on the phone format you need
    
    # Email field
    gmail = models.EmailField(unique=True)
    
    # Password field (for storing hashed password, don't store plaintext passwords!)
    password = models.CharField(max_length=255)
    
    # Admin flag (to distinguish admins from regular users)
    is_admin = models.BooleanField(default=False)
    
    # Adding a method to display the volunteer's name in a more readable way
    def __str__(self):
        return self.name


class Donation(models.Model):
    # ForeignKey to Volunteer for the username field
    username = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='donations_made')

    # A simple CharField for name (no need for another ForeignKey)
    name = models.CharField(max_length=255)  # The name of the donor (could be the same as volunteer's name)

    # Donation image (optional)
    image = models.ImageField(upload_to='donations/', blank=True, null=True)

    # Donation amount
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Donation by {self.name} ({self.username.gmail})"
