"""prediksi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bahanpokok.views import add_admins, add_harga, dashboard, delete_harga, delete_komoditas, get_admins, get_harga, get_komoditas, komoditas, harga, add_komoditas, update_admins, update_harga, update_komoditas, admins, prediksi, prediksi_identifikasi, get_acf_pacf, prediksi_model, get_model, prediksi_hasil, get_hasil_prediksi, laporan, get_laporan, laporan_detail, get_laporan_detail, print_laporan, delete_admins
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard),
    path('dashboard/', dashboard),
    path('komoditas/', komoditas),
    path('harga/', harga),
    path('komoditas/lihat/', get_komoditas, name="get_komoditas"),
    path('komoditas/tambah/', add_komoditas, name="add_komoditas"),
    path('komoditas/ubah/<int:id_kmd>', update_komoditas, name='update_komoditas'),
    path('komoditas/hapus/<int:id_kmd>', delete_komoditas, name='delete_komoditas'),
    path('harga/lihat/', get_harga, name="get_harga"),
    path('harga/tambah/', add_harga, name="add_harga"),
    path('harga/ubah/<int:id_harga>', update_harga, name='update_harga'),
    path('harga/hapus/<int:id_harga>', delete_harga, name='delete_harga'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admins/', admins),
    path('admins/lihat/', get_admins, name="get_admins"),
    path('admins/tambah/', add_admins, name="add_admins"),
    path('admins/ubah/<int:id_admin>', update_admins, name='update_admins'),
    path('admins/hapus/<int:id_admin>', delete_admins, name='delete_admins'),
    path('prediksi/', prediksi),
    path('prediksi/identifikasi/<int:id_kmd>/<str:start>/<str:end>', prediksi_identifikasi),
    path('get_acf_pacf/', get_acf_pacf, name="get_acf_pacf"),
    path('prediksi/model/<int:id_kmd>/<str:start>/<str:end>/<str:p>/<str:d>/<str:q>', prediksi_model),
    path('prediksi/pilihmodel/', get_model, name="get_model"),
    path('prediksi/hasil/<int:id_kmd>/<str:start>/<str:end>/<str:p>/<str:d>/<str:q>/<str:startf>/<str:endf>', prediksi_hasil),
    path('prediksi/gethasil/', get_hasil_prediksi, name="get_hasil_prediksi"),
    path('laporan/', laporan, name="laporan"),
    path('laporan/lihat/', get_laporan, name="get_laporan"),
    path('laporan/detail/<int:id_ramal>', laporan_detail, name="laporan_detail"),
    path('laporan/get_detail/', get_laporan_detail, name="get_laporan_detail"),
    path('laporan/cetak/<int:id_ramal>', print_laporan, name="print_laporan"),
]
