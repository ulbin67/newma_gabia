from django import forms
class ApplySearchForm(forms.Form):
    CHART_CHOICE = (
        ('#1', '막대 그래프'),
        ('#2', '파이 그래프'),
        ('#3', '선 그래프')
    )
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control date-field'}), label='시작일자')
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control date-field'}), label='종료일자(하루 뒤로 지정해주세요)')
    chart_type = forms.ChoiceField(choices=CHART_CHOICE, label='차트 종류')

class ApplyForm(forms.Form):
    date_from2 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control date-field'}), label='시작일자')
    date_to2 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control date-field'}), label='종료일자(하루 뒤로 지정해주세요)')
    company_info = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        label='회사명 또는 담당자명',
        required=False,
    )
