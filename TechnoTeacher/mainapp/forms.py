from django import forms
from django.forms.widgets import HiddenInput
from djangocodemirror.fields import CodeMirrorField
from mainapp.models import Course, Task, Content, Sollution


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
            'status',
            'test',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'task_form'


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
