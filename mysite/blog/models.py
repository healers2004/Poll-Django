from pathlib import Path
from django.db import models
from polls.models import Question  # Import the Question model
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_image_format(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = Path(value.name).suffix.lower()
    if ext not in valid_extensions:
        raise ValidationError("Only JPG, PNG, and GIF images are supported.")

class Category(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    poll = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL)  # Add this line
    
    # Adding image field
    image = ThumbnailerImageField(
        upload_to='images/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), validate_image_format]
    ) 
     
    thumbnail_size = models.CharField(
        max_length=10,
        choices=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large')
        ],
        default='medium'
    )

    def __str__(self):
        return self.title
    
    def get_thumbnail_url(self):
        if self.image:
            return self.image[self.thumbnail_size].url
        return ''

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"
