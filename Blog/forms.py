from django import forms
from Blog.models import Post, Comments

class PostForm(forms.ModelForm):
    """
    This Form class will work very closely with the corresponding model.

    A form is a recepticle for data
    The user will input data into the form and the form will store the data in the model.

    Definetivly the data will be inmput into the sql database
    """

    class Meta():
        model = Post
        fields = ('author','title','text','post_image','image_name')# The date fields dont need to be put in because
                                          # allowing the date to be a field would allow the
                                          # user to be able to add and change the date

        # The classes allow to connect css classes to the entry fields
        widgets = {
            'title': forms.TextInput(attrs={'class':'textinputclass form-control'}),
            'text' : forms.Textarea(attrs= {'class':'editable form-control medium-editor-textarea postcontent',
                                            'placeholder':'Write your post here', 'style':'min-height: 300px;'})
        }



class CommentForm(forms.ModelForm):

    class Meta():
        model = Comments
        fields = ('author','text')

        widget = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }