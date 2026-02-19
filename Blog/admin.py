from django.contrib import admin
from Blog.models import Post, Comments
# Register your models here.
admin.site.register(Post)
#admin.site.register(PostFile)
admin.site.register(Comments)