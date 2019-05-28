import mistune

from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    nick_name = forms.CharField(
        max_length=50,
        label='昵称',
        widget=forms.widgets.Input(attrs={'class': 'form-control', 'style': 'width: 60%;'})
    )
    email = forms.EmailField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(attrs={'class': 'form-control', 'style': 'width: 60%;'}))
    website = forms.URLField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(attrs={'class': 'form-control', 'style': 'width: 60%;'})
    )
    content = forms.CharField(
        max_length=500,
        label='内容',
        widget=forms.widgets.Textarea(attrs={'class': 'form-control', 'rows': 6})
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度太短！')
        return mistune.markdown(content)

    class Meta:
        model = Comment
        fields = ['nick_name', 'email', 'website', 'content']
