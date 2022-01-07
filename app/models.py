from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Program(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    min_age = models.IntegerField(default=3)
    max_age = models.IntegerField(default=30)
    language = models.CharField(max_length=30)
    mode = models.CharField(max_length=30)
    img = models.FileField(
        upload_to='app', default='../media/app/program-default.png')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['min_age']


class Course(models.Model):
    program = models.ForeignKey(Program,  on_delete=CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=255)
    img = models.FileField(
        upload_to='app', default='../media/app/course-default.png')
    creator = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.name + ' by ' + self.creator.username


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    video_url = models.CharField(max_length=255)
    text_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    preview = models.BooleanField()

    def __str__(self):
        return self.title + ' from ' + self.course.name


class Enroll(models.Model):
    course = models.ForeignKey(Course, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' in ' + self.course.name


# class Appointment(models.Model):
#     program = models.ForeignKey(Program, on_delete=CASCADE)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     telephone = models.CharField(max_length=13)
#     email = models.EmailField(max_length=254)
#     address = models.CharField(max_length=255)
#     desired_time = models.DateTimeField()
#     number_of_people = models.IntegerField()

#     def __str__(self):
#         return self.first_name + ' => ' + self.program.title


class SchoolAppointment(models.Model):

    program = models.ForeignKey(Program, on_delete=CASCADE)
    course = models.ForeignKey(Course, on_delete=CASCADE)
    head_name = models.CharField(max_length=50)
    school_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    number_of_people = models.IntegerField()
    telephone = models.CharField(max_length=13)
    address = models.CharField(max_length=255)
    desired_time = models.DateTimeField()
    intake = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.school_name + ' => ' + self.course.name


class ParentAppointment(models.Model):
    program = models.ForeignKey(Program, on_delete=CASCADE)
    course = models.ForeignKey(Course, on_delete=CASCADE)
    parent_name = models.CharField(max_length=50)
    parent_id = models.CharField(max_length=20)
    intake = models.CharField(max_length=254, null=True, blank=True)
    # last_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=13)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=255)
    desired_time = models.DateTimeField()
    child_name = models.CharField(max_length=50)
    child_dob = models.DateTimeField()

    def __str__(self):
        return self.parent_name + ' in ' + self.course.name


class Event(models.Model):
    program = models.ForeignKey(Program, on_delete=CASCADE)
    time = models.DateTimeField()
    venue = models.CharField(max_length=50)

    def __str__(self):
        return self.program.title + ' happening at ' + self.venue
