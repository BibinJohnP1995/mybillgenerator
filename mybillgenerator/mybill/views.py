from django.shortcuts import render
import requests
import datetime
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from mybill.render import render_to_pdf #created in step 4

"""class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
             'today': datetime.date.today(),
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('pdf/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')"""

class GeneratePDF(View):
    def get(self, request):
        template = get_template('invoice.html')
        context = {
            "customer_name": "b_name"
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



# Create your views here.

def bill_calc(request):
	dc = Buildings.objects.filter(buil_reg=request.session['log'])
	if request.method == 'POST':
		b_no = request.POST.get('building')
		f_date = request.POST.get('from_date')
		t_date = request.POST.get('to_date')
		f_reading = 0
		t_reading = 0
		amount = 0
		difference = 0
		db = Buildings.objects.get(buil_reg=request.session['log'], Building_number=b_no)
		b_name = db.Building_name
		dd = Readings.objects.filter(r_reg = db.id)

		for i in dd:
			if str(i.Reading_date) == str(f_date):
				f_reading = i.Reading
			if str(i.Reading_date) == str(t_date):
				t_reading = i.Reading
		if not f_reading:
			messages.success(request, 'reading empty on the selected FROM DATE')
			return render(request, 'bill_calc.html', {'dc': dc})

		if not t_reading:
			messages.success(request, 'reading empty on the selected TO DATE')
			return render(request, 'bill_calc.html', {'dc': dc})
		difference =t_reading - f_reading
		amount = (difference)*10

		dk = Registration.objects.get(id = request.session['log'])
		name = dk.Name
		phone = dk.Phone
		x = datetime.datetime.now()
		y = x.strftime("%Y-%m-%d")

		vb = Calculation()
		vb.Building_name = b_name
		vb.Building_number = b_no
		vb.Date_from = f_date
		vb.Previous_reading = f_reading
		vb.Date_to = t_date
		vb.Current_reading = t_reading
		vb.Amount = amount
		vb.Bill_date = y
		vb.Difference = difference
		vb.r_reg = db
		vb.save()

		context = {
			'date': y,
			'name': name,
			'phone': phone,
			'b_name': b_name,
			'b_no' : b_no,
			'f_date': f_date,
			'f_reading': f_reading,
			't_date': t_date,
			't_reading': t_reading,
			'difference': difference,
			'amount': amount,
		}

		pdf = render_to_pdf('invoice.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Invoice_%s.pdf" % ("12341231")
			content = "inline; filename='%s'" % (filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" % (filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")

	return render(request, 'bill_calc.html', {'dc': dc})

def spot_bill(request):
	dc = Buildings.objects.filter(buil_reg=request.session['log'])
	if request.method == 'POST':
		b_no = request.POST.get('building')
		f_reading = request.POST.get('f_reading')
		t_reading = request.POST.get('t_reading')

		amount = 0
		difference = 0
		db = Buildings.objects.get(buil_reg=request.session['log'], Building_number=b_no)
		b_name = db.Building_name
		dd = Readings.objects.filter(r_reg=db.id)

		difference = int(t_reading) - int(f_reading)
		amount = (difference) * 10

		dk = Registration.objects.get(id=request.session['log'])
		name = dk.Name
		phone = dk.Phone
		x = datetime.datetime.now()
		y = x.strftime("%Y-%m-%d")

		context = {
			'date': y,
			'name': name,
			'phone': phone,
			'b_name': b_name,
			'b_no': b_no,
			'f_date': y,
			'f_reading': f_reading,
			't_date': y,
			't_reading': t_reading,
			'difference': difference,
			'amount': amount
		}

		pdf = render_to_pdf('invoice.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Invoice_%s.pdf" % ("12341231")
			content = "inline; filename='%s'" % (filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" % (filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")

	return render(request, 'spot_bill.html', {'dc': dc})


def home(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		comment = request.POST.get('comment')
		t = Feedback()
		t.Name = name
		t.Email = email
		t.Comment = comment
		t.save()
		messages.success(request, 'Saved Your Comment')
		return render(request, 'home.html')
	else:
		return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')

def admin_home(request):
	dc = Registration.objects.filter(Q(User_role="user") | Q(User_role="user_blocked"))
	return render(request, 'admin_home.html',{'dc': dc})

def feedbacks(request):
	dc = Feedback.objects.all()
	return render(request, 'feedbacks.html',{'dc': dc})

def f_delete(request, c):
	Feedback.objects.get(id = c).delete()
	dc = Feedback.objects.all()
	return render(request, 'feedbacks.html',{'dc': dc})

def f_read(request, c):
	db = Feedback.objects.get(id= c)
	db.status = 'Read'
	db.save()
	dc = Feedback.objects.all()
	return render(request, 'feedbacks.html', {'dc': dc})

def user_enable(request, uu):
    d = Registration.objects.get(id = uu)
    d.User_role = 'user'
    d.save()
    dc = Registration.objects.filter(Q(User_role="user") | Q(User_role="user_blocked"))
    return render(request, 'admin_home.html', {'dc': dc})

def user_block(request, uu):
    d = Registration.objects.get(id=uu)
    d.User_role = 'user_blocked'
    d.save()
    dc = Registration.objects.filter(Q(User_role="user") | Q(User_role="user_blocked"))
    return render(request, 'admin_home.html', {'dc': dc})

def add_new_building(request):
	if request.method == 'POST':
		x = datetime.datetime.now()
		y = x.strftime("%Y-%m-%d")
		building_no = request.POST.get('building_no')
		building_name = request.POST.get('building_name')

		db = Buildings.objects.filter(buil_reg=request.session['log'])
		for i in db:
			building_no = int(building_no)
			if i.Building_number == building_no and i.Building_name == building_name:
				messages.success(request, 'Building already exists in your account with same number and name')
				return render(request, 'add_new_building.html')

		state = request.POST.get('state')
		district = request.POST.get('district')
		place = request.POST.get('place')
		pin = request.POST.get('pin')
		phase = request.POST.get('phase')
		purpose = request.POST.get('purpose')
		a = ['Domestic']
		b = ['Manufacturing_Units', 'KWA_Pump_House']
		c = ['IT_Enabled_Services']
		d = ['Pumping/Dewatering']
		e = ['Livestock_Farm']
		f = ['Educational_Institutions', 'Libraries_and_Reading_rooms']
		g = ['KWA_Offices']
		h = ['Railways']
		i = ['Orphanages']
		j = ['Gymnasium', 'Sports_and_Arts_Club', 'Swimming_club', 'Offices_of_Political_Parties']
		k = ['Construction']
		l = ['Private_Hospitals']
		m = ['Commercial']
		n = ['Shops']
		o = ['Cinema_Theatres', 'Circus']
		if purpose in a:
			tarif = 'LT-1A'
		elif purpose in b:
			tarif = 'LT-4A'
		elif purpose in c:
			tarif = 'LT-4B'
		elif purpose in d:
			tarif = 'LT-5A'
		elif purpose in e:
			tarif = 'LT-5B'
		elif purpose in f:
			tarif = 'LT-6A'
		elif purpose in g:
			tarif = 'LT-6B'
		elif purpose in h:
			tarif = 'LT-6C'
		elif purpose in i:
			tarif = 'LT-6D'
		elif purpose in j:
			tarif = 'LT-6E'
		elif purpose in k:
			tarif = 'LT-6F'
		elif purpose in l:
			tarif = 'LT-6G'
		elif purpose in m:
			tarif = 'LT-7A'
		elif purpose in n:
			tarif = 'LT-7B'
		elif purpose in o:
			tarif = 'LT-7C'
		else:
			tarif = 'others'
		pk = Registration.objects.get(id = request.session['log'])
		s = Buildings()
		s.Building_number = building_no
		s.Building_name = building_name
		s.State = state
		s.District = district
		s.Place = place
		s.Pin_code = pin
		s.Purpose = purpose
		s.Phase = phase
		s.Tarif = tarif
		s.Reg_Date = y
		s.buil_reg = pk
		s.save()
		messages.success(request, 'You have successfully registered one building')
		return render(request, 'home.html')

	return render(request, 'add_new_building.html')

def change_pswd(request):
	if request.method == 'POST':
		old_pswrd = request.POST.get('password_old')
		new_pswrd = request.POST.get('password_new')
		con_pswrd = request.POST.get('password_con')

		passwords = make_password(new_pswrd)
		print(passwords)

		dc = Registration.objects.get(id= request.session['log'])
		u = User.objects.get(username= dc.Phone)

		if dc.Password == old_pswrd:
			if new_pswrd == con_pswrd:
				dc.Password = new_pswrd
				dc.save()

				u.password = passwords
				u.save()
		else:
			messages.success(request, 'Old password Not Correct')
			return render(request, 'change_pswd.html')

		messages.success(request, 'Password Successfully Changed')
		return render(request, 'home.html')
	return render(request, 'change_pswd.html')

def edit_reading(request, c):
	do = Readings.objects.get(id =c)
	db = Buildings.objects.get(buil_reg=request.session['log'], Building_number=request.session['buil'])
	if request.method == 'POST':
		#date = request.POST.get('date')
		reading = request.POST.get('reading')
		#dc.Reading_date = date
		do.Reading = reading
		do.save()
		dc = Buildings.objects.filter(buil_reg=request.session['log'])
		messages.success(request, 'You have successfully Edit Reading')
		return render(request, 'show_all_readings.html', {'dc': dc})
	return render(request, 'edit_reading.html', {'do': do, 'db': db})

def delete_reading(request, ed):
	Readings.objects.get(id=ed).delete()
	dc = Buildings.objects.filter(buil_reg=request.session['log'])
	messages.success(request, 'Deleted Successfully You can check')
	return render(request, 'show_all_readings.html', {'dc': dc})

def profile(request):
	dc = Registration.objects.filter(id=request.session['log'])
	db = Buildings.objects.filter(buil_reg=request.session['log'])

	a = []
	b = []
	c = []

	for i in db:
		a.append(i.Building_number)
		b.append(i.Building_name)
		c.append(i.id)

	hh = zip(a, b, c)
	return render(request, 'profile.html', {'dc': dc, 'hh': hh})

def edit_profile(request):
	dc = Registration.objects.get(id=request.session['log'])

	if request.method == 'POST':
		name = request.POST.get('name')
		address = request.POST.get('address')
		email = request.POST.get('e-mail')

		dc.Name = name
		dc.Address = address
		dc.Email = email
		dc.save()

		"""bd = User.objects.get(user = request.session['log'])
		bd.username = phone
		bd.first_name = name
		bd.last_name =address
		bd.email = email
		bd.save()"""

		messages.success(request, 'Profile successfully updated')
		return render(request, 'home.html')
	return render(request, 'edit_profile.html', {'dc': dc})

def save_reading(request):
	dc = Buildings.objects.filter(buil_reg= request.session['log'])
	if request.method == 'POST':
		building_no = request.POST.get('building')
		a = Buildings.objects.get(buil_reg=request.session['log'], Building_number=building_no)
		date = request.POST.get('date')
		db = Readings.objects.filter(r_reg_id = a)
		for i in db:
			if str(i.Reading_date) == str(date):
				messages.success(request, 'Reading already exist on the present date')
				return render(request, 'save_reading.html', {'dc': dc})

		reading = request.POST.get('reading')
		t = Readings()
		t.Reading_date = date
		t.Reading = reading
		t.r_reg = a
		t.save()
		messages.success(request, 'Reading Successfully saved')
		return render(request, 'save_reading.html', {'dc':dc})

	return render(request, 'save_reading.html', {'dc':dc})

def show_all_readings(request):
	dc = Buildings.objects.filter(buil_reg=request.session['log'])
	if request.method == 'POST':
		request.session['buil'] = request.POST.get('building_no')
		dc = Buildings.objects.filter(buil_reg=request.session['log'])
		aa = Buildings.objects.get(buil_reg=request.session['log'], Building_number=request.session['buil'])
		db = Readings.objects.filter(r_reg=aa)
		a = []
		b = []
		c = []
		for i in db:
			a.append(i.Reading_date)
			b.append(i.Reading)
			c.append(i.id)
		hh = zip(a, b, c)
		return render(request, 'show_all_readings.html', {'hh': hh, 'dc': dc, 'aa': aa})

	return render(request, 'show_all_readings.html', {'dc': dc})

def logout(request):
	auth.logout(request)
	return render(request, 'login.html')

def logout_ad(request):
	auth.logout(request)
	return render(request, 'login0.html')

def login0(request):
	if request.method == 'POST':
		phone = request.POST.get('phone')
		password = request.POST.get('password')
		user = auth.authenticate(username= phone, password= password)
		if user is not None:
			b = User.objects.get(username= phone)
			c = Registration.objects.filter(Phone=b)
			for i in c:
				if i.User_role == 'admin':
					request.session['log'] = i.id
					dc = Registration.objects.filter(Q(User_role="user") | Q(User_role="user_blocked"))
					return render(request, 'admin_home.html', {'dc': dc})
			auth.login(request, user)
		else:
			messages.info(request, 'invalid credentials')
			return render(request, 'login0.html')

	return render(request, 'login0.html')

"""
try:
	user = User.objects.get(username=phone)
except:
	messages.info(request, 'invalid credentials')
	return render(request, 'login.html')
c = Registration.objects.get(user=user)

if str(c.Password) == str(password) and str(user) == str(phone):
	cd = Registration.objects.filter(user=user)"""



def login(request):
	if request.method == 'POST':
		phone = request.POST.get('phone')
		password = request.POST.get('password')
		user = auth.authenticate(username=phone, password=password)
		if user is not None:
			b = User.objects.get(username=phone)
			cd = Registration.objects.filter(Phone=b)

			for i in cd:
				if i.User_role == 'user':
					request.session['log'] = i.id
					db = Buildings.objects.filter(buil_reg=request.session['log'])
					dh = []
					for i in db:
						dh.append(i.Building_name)
					if not dh:
						messages.info(request, 'Please add atleast one Building to Continue')
						return render(request, 'new_user_add_building.html')
					else:
						messages.info(request, 'WELCOME TO MYBILLGENERATOR')
						return render(request, 'home.html')
				else:
					messages.info(request, 'Your account Blocked')
					return render(request, 'login.html')
			auth.login(request, user)
		else:
			messages.info(request, 'invalid credentials')
			return render(request, 'login.html')

	return render(request, 'login.html')

def admin_reg(request):
	if request.method == 'POST':
		lk = Registration.objects.all()
		for t in lk:
			if t.User_role == 'admin':
				messages.success(request, 'You are not allowed to be registered as admin')
				return render(request, 'login0.html')
		x = datetime.datetime.now()
		y = x.strftime("%Y-%m-%d")
		Name = request.POST.get('Name')
		Address = request.POST.get('Address')
		Phone = request.POST.get('Phone')
		Email = request.POST.get('Email')
		password = request.POST.get('password1')
		usr = User.objects.create_user(username= Phone, password=password, email=Email, first_name=Name,
									   last_name=Address)
		usr.save()
		t = Registration()
		t.Name = Name
		t.Address = Address
		t.Phone = Phone
		t.Email = Email
		t.Password = password
		t.Registration_date = y
		t.User_role = 'admin'
		t.user = usr
		t.save()
		b = User.objects.get(username=Phone)
		dc = Registration.objects.filter(user=b)
		for i in dc:
			request.session['log'] = i.id
		messages.success(request, 'You have successfully registered as admin, Please Login to continue')
		return render(request, 'login0.html')
	else:
		return render(request, 'admin_reg.html')

def new_user(request):
	if request.method == 'POST':
		x = datetime.datetime.now()
		y = x.strftime("%Y-%m-%d")
		Name = request.POST.get('Name')
		Address = request.POST.get('Address')
		Phone = request.POST.get('Phone')
		Email = request.POST.get('Email')
		password = request.POST.get('password1')
		reg1 = Registration.objects.all()
		for i in reg1:
			if i.Phone == Phone:
				messages.success(request, 'User already exists please login')
				return render(request, 'login.html')
		usr = User.objects.create_user(username= Phone, password=password, email=Email, first_name=Name,
									   last_name=Address)
		usr.save()
		t = Registration()
		t.Name = Name
		t.Address = Address
		t.Phone = Phone
		t.Email = Email
		t.Password = password
		t.Registration_date = y
		t.User_role = 'user'
		t.user = usr
		t.save()
		b = User.objects.get(username=Phone)
		dc = Registration.objects.filter(user=b)
		for i in dc:
			request.session['log'] = i.id
		messages.success(request, 'You have successfully registered, Please Login to continue')
		return render(request, 'login.html')
	else:
		return render(request, 'new_user.html')



def new_user_add_building(request):
	if request.method == 'POST':
		x = datetime.datetime.now()
		y = x.strftime("%Y-%m-%d")
		building_no = request.POST.get('building_no')
		building_name = request.POST.get('building_name')
		state = request.POST.get('state')
		district = request.POST.get('district')
		place = request.POST.get('place')
		pin = request.POST.get('pin')
		purpose = request.POST.get('purpose')
		a = ['Domestic']
		b = ['Manufacturing_Units', 'KWA_Pump_House']
		c = ['IT_Enabled_Services']
		d = ['Pumping/Dewatering']
		e = ['Livestock_Farm']
		f = ['Educational_Institutions', 'Libraries_and_Reading_rooms']
		g = ['KWA_Offices']
		h = ['Railways']
		i = ['Orphanages']
		j = ['Gymnasium', 'Sports_and_Arts_Club', 'Swimming_club', 'Offices_of_Political_Parties']
		k = ['Construction']
		l = ['Private_Hospitals']
		m = ['Commercial']
		n = ['Shops']
		o = ['Cinema_Theatres', 'Circus']
		if purpose in a:
			tarif = 'LT-1A'
		elif purpose in b:
			tarif = 'LT-4A'
		elif purpose in c:
			tarif = 'LT-4B'
		elif purpose in d:
			tarif = 'LT-5A'
		elif purpose in e:
			tarif = 'LT-5B'
		elif purpose in f:
			tarif = 'LT-6A'
		elif purpose in g:
			tarif = 'LT-6B'
		elif purpose in h:
			tarif = 'LT-6C'
		elif purpose in i:
			tarif = 'LT-6D'
		elif purpose in j:
			tarif = 'LT-6E'
		elif purpose in  k:
			tarif = 'LT-6F'
		elif purpose in l:
			tarif = 'LT-6G'
		elif purpose in m:
			tarif = 'LT-7A'
		elif purpose in n:
			tarif = 'LT-7B'
		elif purpose in o:
			tarif = 'LT-7C'
		else:
			tarif = 'others'
		phase = request.POST.get('phase')

		pk = Registration.objects.get(id = request.session['log'])

		i = Buildings()
		i.Building_number = building_no
		i.Building_name = building_name
		i.State = state
		i.District = district
		i.Place = place
		i.Pin_code = pin
		i.Purpose = purpose
		i.Phase = phase
		i.Tarif = tarif
		i.Reg_Date = y
		i.buil_reg = pk
		i.save()
		messages.success(request, 'WELCOME TO MYBILLGENERATOR')
		return render(request, 'home.html')
			#else:
				#messages.success(request, 'Your registred phone number is not matching')
				#return render(request, 'new_user_add_building.html')
	else:
		return render(request, 'new_user_add_building.html')

def edit_building(request, c):
	dc = Buildings.objects.get(id= c)
	if request.method == 'POST':
		x = datetime.datetime.now()
		y = x.strftime("%Y-%m-%d")
		building_no = request.POST.get('building_no')
		building_name = request.POST.get('building_name')

		db = Buildings.objects.filter(buil_reg=request.session['log'])
		for i in db:
			building_no = int(building_no)
			if i.Building_number == building_no and i.Building_name == building_name:
				messages.success(request, 'Building already exists in your account with same number and name')
				return render(request, 'home.html')

		state = request.POST.get('state')
		district = request.POST.get('district')
		place = request.POST.get('place')
		pin = request.POST.get('pin')
		phase = request.POST.get('phase')
		purpose = request.POST.get('purpose')
		a = ['Domestic']
		b = ['Manufacturing_Units', 'KWA_Pump_House']
		c = ['IT_Enabled_Services']
		d = ['Pumping/Dewatering']
		e = ['Livestock_Farm']
		f = ['Educational_Institutions', 'Libraries_and_Reading_rooms']
		g = ['KWA_Offices']
		h = ['Railways']
		i = ['Orphanages']
		j = ['Gymnasium', 'Sports_and_Arts_Club', 'Swimming_club', 'Offices_of_Political_Parties']
		k = ['Construction']
		l = ['Private_Hospitals']
		m = ['Commercial']
		n = ['Shops']
		o = ['Cinema_Theatres', 'Circus']
		if purpose in a:
			tarif = 'LT-1A'
		elif purpose in b:
			tarif = 'LT-4A'
		elif purpose in c:
			tarif = 'LT-4B'
		elif purpose in d:
			tarif = 'LT-5A'
		elif purpose in e:
			tarif = 'LT-5B'
		elif purpose in f:
			tarif = 'LT-6A'
		elif purpose in g:
			tarif = 'LT-6B'
		elif purpose in h:
			tarif = 'LT-6C'
		elif purpose in i:
			tarif = 'LT-6D'
		elif purpose in j:
			tarif = 'LT-6E'
		elif purpose in k:
			tarif = 'LT-6F'
		elif purpose in l:
			tarif = 'LT-6G'
		elif purpose in m:
			tarif = 'LT-7A'
		elif purpose in n:
			tarif = 'LT-7B'
		elif purpose in o:
			tarif = 'LT-7C'
		else:
			tarif = 'others'

		dc.Building_number = building_no
		dc.Building_name = building_name
		dc.State = state
		dc.District = district
		dc.Place = place
		dc.Pin_code = pin
		dc.Purpose = purpose
		dc.Phase = phase
		dc.Tarif = tarif
		dc.Reg_Date = y
		dc.save()
		messages.success(request, 'You have successfully Edit your building')
		return render(request, 'home.html')
	return render(request, 'edit_building.html',{'dc': dc})

def building_delete(request,c):
	Buildings.objects.get(id = c).delete()
	messages.success(request, 'Deleted Successfully')
	return render(request, 'home.html')

def history(request):
	dc = Buildings.objects.filter(buil_reg=request.session['log'])
	if request.method == 'POST':
		request.session['buil'] = request.POST.get('building_no')
		dc = Buildings.objects.filter(buil_reg=request.session['log'])
		aa = Buildings.objects.get(buil_reg=request.session['log'], Building_number=request.session['buil'])
		db = Calculation.objects.filter(r_reg=aa)
		a = []
		b = []
		c = []
		d = []
		e = []
		f = []
		g = []
		h = []
		for i in db:
			a.append(i.id)
			b.append(i.Bill_date)
			c.append(i.Date_from)
			d.append(i.Previous_reading)
			e.append(i.Date_to)
			f.append(i.Current_reading)
			g.append(i.Difference)
			h.append(i.Amount)
		hh = zip(a, b, c, d, e, f, g, h)
		return render(request, 'history.html', {'hh': hh, 'dc': dc, 'aa': aa})

	return render(request, 'history.html', {'dc': dc})

def print_bill(request, a):
	dd = Calculation.objects.get( id=a)
	dk = Registration.objects.get(id=request.session['log'])
	x = datetime.datetime.now()
	y = x.strftime("%Y-%m-%d")

	name = dk.Name
	phone = dk.Phone

	b_name = dd.Building_name
	b_no = dd.Building_number
	f_date = dd.Date_from
	f_reading = dd.Previous_reading
	t_date = dd.Date_to
	t_reading = dd.Current_reading
	amount = dd.Amount
	y = dd.Bill_date
	difference = dd.Difference

	context = {
		'date': y,
		'name': name,
		'phone': phone,
		'b_name': b_name,
		'b_no': b_no,
		'f_date': f_date,
		'f_reading': f_reading,
		't_date': t_date,
		't_reading': t_reading,
		'difference': difference,
		'amount': amount,
	}

	pdf = render_to_pdf('invoice.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" % ("12341231")
		content = "inline; filename='%s'" % (filename)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" % (filename)
		response['Content-Disposition'] = content
		return response
	return HttpResponse("Not found")

def delete_bill(request, a):
	Calculation.objects.get(id= a).delete()
	dc = Buildings.objects.filter(buil_reg=request.session['log'])
	messages.success(request, 'Deleted Successfully, You can check')
	return render(request, 'history.html', {'dc': dc})