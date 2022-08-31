from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('chatbot', views.ChatbotViewSet,basename='chatbot')
router.register('categories', views.CategoriesViewSet,basename='categories')
router.register('types', views.TypesViewSet,basename='types')
router.register('answers', views.AnswersViewSet,basename='answers')
router.register('read_excel', views.ReadExcelViewSet,basename='read_excel')

# URLConf
urlpatterns = router.urls