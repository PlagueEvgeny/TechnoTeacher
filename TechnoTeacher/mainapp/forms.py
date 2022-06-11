from django import forms
from django.forms.widgets import HiddenInput
from djangocodemirror.fields import CodeMirrorField
from mainapp.models import Course, Task, Content, Sollution, ContactEvent


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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'course',
            'content',
            'name',
            'desc',
            'difficulty',
            'test',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'course_form'


class CodeForm(forms.ModelForm):
    class Meta:
        model = Sollution
        fields = (
            'task',
            'code',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['id'] = 'codes'
            if name == 'task':
                item.widget = HiddenInput()


class ContactEventForm(forms.ModelForm):
    class Meta:
        model = ContactEvent
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for name, item in self.fields.items():
                item.widget.attrs['class'] = 'contact-events'
