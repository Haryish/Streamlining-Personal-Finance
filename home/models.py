from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from django.core.mail import send_mail

SELECT_CATEGORY_CHOICES = [
    ("Food","Food"),
    ("Travel","Travel"),
    ("Shopping","Shopping"),
    ("Necessities","Necessities"),
    ("Entertainment","Entertainment"),
    ("Other","Other")
]

SELECT_INCOME_CHOICES = [
    ("Monthly income","Monthly income"),
    ("Part Time Income","Part Time Income")
]

ADD_EXPENSE_CHOICES = [
     ("Expense","Expense"),
     ("Income","Income")
 ]
PROFESSION_CHOICES =[
    ("Employee","Employee"),
    ("Business","Business"),
    ("Student","Student"),
    ("Other","Other")
]

GENDER = [
    ("Male","Male"),
    ("Female","Female"),
    ("Others","Others"),
]

class Addmoney_info(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    add_money = models.CharField(max_length = 10 ,default='Expense', choices = ADD_EXPENSE_CHOICES)
    quantity = models.BigIntegerField()
    Date = models.DateField(default = now)
    Category = models.CharField( max_length = 20, choices = SELECT_CATEGORY_CHOICES , default ='Food')
    class Meta:
        db_table:'addmoney'
        
    def save(self,*args, **kwargs):
        is_new = self._state.adding
        super(Addmoney_info,self).save(*args,**kwargs)
        
        if is_new:
            subject = 'New Addmoney Info Added'
            message = f"""
            A new transaction record has been added:

            - Amount: {self.quantity}
            - Category: {self.Category}
            - Type: {self.add_money}
            - Date: {self.Date}
            - User: {self.user.username}
            """

            user_email = self.user.email 

            if user_email: 
                try:
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER, 
                        [user_email], 
                    )
                except Exception as e:
                    print(f"Error sending email: {e}")


class Addmoney_info1(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    add_money = models.CharField(max_length = 10 ,default='Income', choices = ADD_EXPENSE_CHOICES)
    quantity = models.BigIntegerField()
    Date = models.DateField(default = now)
    Category = models.CharField( max_length = 20, choices = SELECT_INCOME_CHOICES , default ='Monthly income')


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10,null=True,blank=True)
    profession = models.CharField(max_length = 10, choices=PROFESSION_CHOICES)
    Savings = models.IntegerField( null=True, blank=True)
    income = models.BigIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_image',blank=True)
    def __str__(self):
       return self.user.username
