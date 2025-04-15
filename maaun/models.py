from django.db import models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Election(models.Model):
    year = models.IntegerField(unique=True, max_length=4)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Election {self.year}"

class Position(models.Model):
    name = models.CharField(max_length=100)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="positions")

    class Meta:
        unique_together = ('name', 'election')  # Prevents duplicate positions under the same election

    def __str__(self):
        return f"{self.name} ({self.election.year})"



class Candidate(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=15, unique=True)
    position = models.ForeignKey('Position', on_delete=models.CASCADE, related_name="candidates")
    avater = models.ImageField(null= True, default="avater.png") 
    created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position.name} ({self.position.election.year})"
    

# Voter Manager
class VoterManager(BaseUserManager):
    def create_user(self, reg_no, password=None, **extra_fields):
        if not reg_no:
            raise ValueError("The Registration Number is required")

        voter = self.model(reg_no=reg_no, **extra_fields)
        voter.set_password(password or reg_no)  # Default password is reg_no if not provided
        voter.save(using=self._db)
        return voter
class Voter(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=15, unique=True)
    level = models.CharField(max_length=3)
    has_voted = models.BooleanField(default=False)  # Add this field
    created = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "reg_no"
    objects = VoterManager()



    def save(self, *args, **kwargs):
        if not self.pk:  # Only set the password when the voter is first created
            self.set_password(self.reg_no)  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.reg_no}"
    
# this is to handle the voting process

class Vote(models.Model):
    voter = models.ForeignKey("Voter", on_delete=models.CASCADE, related_name="votes")
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE)
    position = models.ForeignKey("Position", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voter', 'position')  # Ensures one vote per position per voter

    def __str__(self):
        return f"{self.voter.first_name} {self.voter.last_name} voted for {self.candidate.first_name} {self.candidate.last_name}"


   