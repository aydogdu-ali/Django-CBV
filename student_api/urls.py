
from django.urls import path,include

from rest_framework import routers

from .views import (
    home,
    #APIViews methodu
    # StudentListCreate,  
    # StudentDetail,
    #  
    #GenericAPIViews
    #StudentGAV,
    #StudentDetailGAV
    # Concrete Methodu
    #StudentCV,
    #StudentDetailCV,

    #Views Methodu
    StudentMVS,
    PathMVS

  )

router = routers.DefaultRouter()
router.register("student",StudentMVS) #endpoint imizi burda belirtmiş oluyoruz.
router.register("path",PathMVS) 

urlpatterns = [
    path("", home),
  #   #APIViews methodu
  #   path('student/', StudentListCreate.as_view()),
  #   path('student/<int:pk>', StudentDetail.as_view()),

  # GenericAPIViews Methodu
  # path('student/', StudentGAV.as_view()),
  # path('student/<int:pk>', StudentDetailGAV.as_view()),

  # Concrete Methodu
  # path('student/', StudentCV.as_view()),
  # path('student/<int:pk>', StudentDetailCV.as_view()),

  #Views Methodu
  path("",include(router.urls))
   ]

# urlpatterns += router.urls içine yazmak yerine böylede kullanabiliriz.






    

