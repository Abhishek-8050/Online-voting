from django.db import models

# Admin model
class AdminUser(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    unique_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.unique_code})"


class Candidate(models.Model):
    admin = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name="candidates")
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100, blank=True)
    unique_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.unique_code})"



# Voter model
class Voter(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    unique_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.unique_code}"
    
# Voting Time model

from django.db import models

class VotingTime(models.Model):
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    seconds = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hours}h {self.minutes}m {self.seconds}s - {'Active' if self.is_active else 'Inactive'}"
votes = models.IntegerField(default=0)



class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote for {self.candidate.name}"




