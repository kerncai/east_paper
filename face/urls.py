from django.urls import path

from face import views

app_name = "face"

urlpatterns = [ 
    path('face_images_upload.html',views.Face_image_upload.as_view(), name='face_images_upload'),

    #人脸检测列表
    path('face_check_list.html',views.Face_check_list.as_view(), name='face_check_list'),
    path('face_check_results_detail_<int:pk>.html',views.Face_check_results_detail.as_view(),name='face_check_results_detail'),

    path('face_diff_list.html',views.Face_diff_list.as_view(), name='face_diff_list'),
    path('face_diff_results_detail_<int:pk>.html',views.Face_diff_results_detail.as_view(),name='face_diff_results_detail'),

    path('face_core_body_list.html',views.Face_core_body_list.as_view(), name='face_core_body_list'),
    path('face_core_body_results_detail_<int:pk>.html',views.Face_core_body_results_detail.as_view(),name='face_core_body_results_detail'),
    
    #动作
    path('face_all_del.html',views.Face_all_del.as_view(), name='face_all_del'),
    path('face_all_action.html',views.Face_all_action.as_view(), name='face_all_action'),


]
