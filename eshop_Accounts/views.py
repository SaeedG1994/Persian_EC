from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from eshop_Cart.models import Cart, CartItem
from eshop_Cart.views import _cart_id
import  requests
from .form import RegistrationForm
from .models import Account

#VERIFICATION EMAIL IMPORT
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# THIS FUNCTION FOR REGISTER USER AND SEND ACTIVATE LINK
#-------------------------------------------------------
def register_user(request):
    if request.method == 'POST':
         form = RegistrationForm(request.POST)
         if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name =form.cleaned_data['last_name']
            phone_number =form.cleaned_data['phone_number']
            email =form.cleaned_data['email']
            password =form.cleaned_data['password']
            username =email.split("@")[0]
            user =Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number =phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Please Activate Your Account "
            message = render_to_string('shared/eshop_account/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email =email
            send_email =EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # messages.success(request,"Thank you For Registration .")
            return redirect('/login/?command=verification&email='+email)
    else:
        form =RegistrationForm()
    context ={
        'form':form
    }
    return render(request,'shared/eshop_account/Register.html',context)


# THIS FUNCTION FOR ACTIVATE USER  (  WHEN USER CLICK ON THE ACTIVATE LINK )
#----------------------------------------------------------------------
def email_activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations! Your Account Is Activated.')
        return redirect('login_user')
    else:
        messages.error(request,'Invalid Activation link !!!')
        return redirect('register_user')

@login_required(login_url='login')
def dashboard_user(request):
    return render(request,'shared/eshop_account/dashboard.html')



#THIS FUNCTION FOR LOGIN USER
#-----------------------------
def login_user(request):
    if request.method == 'POST':
        email =request.POST['email']
        password =request.POST['password']

        user =auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(cart=cart)

                    #GETTING THE PRODUCT VARIATIONS BY CART ID
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    #GET THE CART ITEMS FROM THE USER TO ACCESS  HIS PRODUCT VARIATIONS
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # product_variation = [1,2,3,4,6]
                    # ex_var_list = [4,6,3,5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,'You are logged in .')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query

                # next/cart/checkout/
                params = dict(x.split('=') for x  in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                return redirect('dashboard_user')
        else:
            messages.error(request,'Invalid login credentials.')
            return redirect('login_user')
    return render(request, 'shared/eshop_account/Login.html')


#THIS FUNCTION FOR LOGOUT USER FORM USER PANEL
#---------------------------------------------
@login_required(login_url='login_user')
def logout_user(request):
    auth.logout(request)
    # messages.success(request,'you are logged out ')
    return redirect('index') # Home page




#THIS FUNCTION SEND AN EMAIL TO EMAIL USERS FOR   (FORGOT USER)
#------------------------------------------
def forgotPassword_user(request):
    if request.method == 'POST':
        email =request.POST['email']
        if Account.objects.filter(email=email).exists():
            user =Account.objects.get(email__exact=email)

            #RESET PASSWORD EMAIL
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message =render_to_string('shared/eshop_account/reset_verification_email.html', {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email =email
            send_email =EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password Reset Email Has Been To Your Email Address. ')
            return redirect('login_user')
        else:
            messages.error(request,'Account  Does Not Exist !!! ')
            return redirect('forgotPassword_user')

    return render(request,'shared/eshop_account/ForgotPassword.html')



# RETURN USER TO (RESET PASSWORD PAGE) THROUGH THE ACTIVE LINK 
#--------------------------------------------------
def resetPassword_value(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] =uid
        messages.info(request,'Please Reset your Password')
        return redirect('emailResetPassword')
    else:
        messages.error(request,'This Link Had Been Expired !')
        return redirect('login_user')


# AND FINALLY RETURN USER  FOR RESET PASSWORD.......THE EMAIL USER
#------------------------------------------------------
def emailResetPassword(request):
    if request.method == 'POST':
        password =request.POST['password']
        confirm_password =request.POST['confirm_password']

        if password ==confirm_password:
            uid =request.session.get('uid')
            user= Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Your Password Successful Changed.')
            return redirect('login_user')
        else:
            messages.error(request,'Your Password Does Not Match ')
            return redirect('emailResetPassword')
    else:
        return render(request,'shared/eshop_account/ResetPassword.html')