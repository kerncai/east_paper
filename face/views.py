from django.http import HttpResponse
from django.shortcuts import redirect  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView, UpdateView, DetailView
from django.db.models import Q
from face.models import Face_images_upload,Face_check_results,Face_diff_results,Face_core_body_results
from name.models import Names
from face.form import Face_images_upload_Form
from qcloud_image import Client,CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers

import json,os,logging
import datetime

logger = logging.getLogger('face')

appid = "xxxxxxx"
secret_id = "xxxxxxxxxxxxxxxxxxxxxxxx"
secret_key = "xxxxxxxxxxxxxxxxxxxxxxx"
bucket = 'BUCKET'
face_client = Client(appid, secret_id, secret_key, bucket)
face_client.use_http()
face_client.set_timeout(30)

code_list = []    
code_value = {'-5801':'请求缺少身份证号码或身份证姓名'
                ,'-5802':'服务器内部接口错误，服务暂时不可用'
                ,'-5803':'身份证姓名与身份证号码不一致'
                ,'-5804':'身份证号码无效（因户口变动，极少数正常用户也会返回这个结果，此类用户无法使用本服务'
                ,'-5805':'用户未输入图像或者 url 下载失败'
                ,'-5806':'身份证号码与身份证姓名不匹配'
                ,'-5809':'用户身份证登记照无效'}
for i in code_value:
    code_list.append(i)

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_user(request):
    print (request.user)
    return request.user

class Face_image_upload(LoginRequiredMixin, CreateView):
    '''
    脸部图片上传
    '''
    
    model = Face_images_upload
    form_class = Face_images_upload_Form
    template_name = 'face/face_images_upload.html'
    success_url = reverse_lazy('face:face_images_upload')


    def get_context_data(self, **kwargs):
        context = {
            "face_active": "active",
            "face_images_upload_active": "active",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self,form,**kwargs):
        #校验form表单，通过后获取到当前登录名，然后提交
        name = Names.objects.get(username=self.request.user)
        form.instance.upload_name = name
        form.save()
        return redirect(self.success_url)  #重定向

#    def form_invalid(self, form):
#        print(form)
#        return HttpResponse("form is invalid.. this is just an HttpResponse object")

class Face_check_list(LoginRequiredMixin, ListView):
    """
    人脸检测列表
    """
    template_name = 'face/face_check_list.html'
    model = Face_images_upload

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        login_user_name = self.request.user
        is_superuser = Names.objects.values('is_superuser').get(username=login_user_name)
        if is_superuser['is_superuser'] == True:
            queryset = Face_images_upload.objects.filter(face_action_type=0).order_by('-ctime')
        else:
            queryset = Face_images_upload.objects.filter(face_action_type=0,upload_name=login_user_name).order_by('-ctime')

        context = {
            "face_active": "active",
            "face_check_list_active": "active",
            "face_check_list":queryset,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class Face_diff_list(LoginRequiredMixin, ListView):
    """
    人脸对比列表
    """
    template_name = 'face/face_diff_list.html'
    model = Face_images_upload
    ordering = ('-ctime',)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        login_user_name = self.request.user
        is_superuser = Names.objects.values('is_superuser').get(username=login_user_name)
        if is_superuser['is_superuser'] == True:
            queryset = Face_images_upload.objects.filter(face_action_type=1).order_by('-ctime')
        else:
            queryset = Face_images_upload.objects.filter(face_action_type=1,upload_name=login_user_name).order_by('-ctime')
        context = {
            "face_active": "active",
            "face_diff_list_active": "active",
            "face_diff_list": queryset,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
 
class Face_core_body_list(LoginRequiredMixin, ListView):
    """
    人脸核身
    """
    template_name = 'face/face_core_body_list.html'
    model = Face_images_upload
    ordering = ('-ctime',)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        login_user_name = self.request.user
        is_superuser = Names.objects.values('is_superuser').get(username=login_user_name)
        if is_superuser['is_superuser'] == True:
            queryset = Face_images_upload.objects.filter(face_action_type=2).order_by('-ctime')
        else:
            queryset = Face_images_upload.objects.filter(face_action_type=2,upload_name=login_user_name).order_by('-ctime')
        context = {
            "face_active": "active",
            "face_core_body_list_active": "active",
            "face_core_body_list": queryset,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class Face_all_del(LoginRequiredMixin, View):
    '''
    人脸图片删除
    '''
    model = Face_images_upload

    @staticmethod
    def post(request):
        print(request.POST.get('nid'))
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                ids = request.POST.get('nid', None)
                Face_images_upload.objects.get(id=ids).delete()
            else:
                ids = request.POST.getlist('id', None)
                idstring = ','.join(ids)
                Face_images_upload.objects.extra(
                    where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,没有权限{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


class Face_all_action(LoginRequiredMixin,View):
    '''
    处理图片
    '''

    @staticmethod
    def post(request):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('action_id'):
                ids = request.POST.get('action_id', None)
                face_all_list = Face_images_upload.objects.filter(id=ids).values_list('id','face_action_type','face_action_status'
                                                                                    ,'face_image_path1','face_image_path2','ID_card'
                                                                                    ,'ID_card_name') 
                face_upload_id = list(face_all_list[0])[0]
                face_upload_type = list(face_all_list[0])[1]
                face_upload_status = list(face_all_list[0])[2]
                face_upload_path1 = list(face_all_list[0])[3]
                face_upload_path2 = list(face_all_list[0])[4]
                face_id_card = list(face_all_list[0])[5]
                face_id_card_name = list(face_all_list[0])[6]
                if not face_upload_path1:
                    ret['status'] = False
                    ret['error'] = '图片检测失败,图片不存在！({})'.format(face_status['code'])
                    
                #计算人脸检测功能
                if face_upload_type == 0:
                    face_status = face_client.face_detect(CIFile(face_upload_path1),1)
#                    os.system('ls -al %s' %face_upload_path1)
#                    print (face_status)
                    if (face_status['message']) == 'OK' and face_status['httpcode'] == 200 and face_status['code'] == 0:
#                        print ("第一步")
                        if not Face_check_results.objects.filter(face_image_upload_relation=ids).values_list('face_image_upload_relation'): 
                            Face_check_results.objects.create(face_image_upload_relation_id=ids)

                        face_check_image_width = face_status['data']['image_width']
                        face_check_image_height = face_status['data']['image_height']
                        face_check = face_status['data']['face'][0]
                        face_check_gender = int(face_check['gender'])
                        face_check_age = face_check['age']
                        face_check_expression = face_check['expression']
                        face_check_glass = face_check['glass']
                        face_check_pitch = face_check['pitch']
                        face_check_yaw = face_check['yaw']
                        face_check_beauty = face_check['beauty']
                        face_check_width = face_check['width']
                        face_check_height = face_check['height']
                        face_check_results_status = 1
                        face_image_upload_relation_id = request.POST.get('action_id') 
                        face_action_user = str(request.user)
                        Face_check_results.objects.filter(face_image_upload_relation=ids).update(face_check_image_width=face_check_image_width,face_check_image_height=face_check_image_height,face_check_gender=face_check_gender,face_check_age=face_check_age,face_check_expression=face_check_expression,face_check_glass=face_check_glass,face_check_pitch=face_check_pitch,face_check_yaw=face_check_yaw,face_check_beauty=face_check_beauty,face_check_width=face_check_width,face_check_height=face_check_height,face_check_results_status=face_check_results_status,face_action_user=face_action_user,ctime=now)
                        idr = list(Face_check_results.objects.filter(face_image_upload_relation=ids).values_list('id')[0])[0]
                        Face_images_upload.objects.filter(id=ids).update(face_action_status=idr)
                    else:
                        ret['status'] = False
                        ret['error'] = '脸部检测失败,请确认是否是人类脸部图片！({})'.format(face_status['code'])
                #人脸对比检测
                if face_upload_type == 1:
                    face_status = face_client.face_compare(CIFile(face_upload_path1), CIFile(face_upload_path2))
                    if (face_status['message']) == 'OK' and face_status['httpcode'] == 200 and face_status['code'] == 0:
                        if not Face_diff_results.objects.filter(face_image_upload_relation=ids).values_list('face_image_upload_relation'): 
                            Face_diff_results.objects.create(face_image_upload_relation_id=ids)
                        face_image_upload_relation_id = request.POST.get('action_id') 
                        face_action_user = str(request.user)
                        face_diff_results_status = 1
                        face_similarity = face_status['data']['similarity']
                        Face_diff_results.objects.filter(face_image_upload_relation=ids).update(face_image_upload_relation_id=face_image_upload_relation_id,face_action_user=face_action_user,face_diff_results_status=face_diff_results_status,face_similarity=face_similarity,ctime=now)                
                        idr = list(Face_diff_results.objects.filter(face_image_upload_relation=ids).values_list('id')[0])[0]
                        Face_images_upload.objects.filter(id=ids).update(face_action_status=idr)

                    else:
                        ret['status'] = False
                        ret['error'] = "第 %s 张图片检测失败,code %s" %(face_status['data']['fail_flag'],face_status['code'])
                if face_upload_type == 2:
                    face_status = face_client.face_idcardcompare(face_id_card,face_id_card_name,CIFile(face_upload_path1))
                    print (face_status,face_id_card,face_id_card_name,face_upload_path1)
                    if (face_status['message']) == 'OK' and face_status['httpcode'] == 200 and face_status['code'] == 0:
                        if not Face_core_body_results.objects.filter(face_image_upload_relation=ids).values_list('face_image_upload_relation'): 
                            Face_core_body_results.objects.create(face_image_upload_relation_id=ids)
                        face_image_upload_relation_id = request.POST.get('action_id')
                        face_action_user = str(request.user)
                        face_core_body_results_status = 1
                        face_similarity = face_status['data']['similarity']
                        Face_core_body_results.objects.filter(face_image_upload_relation=ids).update(face_image_upload_relation_id=face_image_upload_relation_id,face_action_user=face_action_user,face_core_body_results_status=face_core_body_results_status,face_similarity=face_similarity,face_id_card_name=face_id_card_name,face_id_card=face_id_card,ctime=now)


                        idr = list(Face_core_body_results.objects.filter(face_image_upload_relation=ids).values_list('id')[0])[0]
                        Face_images_upload.objects.filter(id=ids).update(face_action_status=idr)
                
                    elif str(face_status['code']) in code_list:
                        ret['status'] = False
                        ret['error'] = '执行失败 ({})'.format(code_value[str(face_status['code'])])

                        
                    else:
                        ret['status'] = False
                        ret['error'] = '人脸识别失败 ({})'.format(face_status['message'])

                        
        except Exception as e:
            ret['status'] = False
            ret['error'] = '执行请求错误，请联系kernycai ({})'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))

class Face_check_results_detail(LoginRequiredMixin, DetailView):
    '''
    人脸检测结果
    '''
    model = Face_check_results
    template_name = 'face/face_check_results_detail.html'
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        upload_table = Face_images_upload.objects.get(face_action_status=pk,face_action_type=0)
        try:
            results_table = Face_check_results.objects.get(id=pk)
        except Exception as e:
            results_table = {'result': "还未完成,请稍后再查看！！"}
        context = { 
            "face_active": "active",
            "face_check_list_active": "active",
            "upload_table": upload_table,
            "results_table": results_table,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class Face_diff_results_detail(LoginRequiredMixin, DetailView):
    '''
    人脸对比结果
    '''
    model = Face_diff_results
    template_name = 'face/face_diff_results_detail.html'
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        upload_table = Face_images_upload.objects.get(face_action_status=pk,face_action_type=1)
        try:
            results_table = Face_diff_results.objects.get(id=pk)
        except Exception as e:
            results_table = {'result': "还未完成,请稍后再查看！！"}
        context = { 
            "face_active": "active",
            "face_diff_list_active": "active",
            "upload_table": upload_table,
            "results_table": results_table,
        }
        kwargs.update(context)
        print ('test')
        return super().get_context_data(**kwargs)

class Face_core_body_results_detail(LoginRequiredMixin, DetailView):
    '''
    人脸核身结果
    '''
    model = Face_core_body_results
    template_name = 'face/face_core_body_results_detail.html'
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        upload_table = Face_images_upload.objects.get(face_action_status=pk,face_action_type=2)
        try:
            results_table = Face_core_body_results.objects.get(id=pk)
        except Exception as e:
            results_table = {'result': "还未完成,请稍后再查看！！"}
        context = { 
            "face_active": "active",
            "face_core_body_list_active": "active",
            "upload_table": upload_table,
            "results_table": results_table,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
