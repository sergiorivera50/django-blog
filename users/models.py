from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
	# Have a one-to-one relationship with the user
	# if user is deleted, profile gets deleted. Not in the other direction.
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs): # override
		super().save(*args, **kwargs)

		img = Image.open(self.image.path) # loads image from path
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size) # resize
			img.save(self.image.path) # saves image into same path to override larger image
