from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import redirect  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView, UpdateView, DetailView
from django.db.models import Q
from name.models import Names
from ocr.models import Ocr_images_upload
from ocr.form import Ocr_images_upload_Form
from qcloud_image import Client,CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers
import json,os

appid = "1253879462"
secret_id = "AKIDA9tMbdGzKQHsDIAwQfgS0KPWP3RZt5Tb"
secret_key = "1mIYYIrBG6h2B8pGRN0PZT8XhiY8VeZQ"
bucket = 'BUCKET'
ocr_client = Client(appid, secret_id, secret_key, bucket)
ocr_client.use_http()
ocr_client.set_timeout(30)

class Ocr_image_upload(LoginRequiredMixin, CreateView):
    '''
    OCR图片上传
    '''
    
    model = Ocr_images_upload
    form_class = Ocr_images_upload_Form
    template_name = 'ocr/ocr_images_upload.html'
    success_url = reverse_lazy('ocr:ocr_images_upload')


    def get_context_data(self, **kwargs):
        context = {
            "ocr_active": "active",
            "ocr_images_upload_active": "active",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self,form,**kwargs):
        #校验form表单，通过后获取到当前登录名，然后提交
        name = Names.objects.get(username=self.request.user)
        form.instance.upload_name = name
        form.save()
        return redirect(self.success_url)  #重定向

class IDcards_check_list(LoginRequiredMixin, ListView):
    """
    身份证识别列表
    """
    template_name = 'ocr/idcards_check_list.html'
    context_object_name = 'idcards_check_list'
    model = Ocr_images_upload
    queryset = Ocr_images_upload.objects.filter(ocr_action_type=0)
    ordering = ('-ctime',)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            "ocr_active": "active",
            "idcards_check_list_active": "active",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class Ocr_all_del(LoginRequiredMixin, View):
    '''
    身份证列表删除
    '''
    model = Ocr_images_upload

    @staticmethod
    def post(request):
        print(request.POST.get('nid'))
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                ids = request.POST.get('nid', None)
                Ocr_images_upload.objects.get(id=ids).delete()
            else:
                ids = request.POST.getlist('id', None)
                idstring = ','.join(ids)
                Ocr_images_upload.objects.extra(
                    where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,没有权限{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))

class Ocr_all_action(LoginRequiredMixin,View):
    '''
    OCR识别
    '''

    @staticmethod
    def post(request):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('action_id'):
                ids = request.POST.get('action_id', None)
                ocr_all_list = Ocr_images_upload.objects.filter(id=ids).values_list('id','ocr_action_type','ocr_action_status'
                                                                                    ,'ocr_image_path','ocr_image_path1') 
                ocr_upload_id = list(ocr_all_list[0])[0]
                ocr_upload_type = list(ocr_all_list[0])[1]
                ocr_upload_status = list(ocr_all_list[0])[2]
                ocr_upload_path1 = list(ocr_all_list[0])[3]
                ocr_upload_path2 = list(ocr_all_list[0])[4]
                if ocr_upload_path1:
                    #开始身份证识别
                    if ocr_upload_type == 0:
                        os.system('ls -al %s' %ocr_upload_path1)
                        idcard_front_status = ocr_client.idcard_detect(CIFiles([ocr_upload_path1]),1)
                        idcard_con_status = ocr_client.idcard_detect(CIFiles([ocr_upload_path2]),0)
                        if idcard_front_status['httpcode'] == 200 and idcard_front_status['result_list'][0]['code'] == 0 and idcard_front_status['result_list'][0]['message'] == 'OK':
                            authority = idcard_front_status['result_list'][0]['data']['authority']
                            valid_date = idcard_front_status['result_list'][0]['data']['valid_date']
                        if idcard_con_status['httpcode'] == 200 and idcard_con_status['result_list'][0]['code'] == 0 and idcard_con_status['result_list'][0]['message'] == 'OK':
                            name = idcard_con_status['result_list'][0]['data']['name']
                            sex = idcard_con_status['result_list'][0]['data']['sex']
                            birth = idcard_con_status['result_list'][0]['data']['birth']
                            nation = idcard_con_status['result_list'][0]['data']['nation']
                            idcard_id = idcard_con_status['result_list'][0]['data']['id']
                            address = idcard_con_status['result_list'][0]['data']['address']

                            print (authority,valid_date,name,sex,birth,nation,idcard_id,address)
				
                else:
                    ret['status'] = False
                    ret['error'] = '图片检测失败,图片不存在！({})'.format(['code'])

        except Exception as e:
            ret['status'] = False
            ret['error'] = '执行请求错误，请联系kernycai ({})'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))

