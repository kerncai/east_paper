from django.db import models
from jsonfield import JSONField
import django.utils.timezone as timezone
import random
import uuid

__all__ = [
    'Face_images_upload',
    'Face_check_results'
    'Face_diff_results'
]

class Face_images_upload(models.Model):
    FACE_ACTION_TYPE = (
        (0,'人脸检测'),
        (1,'人脸对比'),
        (2,'人脸核身'),
    )
    image_name = models.CharField(max_length=255, verbose_name='图片名称', null=True,unique=True,error_messages={'invalid': '名称重复.'})
    upload_name = models.CharField(max_length=255, verbose_name='上传者', null=True)
    face_action_type = models.IntegerField(choices=FACE_ACTION_TYPE, verbose_name='识别动作')
    face_image_path1 = models.ImageField(upload_to='upload/%Y%m%d{}'.format(random.randint(0, 99999)),
                                        verbose_name="上传照片", null=True, blank=True)
    face_image_path2 = models.ImageField(upload_to='upload/%Y%m%d{}'.format(random.randint(0, 99999)),
                                        verbose_name="对比照片", null=True, blank=True)
    face_action_status = models.IntegerField(verbose_name='识别动作',default=0)
    ID_card_name = models.CharField(max_length=255,verbose_name='姓名',null=True,blank=True)
    ID_card = models.CharField(max_length=255,verbose_name='身份证号码',null=True,blank=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.image_name, self.upload_name,self.face_action_type,self.face_image_path1,self.face_image_path2,self.face_action_status,self.ID_card)

    class Meta:
        ordering=['-ctime'] 
        db_table = "Face_images_upload"
        verbose_name = "人脸识别"
        verbose_name_plural = verbose_name
        permissions = {
            ('read_uploadimages', u"只读操作"),
            ('cmd_uploadimages', u"上传操作"),
        }


class Face_check_results(models.Model):
    face_action_user = models.CharField(max_length=255, verbose_name='执行者', null=True)
    face_check_image_width = models.FloatField(verbose_name='图片宽度', null=True)
    face_check_image_height = models.FloatField(verbose_name='图片高度', null=True)
    face_check_gender = models.IntegerField(verbose_name='性别', null=True)
    face_check_age = models.IntegerField(verbose_name='年龄', null=True)
    face_check_expression = models.IntegerField(verbose_name='笑容', null=True)
    face_check_glass = models.CharField(max_length=20, verbose_name='眼镜', null=True)
    face_check_pitch = models.IntegerField(verbose_name='上下偏移', null=True)
    face_check_yaw = models.IntegerField(verbose_name='左右偏移', null=True)
    face_check_beauty = models.IntegerField(verbose_name='颜值魅力', null=True)
    face_check_width = models.FloatField(verbose_name='脸部宽度', null=True)
    face_check_height = models.FloatField(verbose_name='脸部高度', null=True)
    face_check_results_status = models.IntegerField(verbose_name='检测结果', default=0)
    face_image_upload_relation = models.ForeignKey(verbose_name='上传ID', to='Face_images_upload', related_name='face', on_delete=models.CASCADE,null=True)
    ctime = models.DateTimeField(auto_now=True, verbose_name='操作时间')


    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' %(self.face_action_user,self.face_check_image_width,self.face_check_image_height,self.face_check_gender,self.face_check_age,self.face_check_expression,self.face_check_glass,self.face_check_pitch,self.face_check_yaw,self.face_check_beauty,self.face_check_width,self.face_check_height,self.face_check_results_status,self.face_image_upload_relation_id,self.ctime)

    class Meta:
        db_table = "Face_check_results"
        verbose_name = "人脸检测结果"
        verbose_name_plural = verbose_name


class Face_diff_results(models.Model):
    face_action_user = models.CharField(max_length=255, verbose_name='上传者', null=True)
    face_similarity = models.FloatField(verbose_name='相似度', null=True)
    face_diff_results_status = models.IntegerField(verbose_name='检测结果', default=0)
    face_image_upload_relation = models.ForeignKey(verbose_name='上传ID', to='Face_images_upload', related_name='face_diff', on_delete=models.CASCADE,null=True)
    ctime = models.DateTimeField(auto_now=True, verbose_name='完成时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Face_diff_results"
        verbose_name = "人脸对比"
        verbose_name_plural = verbose_name

class Face_core_body_results(models.Model):
    face_action_user = models.CharField(max_length=255, verbose_name='上传者', null=True)
    face_id_card_name = models.CharField(max_length=255, verbose_name='姓名', null=True)
    face_id_card = models.CharField(max_length=255, verbose_name='身份证号码', null=True)
    face_similarity = models.FloatField(verbose_name='验证结果', null=True)
    face_core_body_results_status = models.IntegerField(verbose_name='检测结果', default=0)
    face_image_upload_relation = models.ForeignKey(verbose_name='上传ID', to='Face_images_upload', related_name='face_core_body', on_delete=models.CASCADE,null=True)
    ctime = models.DateTimeField(auto_now=True, verbose_name='完成时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Face_core_body_results"
        verbose_name = "人脸对比"
        verbose_name_plural = verbose_name
