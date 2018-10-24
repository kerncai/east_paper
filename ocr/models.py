from django.db import models
from jsonfield import JSONField
import random
import uuid

__all__ = [
    'Ocr_images_upload',
]


class Ocr_images_upload(models.Model):
    OCR_ACTION_TYPE = (
        (0,'身份证'),
        (1,'名片'),
    )
    image_name = models.CharField(max_length=255, verbose_name='图片名称', null=True,unique=True,error_messages={'invalid': '名称重复.'})
    upload_name = models.CharField(max_length=255, verbose_name='上传者', null=True)
    ocr_action_type = models.IntegerField(choices=OCR_ACTION_TYPE, verbose_name='识别动作')
    ocr_image_path = models.FileField(upload_to='upload/%Y%m%d{}'.format(random.randint(0, 99999)),
                                        verbose_name="身份证正面(国徽)/名片", null=True, blank=True)
    ocr_image_path1 = models.FileField(upload_to='upload/%Y%m%d{}'.format(random.randint(0, 99999)),
                                        verbose_name="身份证反面", null=True, blank=True)
    ocr_action_status = models.IntegerField(verbose_name='识别对象',default=0)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.image_name, self.upload_name,self.ocr_action_type,self.ocr_image_path,self.ocr_action_status,self.ctime)

    class Meta:
        ordering=['-ctime'] 
        db_table = "Ocr_images_upload"
        verbose_name = "OCR上传"
        verbose_name_plural = verbose_name


class IDcard_check_results(models.Model):
    idcard_action_user = models.CharField(max_length=255, verbose_name='执行者', null=True)
    authority = models.CharField(max_length=255, verbose_name='签发机关', null=True)
    valid_date = models.CharField(max_length=255, verbose_name='有效期限', null=True)
    name = models.CharField(max_length=255, verbose_name='姓名', null=True)
    sex = models.CharField(max_length=255, verbose_name='性别', null=True)
    birth = models.CharField(max_length=255, verbose_name='出生年月', null=True)
    nation = models.CharField(max_length=255, verbose_name='民族', null=True)
    num = models.CharField(max_length=255, verbose_name='公民身份号码', null=True)
    address = models.CharField(max_length=255, verbose_name='住址', null=True)
    idcard_check_results_status = models.IntegerField(verbose_name='检测结果', default=0)
    idcard_image_upload_relation = models.ForeignKey(verbose_name='上传ID', to='Ocr_images_upload', related_name='OCR', on_delete=models.CASCADE,null=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s' % (self.idcard_action_user,self.authority,self.valid_date,self.name,self.sex,self.birth,self.nation,self.num,self.address,self.idcard_check_results_status,self.idcard_image_upload_relation,self.ctime)

    class Meta:
        db_table = "IDcard_check_results"
        verbose_name = "身份证识别"
        verbose_name_plural = verbose_name
