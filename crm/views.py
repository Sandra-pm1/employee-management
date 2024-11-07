from django.shortcuts import render,redirect
from django.views.generic import View
from crm.forms import EmployeeForm,SignUpForm,SignInForm
from crm.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from crm.decorators import signin_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

decs=[signin_required,never_cache]

@method_decorator(decs,name="dispatch")
class EmployeeCreateView(View):
    template_name="employee_add.html"
    form_class=EmployeeForm
    def get(self,request,*args,**kwargs):
        # create form_instance
        form_instance=self.form_class()
        # render form into template
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        # extract form_data
        form_data=request.POST 
        # initialize form with form_data
        form_instance=self.form_class(form_data,files=request.FILES)
        # check form has no errors
        if form_instance.is_valid():
            # save form_instance
            form_instance.save()
            messages.success(request,"New employee has been created")
            return redirect("employee-list")
        messages.error(request,"Failed to add employee")
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class EmployeeListView(View):
    template_name="employee_list.html"
    def get(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        return render(request,self.template_name,{"data":qs})

@method_decorator(decs,name="dispatch")
class EmployeeDetailView(View):
    template_name="employee_detail.html"
    def get(self,request,*args,**kwargs):
        # extract pk from url
        id=kwargs.get("pk")
        # fetch employee with id=id
        qs=Employee.objects.get(id=id)
        return render(request,self.template_name,{"data":qs})

@method_decorator(decs,name="dispatch")
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employee.objects.get(id=id).delete()
        messages.success(request,"Employee has been deleted")
        return redirect("employee-list")

@method_decorator(decs,name="dispatch")
class EmployeeUpdateView(View):
    template_name="employee_update.html"
    form_class=EmployeeForm
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        employee_object=Employee.objects.get(id=id)
        # initialize form_instance with employee object
        form_instance=self.form_class(instance=employee_object)
        return render(request,self.template_name,{"form":form_instance})    
    def post(self,request,*args,**kwargs):
        # extract id
        id=kwargs.get("pk")
        # fetch employee id
        employee_object=Employee.objects.get(id=id)
        # extract form_data
        form_data=request.POST 
        # initialise form_instance
        form_instance=self.form_class(form_data,files=request.FILES,instance=employee_object)
        # check for errors in form_instance
        if form_instance.is_valid():
            form_instance.save()
            messages.success(request,"Successfully updated")
            return redirect("employee-list")
        messages.error(request,"Failed to update employee")
        return render(request,self.template_name,{"form":form_instance})

class SignUpView(View):
    template_name="register.html"
    form_class=SignUpForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        form_data=request.POST 
        form_instance=self.form_class(form_data)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            User.objects.create_user(**data)
            return redirect("register")
        return rendre(request,self.template_name,{"form":form_instance})

class SignInView(View):
    template_name="signin.html"
    form_class=SignInForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=self.form_class(form_data)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("employee-list")
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

