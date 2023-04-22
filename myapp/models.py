from django.db import models

# Create your models here.
# class = db ka table
# attributes/variables = db ke columns
# object of class = row of the table
class User(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class Blog(models.Model):
    cate = [ ('food', 'food'),
                  ('beauty', 'beauty'),
                   ('lifestyle', 'lifestyle'),
                    ('fashion', 'fashion') ]

    title = models.CharField(max_length=150)
    des = models.TextField(max_length=255)
    categories = models.CharField(max_length=150, choices=cate)
    pic = models.FileField(upload_to="blog_photos", default='sad.jpeg')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    message = models.CharField(max_length=150)
    blog = models.ForeignKey(Blog, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
    

class Donation(models.Model):
    pay_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pay_to = models.ForeignKey(Blog, on_delete=models.CASCADE)
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    