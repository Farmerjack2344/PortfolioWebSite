from django.db import models
from django.utils.timezone import now
from django.urls import reverse # The reverse function allows retrieving url details from the url's.py file through the name value provided

# Create your models here.
# A model is the single, definitive source of information about your data


class Post(models.Model):
    """
    This Model class will be the source of data regarding the contents of a post
    """
    author = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)# Foreign Key to link on

    title = models.CharField(max_length=256)# Title of the post
    text = models.TextField()# Text that will be in the post, text field is used to prepare for alot of text
    create_date = models.DateTimeField(default=now) # the date the post was made
    published_date = models.DateField(default=now) # the dae the post was puublished
    image_name = models.CharField(default= 'none',max_length=256)
    post_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def publish(self):
        self.published_date = now()
        # It will change the publish date to whenever the date/time is at the time
        self.save() # This will then save the post

    def approved_comments(self):
        return self.comments.filter(apprved_comments=True)# This will return all of the comments that were approved using the filter method

    def get_absolute_url(self):
        """
        This method tell the app where to go back to
        and in this case it will take you back to the post once it has been made.
        :return:
        """
        return reverse("blog:post_detail", kwargs={'pk':self.pk})

    def __str__(self):
        """

        :return: The name of the title
        """
        return self.title

# class PostFile(models.Model):
#     post = models.ForeignKey('Blog.post', on_delete=models.CASCADE, related_name='files')
#     file = models.ImageField(upload_to='images/')
#     image_name = models.CharField(default='Figure',max_length=256)
#
#     def __str__(self):
#         return f"File for post: {self.post.title}"

class Comments(models.Model):
    """
    This model will be the source of data for comments
    """
    # Error on the line below, blog not installedchat
    post = models.ForeignKey('Blog.post', related_name='comments', on_delete=models.CASCADE) # This line will connect a comment to a blog post
    #The CASCADE option in Django's foreign key relationships specifies that when the referenced object (the parent)
    # is deleted, all related objects (the children) that reference it should also be deleted automatically.
    # This helps maintain database integrity by ensuring there are no orphaned records.

    author = models.CharField(max_length=20)
    text = models.TextField()# This field will hold the contents of the comment
    created_date = models.DateTimeField(default=now)
    approved_comment = models.BooleanField(default=False)# The comment will come unapproved as default this field  shwo wether a comment has been approved or not
    # This should also match with the corresponding field in the Post model method

    def approve(self):
        """
        This method will be used to change the approve status of a comment
        :return:
        """
        self.approved_comments = True
        self.save()

    def get_absolute_url(self):
        """
        After a comment has been made.
        The app will return the user to main page which will list off all the posts
        :return:
        """
        return reverse('blog:post_list')

    def __str__(self):
        return self.text
