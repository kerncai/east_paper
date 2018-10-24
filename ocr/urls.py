from django.urls import path

from ocr import views

app_name = "ocr"

urlpatterns = [ 
    path('ocr_images_upload.html',views.Ocr_image_upload.as_view(), name='ocr_images_upload'),

    path('idcards_check_list.html',views.IDcards_check_list.as_view(), name='idcards_check_list'),

#    #人脸检测列表
#    path('face_check_list.html',views.Face_check_list.as_view(), name='face_check_list'),
#    path('face_check_results_detail_<int:pk>.html',views.Face_check_results_detail.as_view(),name='face_check_results_detail'),
#
#    path('face_diff_list.html',views.Face_diff_list.as_view(), name='face_diff_list'),
#    path('face_diff_results_detail_<int:pk>.html',views.Face_diff_results_detail.as_view(),name='face_diff_results_detail'),
#
#    path('face_features_list.html',views.Face_features_list.as_view(), name='face_features_list'),
#    
    #动作
    path('ocr_all_del.html',views.Ocr_all_del.as_view(), name='ocr_all_del'),
    path('ocr_all_action.html',views.Ocr_all_action.as_view(), name='ocr_all_action'),
#

]
