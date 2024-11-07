from django import forms

from blog.models import Blog

class StyleMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # if field_name != 'current_version_indicator' and field_name != 'publication_sign' and field_name != 'is_published':
            field.widget.attrs["class"] = "form-control"


class BlogForm(StyleMixin):

    class Meta:
        model = Blog
        fields = "__all__"