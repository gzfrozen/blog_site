from django.forms import ModelForm, TextInput, Textarea, Select, SelectMultiple, ClearableFileInput

from blog.models import Post, Comment, Reply


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'tags', 'title',
                  'content', 'image', 'description')
        widgets = {
            'category': Select(attrs={
                'class': 'form-control',
            }),
            'tags': SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ここにタイトルを入力してください。',
            }),
            'content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'ここでポストを編集してください。',
            }),
            'image': ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '簡単の説明。',
            }),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'コメント内容',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '返信内容',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }
