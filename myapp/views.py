from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import random 
from django.conf import settings
from .models import *
import os
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# Create your views here.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def beauty_fun(request):
    filtered_blogs = Blog.objects.filter(categories = 'beauty')
    try:
        user_obj = User.objects.get(email =  request.session['user_email'])
        return render(request, 'beauty.html', {'beauty': 'jivit', 'userdata':user_obj, 'blogs': filtered_blogs})
    except:
        return render(request, 'beauty.html', {'beauty': 'jivit', 'blogs': filtered_blogs })
    

def index_fun(request):
    try:
        global user_obj
        user_obj = User.objects.get(email =  request.session['user_email'])
        return render(request, 'index.html', {'home': 'jivit', 'userdata':user_obj})
    except:
        return render(request, 'index.html', {'home': 'jivit'})

def contact_fun(request):
    return render(request, 'contact.html' )

def fashion_fun(request):
    filtered_blogs = Blog.objects.filter(categories = 'fashion')
    try:
        user_obj = User.objects.get(email =  request.session['user_email'])
        return render(request, 'fashion.html', {'fashion': 'jivit', 'userdata':user_obj, 'blogs': filtered_blogs})
    except:
        return render(request, 'fashion.html', {'fashion': 'jivit', 'blogs': filtered_blogs})
    

def reg_function(request):
    return render(request, 'register.html')


def register_submit(request):
    
    if request.POST['passwd'] == request.POST['repasswd']:
        global g_otp, user_data
        user_data = [request.POST['fname'], 
                     request.POST['lname'],
                     request.POST['username'],
                     request.POST['email'],
                     request.POST['passwd']]
        g_otp = random.randint(100000, 999999)
        send_mail('Welcome Welcome',
                  f"Your OTP is {g_otp}",
                  settings.EMAIL_HOST_USER,
                  [request.POST['email']])
        return render(request, 'otp.html')        
    else:
        return render(request, 'register.html', {'msg': 'Both passwords do not MATCH'})


def otp_fun(request):
    try:
        if int(request.POST['u_otp']) == g_otp:
            User.objects.create(
                first_name = user_data[0],
                    last_name = user_data[1],
                    username = user_data[2],
                    email = user_data[3],
                    password = user_data[4])
            return render(request, 'register.html', {'msg':'Successfully Registered!!'})
        else:
            return render(request, 'otp.html', {'msg': 'Invalid OTP, Enter again!!!'})
    except:
        return render(request, 'register.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        #get() ye tumhe table mein se EK HI row zuupp karke 
        # de sakta hai 
        # 0 match mile ya to 1 se zyada match mile
        # get method error dega
        try:
            #agar niche wali line pe error aaya matalb email not found
            # get() wo row object return karega , r1 mein store kar dega
            
            user_obj = User.objects.get(email = request.POST['email'])

            if request.POST['passwd'] == user_obj.password:
                request.session['user_email'] = request.POST['email']
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg': 'Invalid password'})
        except:
            return render(request, 'login.html', {'msg':'email is not registered!!'})


def logout(request):
    try:
        del request.session['user_email']
        global user_obj
        del user_obj
        return render(request, 'index.html', {'home': 'jivit'})
    except:
        return redirect('login')


def add_blog(request):
    if request.method == 'GET':
        try:
            return render(request, 'add_blog.html', {'userdata':user_obj})
        except:
            return redirect('login')
    else:
        Blog.objects.create(
            title = request.POST['title'],
            des = request.POST['des'],
            categories = request.POST['cate'],
            pic = request.FILES['foto'],
            #user ek foreign key field hai, isiliye obj dena hai
            user = user_obj
            #ye object jiska session chalu hai uska hai
        )
        return redirect('index')


def my_blogs(request):
    my_filtered_blogs = Blog.objects.filter(user = user_obj)
    return render(request, 'my_blogs.html', {'blogs':my_filtered_blogs, 'userdata':user_obj})


def singleblog(request, pk):
    s_blog = Blog.objects.get(id = pk)
    filtered_comments = Comment.objects.filter(blog= s_blog)
    d_list = Donation.objects.filter(pay_to = s_blog)
    d_amount = 0
    for i in d_list:
        d_amount += i.amount
    

    try:
        return render(request, 'single_blog.html', {"blog":s_blog, 'userdata':user_obj, 'all_comments':filtered_comments, 'donations': d_amount})
    except:
        return render(request, 'single_blog.html', {"blog":s_blog, 'all_comments': filtered_comments, 'donations': d_amount})

def add_comment(request, bid):
    try:
        user_obj = User.objects.get(email = request.session['user_email'])
        blog_obj = Blog.objects.get(id = bid)
        Comment.objects.create(
            message = request.POST['troll'],
            blog = blog_obj,
            user = user_obj
        )
        filtered_comments = Comment.objects.filter(blog = blog_obj)
        return render(request, 'single_blog.html', {"blog":blog_obj, 'userdata':user_obj, 'all_comments': filtered_comments})
    except:
        return redirect('login')


def search_blog(request):
    shabd = request.POST['search']
    filtered_blogs = Blog.objects.filter(title__icontains = shabd )
    return render(request, 'searched_blog.html', {'blogs': filtered_blogs})


def donate(request, bid):
    try:
        user_obj = User.objects.get(email = request.session['user_email'])
        global blog_obj
        blog_obj = Blog.objects.get(id = bid)
        if request.method == 'POST':
            
    #------------------COPIED CODE------------------------------#        
            currency = 'INR'
            global amount
            amount = int(request.POST['pamount']) * 100 

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                            currency=currency,
                                                            payment_capture='0'))
        
            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'
        
            # we need to pass these details to frontend.
            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
        
            return render(request, 'abto.html', context=context)
        else:
            return render(request, 'donate.html', {'blog':blog_obj, 'userdata': user_obj})
    except:
        return redirect('login')
    

"""def test(request):
    with open(os.path.join(settings.BASE_DIR, 'rzp.csv'), 'r') as f1:
        list_of_lines = f1.readlines()
        str1 = list_of_lines[-1]
        final_list = str1.split(",")
        razor_id = final_list[0]
        razor_secret =  final_list[-1][:-1]
        print(razor_secret)
    return HttpResponse('ok')"""


#----------------PURA COPIED FUNCTION-----------------------#
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        user_obj = User.objects.get(email = request.session['user_email'])
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    Donation.objects.create(
                        pay_by = user_obj,
                        pay_to = blog_obj,
                        amount = amount/100 #1000/100
                    )
                    return render(request, 'success.html')

                except:
 
                    # if there is an error while capturing payment.
                    return HttpResponse('paisa not found')
            else:
 
                # if signature verification fails.
                return HttpResponse('paisa not found')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
