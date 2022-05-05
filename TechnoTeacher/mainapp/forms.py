from django import forms

from mainapp.models import Course, Task, Content

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'category',
            'slug',
            'name',
            'desc',
            'cover',
            'price',
            'teachers',    
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'course_form'



class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = (
            'course',
            'name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'content_form'