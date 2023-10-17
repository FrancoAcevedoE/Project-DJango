from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_header = 'IX Congreso de Extensión...'
    site_title = 'Congreso Extensión'


admin_site = MyAdminSite(name='congresoextension')
