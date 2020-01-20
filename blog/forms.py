from django.forms import (inlineformset_factory, ModelForm, TextInput,
                          Textarea, Select, SelectMultiple, ClearableFileInput)

from blog.models import Post, ContentImage, Comment, Reply


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'tags', 'title',
                  'content', 'image', 'description')
        labels = {
            'category': 'カテゴリー（必要）',
            'tags': 'タグ（複数選択可）',
            'title': 'タイトル（必要）',
            'content': 'ポスト本文（必要）',
            'image': 'タイトル画像（省略可）',
            'description': '内容説明（必要）',
        }

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
                'placeholder': 'ここでポスト本文を編集してください。',
            }),
            'image': ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '簡単の説明。',
            }),
        }


class ContentImageForm(ModelForm):
    class Meta:
        model = ContentImage
        fields = ('content_image', 'description')
        labels = {
            'content_image': '添付画像（省略可）',
            'description': '画像説明（省略可）',
        }
        widgets = {
            'content_image': ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'rows': 1,
                'placeholder': '画像の説明。',
            }),
        }


ContentImageFormSet = inlineformset_factory(
    Post, ContentImage, form=ContentImageForm, can_delete=False)


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
