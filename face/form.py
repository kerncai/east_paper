from django import forms
from .models import Face_images_upload


#__all__ = [
#    'Face_images_upload',
#]

class Face_images_upload_Form(forms.ModelForm):
    class Meta:
        model = Face_images_upload
        fields = ['image_name','face_action_type','face_image_path1','face_image_path2','ID_card','ID_card_name']
        widgets = {
			'ctime': forms.DateInput(
                attrs={'type': 'date', }
            ),
		    'utime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'face_action_type': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': '选择识别类型'}),
        }
        help_texts = {
            'image_name': "*必填项目,名字不可以重复",
        }


