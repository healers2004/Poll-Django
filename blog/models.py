from pathlib import Path
from django.db import models
from polls.models import Question  # Import the Question model
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from taggit.managers import TaggableManager 
from ckeditor.fields import RichTextField

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

    tags = TaggableManager()

    def __str__(self):
        return self.title
    
    def get_thumbnail_url(self):
        if self.image:
            return self.image[self.thumbnail_size].url
        return ''
    
    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

class Comment(models.Model):
    class State(models.TextChoices):
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'

    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.PENDING,
    )

    def __str__(self):
        return f"{self.author} on '{self.post}'"
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} ({self.email})"

class ContactUsPageText(models.Model):
    content = RichTextField()

    def __str__(self):
        return "Contact Us Page Text"