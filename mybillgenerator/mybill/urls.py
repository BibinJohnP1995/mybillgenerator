from django.urls import path
import mybill.views

urlpatterns=[
	path('', mybill.views.login, name='login'),
	path('home', mybill.views.home, name='home'),
	path('bill_calc', mybill.views.bill_calc, name='bill_calc'),
	path('spot_bill', mybill.views.spot_bill, name='spot_bill'),

	path('add_new_building', mybill.views.add_new_building, name='add_new_building'),

	path('change_pswd', mybill.views.change_pswd, name='change_pswd'),
	path('edit_reading/<c>', mybill.views.edit_reading, name='edit_reading'),
	path('delete_reading/<ed>', mybill.views.delete_reading, name='delete_reading'),

	path('profile', mybill.views.profile, name='profile'),
	path('edit_profile', mybill.views.edit_profile, name='edit_profile'),
	path('save_reading', mybill.views.save_reading, name='save_reading'),
	path('show_all_readings', mybill.views.show_all_readings, name='show_all_readings'),

	path('login', mybill.views.login, name='login'),
	path('about', mybill.views.about, name='about'),
	path('logout', mybill.views.logout, name='logout'),
	path('new_user', mybill.views.new_user, name='new_user'),

	path('new_user_add_building', mybill.views.new_user_add_building, name='new_user_add_building'),
	path('edit_building/<c>', mybill.views.edit_building, name='edit_building'),
	path('building_delete/<c>', mybill.views.building_delete, name='building_delete'),

	path('history', mybill.views.history, name='history'),
    path('delete_bill/<a>', mybill.views.delete_bill, name='delete_bill'),
	path('print_bill/<a>', mybill.views.print_bill, name='print_bill'),

	#admin paths
	path('login0', mybill.views.login0, name='login0'),
	path('logout_ad', mybill.views.logout_ad, name='logout_ad'),
	path('admin_reg', mybill.views.admin_reg, name='admin_reg'),
	path('admin_home', mybill.views.admin_home, name='admin_home'),
	path('user_block/<uu>', mybill.views.user_block, name='user_block'),
	path('user_enable/<uu>', mybill.views.user_enable, name='user_enable'),
	path('feedbacks', mybill.views.feedbacks, name='feedbacks'),
	path('f_delete/<c>', mybill.views.f_delete, name='f_delete'),
	path('f_read/<c>', mybill.views.f_read, name='f_read'),

	]