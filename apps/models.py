from django.db.models import Model, ImageField
from django.db.models.fields import BigAutoField, CharField


class UserProfile(Model):
    face_id = BigAutoField(primary_key=True)
    name = CharField(max_length=50)
    address = CharField(max_length=100)
    job = CharField(max_length=15)
    phone = CharField(max_length=10)
    email = CharField(max_length=20)
    bio = CharField(max_length=200)
    image = ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.name
