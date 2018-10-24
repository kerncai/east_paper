from django import forms
from .models import Ocr_images_upload


#__all__ = [
#    'Ocr_images_upload',
#]

class Ocr_images_upload_Form(forms.ModelForm):
    class Meta:
        model = Ocr_images_upload
        fields = ['image_name','ocr_action_type','ocr_image_path','ocr_image_path1']
        widgets = {
			'ctime': forms.DateInput(
                attrs={'type': 'date', }
            ),
		    'utime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'ocr_action_type': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': '选择识别类型'}),
        }
        help_texts = {
            'image_name': "*必填项目,名字不可以重复",
            'ocr_image_path': '上传识别图片',
            'ocr_image_path1': '非身份证请不要上传该项',
        }


