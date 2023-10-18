# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django import forms
from django.forms import Textarea
# Internal:
from .models import Album, Genre, Review
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class AlbumForm(forms.ModelForm):
    """
    A class to create Album model form
    """
    class Meta:
        model = Album
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genres = Genre.objects.all()
        friendly_names = [(g.id, g.get_friendly_name()) for g in genres]

        self.fields['genre'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True


class ReviewForm(forms.ModelForm):
    """
    A class to create Review model form
    """
    class Meta:
        model = Review
        fields = ('body',)
        widgets = {
            'body': Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False
