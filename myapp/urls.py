from django.urls import path, include
from .views import *

urlpatterns = [
   path('beauty/', beauty_fun,name='beauty'),
   path('', index_fun, name='index'), 
   path('contact/', contact_fun, name='contact'),
   path('fashion/', fashion_fun, name='fashion'),
   path('register/', reg_function, name='register'),
   path('register_submit/', register_submit, name='register_submit'),
   path('otp/', otp_fun, name='otp'),
   path('login/', login, name='login'),
   path('logout/', logout, name='logout'),
   path('add_blog/', add_blog, name='add_blog'),
   path('my_blogs/', my_blogs, name='my_blogs'),
   path('singleblog/<int:pk>', singleblog, name='singleblog'),
   path('add_comment/<int:bid>', add_comment, name='add_comment'),
   path('search_blog/', search_blog, name='search_blog'),
   path('donate/<int:bid>', donate, name='donate'),
   path('donate/paymenthandler/', paymenthandler, name='paymenthandler' )
   
   # path('test/', test)





 

]
