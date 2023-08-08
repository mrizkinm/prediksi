from django.shortcuts import redirect, render
from bahanpokok.models import Komoditas, Harga, Ramal, DetailRamal
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
import pandas as pd
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import json
import numpy as np
import base64
import io
import math
import  matplotlib.pyplot as plt
plt.switch_backend('agg')
from pylab import *
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime
import itertools
from statsmodels.tools.validation import (
    array_like
)
from scipy import stats
from statsmodels.compat.python import lzip
from statsmodels.graphics import utils
# from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')
from statsmodels.tsa.arima.estimators.innovations import innovations_mle

@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    title = 'Dashboard'
    data = {
        'title': title,
        'user': get_user(request)
    }
    return render(request, 'dashboard.html', data)

@login_required(login_url=settings.LOGIN_URL)
def komoditas(request):
    title = 'Komoditas'
    data = {
        'title': title,
        'user': get_user(request)
    }
    return render(request, 'komoditas.html', data)

@login_required(login_url=settings.LOGIN_URL)
def laporan(request):
    title = 'Laporan Hasil Prediksi'
    data = {
        'title': title,
        'user': get_user(request)
    }
    return render(request, 'laporan.html', data)

@login_required(login_url=settings.LOGIN_URL)
def get_laporan(request):
    ramal = Ramal.objects.select_related('komoditas').values('id', 'date', 'komoditas__nama', 'model', 'start_train', 'end_train', 'start_ramal', 'end_ramal', 'mape_ramal', 'rmse_ramal')
    data = {
        'success': True,
        'data' : list(ramal)
    }
    return JsonResponse(data, safe=False)

@login_required(login_url=settings.LOGIN_URL)
def get_komoditas(request):
    komoditas = Komoditas.objects.all().values()
    data = {
        'success': True,
        'data' : list(komoditas)
    }
    return JsonResponse(data, safe=False)

@login_required(login_url=settings.LOGIN_URL)
def add_komoditas(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        komoditas = Komoditas(nama=nama)
        komoditas.save()
        msg = "Data berhasil ditambah"
        messages.success(request, msg)
        return redirect('/komoditas')
    else:
        title = 'Tambah Komoditas'
        data = {
            'title': title,
            'user': get_user(request)
        }
        return render(request, 'add_komoditas.html', data)

@login_required(login_url=settings.LOGIN_URL)
def update_komoditas(request, id_kmd):
    komoditas = Komoditas.objects.get(id=id_kmd)
    if request.method == 'POST':
        komoditas.nama = request.POST['nama']
        komoditas.save()
        msg = "Data berhasil diubah"
        messages.success(request, msg)
        return redirect('/komoditas')
    else:
        title = 'Ubah Komoditas'
        data = {
            'title': title,
            'komoditas': komoditas,
            'user': get_user(request)
        }
        return render(request, 'update_komoditas.html', data)

@login_required(login_url=settings.LOGIN_URL)
def delete_komoditas(request, id_kmd):
    komoditas = Komoditas.objects.filter(id=id_kmd)
    komoditas.delete()
    msg = "Data berhasil dihapus"
    messages.success(request, msg)
    return redirect('/komoditas')

@login_required(login_url=settings.LOGIN_URL)
def harga(request):
    title = 'Harga'
    komoditas = Komoditas.objects.all()
    data = {
        'title': title,
        'komoditas': komoditas,
        'user': get_user(request)
    }
    return render(request, 'harga.html', data)

@login_required(login_url=settings.LOGIN_URL)
def get_harga(request):
    start = request.POST['start']
    end = request.POST['end']
    komoditas_id = request.POST['komoditas_id']
    if komoditas_id:
        harga = Harga.objects.filter(date__range=[start, end],komoditas_id=komoditas_id).select_related('komoditas').values('id', 'date', 'komoditas__nama', 'harga')
    else:
        harga = Harga.objects.filter(date__range=[start, end]).select_related('komoditas').values('id', 'date', 'komoditas__nama', 'harga')
    data = {
        'success': True,
        'data' : list(harga)
    }
    return JsonResponse(data, safe=False)

@login_required(login_url=settings.LOGIN_URL)
def add_harga(request):
    if request.method == 'POST':
        date = request.POST['date']
        komoditas_id = request.POST['komoditas_id']
        harga = request.POST['harga']
        tharga = Harga(date=date, komoditas_id=komoditas_id, harga=harga)
        tharga.save()
        msg = "Data berhasil ditambah"
        messages.success(request, msg)
        return redirect('/harga')
    else:
        title = 'Tambah Harga Komoditas'
        komoditas = Komoditas.objects.all()
        data = {
            'title': title,
            'komoditas': komoditas,
            'user': get_user(request)
        }
        return render(request, 'add_harga.html', data)

@login_required(login_url=settings.LOGIN_URL)
def update_harga(request, id_harga):
    tharga = Harga.objects.get(id=id_harga)
    if request.method == 'POST':
        # tharga.date = request.POST['date']
        # tharga.komoditas_id = request.POST['komoditas_id']
        tharga.harga = request.POST['harga']
        tharga.save()
        msg = "Data berhasil diubah"
        messages.success(request, msg)
        return redirect('/harga')
    else:
        title = 'Ubah Harga Komoditas'
        komoditas = Komoditas.objects.all()
        data = {
            'title': title,
            'harga': tharga,
            'komoditas': komoditas,
            'user': get_user(request)
        }
        return render(request, 'update_harga.html', data)

@login_required(login_url=settings.LOGIN_URL)
def delete_harga(request, id_harga):
    tharga = Harga.objects.filter(id=id_harga)
    tharga.delete()
    msg = "Data berhasil dihapus"
    messages.success(request, msg)
    return redirect('/harga')

def get_user(request):
    user = User.objects.get(username=request.user)
    return user

@login_required(login_url=settings.LOGIN_URL)
def admins(request):
    title = 'Admin'
    data = {
        'title': title,
        'user': get_user(request)
    }
    return render(request, 'admin.html', data)

@login_required(login_url=settings.LOGIN_URL)
def get_admins(request):
    user = User.objects.all().values()
    data = {
        'success': True,
        'data' : list(user)
    }
    return JsonResponse(data, safe=False)

@login_required(login_url=settings.LOGIN_URL)
def add_admins(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        is_superuser = 0
        is_staff = 0
        password = make_password(request.POST['password'])
        user = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email, is_superuser=is_superuser, is_staff=is_staff)
        user.save()
        msg = "Data berhasil ditambah"
        messages.success(request, msg)
        return redirect('/admins')
        # form = UserCreationForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     msg = "Data berhasil ditambah"
        #     messages.success(request, msg)
        #     return redirect('/admins')
        # else:
        #     messages.error(request, 'error')
        #     return redirect('/admins')
    else:
        title = 'Tambah Admin'
        data = {
            'title': title,
            'form': UserCreationForm(),
            'user': get_user(request)
        }
        return render(request, 'add_admins.html', data)

@login_required(login_url=settings.LOGIN_URL)
def update_admins(request, id_admin):
    user = User.objects.get(id=id_admin)
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        msg = "Data berhasil diubah"
        messages.success(request, msg)
        return redirect('/admins')
    else:
        title = 'Ubah Data Admin'
        data = {
            'title': title,
            'admin': user,
            'user': get_user(request)
        }
        return render(request, 'update_admins.html', data)

@login_required(login_url=settings.LOGIN_URL)
def delete_admins(request, id_admin):
    tadmin = User.objects.filter(id=id_admin)
    tadmin.delete()
    msg = "Data berhasil dihapus"
    messages.success(request, msg)
    return redirect('/admins')

@login_required(login_url=settings.LOGIN_URL)
def prediksi(request):
    title = 'Prediksi'
    komoditas = Komoditas.objects.all()
    data = {
        'title': title,
        'komoditas': komoditas,
        'user': get_user(request)
    }
    return render(request, 'prediksi.html', data)

@login_required(login_url=settings.LOGIN_URL)
def prediksi_identifikasi(request, id_kmd, start, end):
    title = 'Prediksi Harga Komoditas'
    komoditas = Komoditas.objects.get(id=id_kmd)
    data = {
        'title': title,
        'id_kmd': id_kmd,
        'komoditas': komoditas.nama,
        'start': start,
        'end': end,
        'user': get_user(request)
    }
    return render(request, 'prediksi_identifikasi.html', data)

@login_required(login_url=settings.LOGIN_URL)
def prediksi_model(request, id_kmd, start, end, p, d, q):
    title = 'Hasil Prediksi Harga Komoditas'
    komoditas = Komoditas.objects.get(id=id_kmd)
    data = {
        'title': title,
        'id_kmd': id_kmd,
        'komoditas': komoditas.nama,
        'start': start,
        'end': end,
        'p': p,
        'd': d,
        'q': q,
        'user': get_user(request)
    }
    return render(request, 'prediksi_model.html', data)

def mape(actual, pred):
    actual, pred = np.array(actual), np.array(pred)
    return np.mean(np.abs((actual - pred) / actual)) * 100

def rmse(actual, pred):
    mse = np.square(np.subtract(actual,pred)).mean() 
    return math.sqrt(mse)

@login_required(login_url=settings.LOGIN_URL)
def get_model(request):
    start = request.POST['start']
    end = request.POST['end']
    komoditas_id = request.POST['komoditas_id']
    p = int(request.POST['p'])
    d = int(request.POST['d'])
    q = int(request.POST['q'])
    if komoditas_id:
        harga = Harga.objects.filter(date__range=[start, end],komoditas_id=komoditas_id).select_related('komoditas').values('date', 'komoditas__nama', 'harga')
    else:
        harga = Harga.objects.filter(date__range=[start, end]).select_related('komoditas').values('date', 'komoditas__nama', 'harga')
    data_asli = list(harga)
    npdata = np.array(data_asli)
    npdatanorm = pd.json_normalize(npdata)
    df = pd.DataFrame(npdatanorm, columns=['date', 'komoditas__nama', 'harga'])
    df = df.drop('komoditas__nama', axis=1)
    df = df.set_index('date')
    actualdatalist = list()
    for x in data_asli:
        actualdatalist.append(x['harga'])
    start_raw = datetime.strptime(start, '%Y-%m-%d')
    end_raw = datetime.strptime(end, '%Y-%m-%d')
    daterange = pd.date_range(start_raw, end_raw)
    pastdatelist = list()
    for single_date in daterange:
       pastdatelist.append(single_date.strftime("%Y-%m-%d"))

    # clcpast = calculatePast(df, p, d, q)
    # datapast = {'date': pastdatelist, 'harga': clcpast['data']}
    # dfpast = pd.DataFrame(datapast)
    # print(dfpast.values.tolist())
    
    ps=range(0,p+1)
    ds=[d]
    qs=range(0,q+1)
    pdq_comb = list(itertools.product(ps,ds,qs))

    if d < 1:
        pdq_comb.pop(0)
    if len(pdq_comb) > 3:
        pdq_comb = pdq_comb[-3:]
    pdq_comb.reverse()

    df = [x for x in df['harga']]
    model_list = list()
    for pdq in pdq_comb:
        # model = ARIMA(df, order=pdq).fit()
        # fitted = list(model.fittedvalues)
        fitted_value = fitted(df, pdq[0], pdq[1], pdq[2], False)
        fittedv = fitted_value['prediction']
        mape_val = mape(df, fittedv)
        rmse_val = rmse(df, fittedv)
        # print('df')
        # print(df)
        # print('fitted')
        # print(fitted)
        # print('mape')
        # print(mape_val)
        # print('mape2')
        # print(mean_absolute_percentage_error(df, fitted))
        # print('rmse')
        # print(rmse_val)
        # print('rmse2')
        # print(np.sqrt(mean_squared_error(df, fitted)))
        # print('')
        arr_model = {
            'modelpdq': pdq,
            'fitted': fittedv,
            'mape': mape_val,
            'rmse': rmse_val,
            'coef': fitted_value['params']
        }
        model_list.append(arr_model)
    data = {
        'success': True,
        'pastdatelist': pastdatelist,
        'actual': {
            'name': 'Data Aktual',
            'data': actualdatalist,
        },
        'model': model_list
    }
    return JsonResponse(data, safe=False)

@login_required(login_url=settings.LOGIN_URL)
def prediksi_hasil(request, id_kmd, start, end, p, d, q, startf, endf):
    title = 'Hasil Prediksi Harga Komoditas'
    komoditas = Komoditas.objects.get(id=id_kmd)
    data = {
        'title': title,
        'id_kmd': id_kmd,
        'komoditas': komoditas.nama,
        'start': start,
        'end': end,
        'p': p,
        'd': d,
        'q': q,
        'startf': startf,
        'endf': endf,
        'user': get_user(request)
    }
    return render(request, 'prediksi_hasil.html', data)

# @login_required(login_url=settings.LOGIN_URL)
# def get_hasil_prediksi(request):
#     start = request.POST['start']
#     end = request.POST['end']
#     komoditas_id = request.POST['komoditas_id']
#     p = int(request.POST['p'])
#     d = int(request.POST['d'])
#     q = int(request.POST['q'])
#     startf = request.POST['startf']
#     endf = request.POST['endf']
#     if komoditas_id:
#         harga = Harga.objects.filter(date__range=[start, end],komoditas_id=komoditas_id).select_related('komoditas').values('date', 'komoditas__nama', 'harga')
#     else:
#         harga = Harga.objects.filter(date__range=[start, end]).select_related('komoditas').values('date', 'komoditas__nama', 'harga')
#     data_asli = list(harga)
#     npdata = np.array(data_asli)
#     npdatanorm = pd.json_normalize(npdata)
#     df = pd.DataFrame(npdatanorm, columns=['date', 'komoditas__nama', 'harga'])
#     df = df.drop('komoditas__nama', axis=1)
#     df = df.set_index('date')
#     actualdatalist = list()
#     for x in data_asli:
#         actualdatalist.append(x['harga'])

#     start_raw = datetime.strptime(start, '%Y-%m-%d')
#     end_raw = datetime.strptime(end, '%Y-%m-%d')
#     daterange = pd.date_range(start_raw, end_raw)
#     pastdatelist = list()
#     for single_date in daterange:
#        pastdatelist.append(single_date.strftime("%Y-%m-%d"))

#     startf_raw = datetime.strptime(startf, '%Y-%m-%d')
#     endf_raw = datetime.strptime(endf, '%Y-%m-%d')
#     daterangef = pd.date_range(startf_raw, endf_raw)
#     datelist = list()
#     for single_date in daterangef:
#        datelist.append(single_date.strftime("%Y-%m-%d"))

#     df = [x for x in df['harga']]
#     # model = ARIMA(df, order=(p, d, q)).fit()
#     # pred = list(model.forecast(len(datelist)))
#     fitted_value = fitted(df, p, d, q)
#     forecast_value = forecast(df, p, d, q, len(datelist), fitted_value['residual'])
#     pred = forecast_value['prediction']
#     # alldata = actualdatalist+pred
#     datefull = pastdatelist+datelist

#     banding_aktual_raw = Harga.objects.filter(date__range=[startf, endf],komoditas_id=komoditas_id).select_related('komoditas').values('date', 'komoditas__nama', 'harga')
#     banding_aktual = list(banding_aktual_raw)
#     # print(len(banding_aktual))
#     actualforecast = list()
#     for x in banding_aktual:
#         actualforecast.append(x['harga'])

#     len_actual_pred = len(actualforecast)
#     len_pred = len(pred)
#     selisih = len_pred-len_actual_pred
#     if selisih > 0:
#         # print('selisih')
#         # print(selisih)
#         actualforecast2 = actualforecast[:len_actual_pred]
#         for x in range(0, selisih):
#            actualforecast2.append(None)
#         pred2 = pred[selisih:]

#         # print('pred2')
#         # print(pred2)
#         # print(len(pred2))
#         # print('')
#         # print('acfo')
#         # print(actualforecast)
#         # print(len(actualforecast))
#         # print('')
#         # print('acfo2')
#         # print(actualforecast2)
#         # print(len(actualforecast2))
#         # print('')
#         # print('pred')
#         # print(pred)
#         # print(len(pred))

#         if len_actual_pred > 0:
#             mape_ramal = mape(actualforecast, pred2)
#             rmse_ramal = rmse(actualforecast, pred2)
#         else:
#             mape_ramal = None
#             rmse_ramal = None
#     else:
#         actualforecast2 = actualforecast[:len_actual_pred]
#         mape_ramal = mape(actualforecast, pred)
#         rmse_ramal = rmse(actualforecast, pred)
#         # print('acfo')
#         # print(actualforecast)
#         # print(len(actualforecast))
#         # print('')
#         # print('acfo2')
#         # print(actualforecast2)
#         # print(len(actualforecast2))
#         # print('')
#         # print('pred')
#         # print(pred)
#         # print(len(pred))
#         # print('')
#         # print('mape')
#         # print(mape_ramal)
#         # print('')
#         # print('rmse')
#         # print(rmse_ramal)
#     # model = request.POST['p']+','+request.POST['d']+','+request.POST['q']
#     # ramal = Ramal.objects.filter(model=model, start_train=start, end_train=end, start_ramal=startf, end_ramal=endf, komoditas_id=komoditas_id, mape_ramal=mape_ramal, rmse_ramal=rmse_ramal)
#     # if len(ramal) < 1:
#     #     tramal = Ramal(model=model, start_train=start, end_train=end, start_ramal=startf, end_ramal=endf, komoditas_id=komoditas_id, mape_ramal=mape_ramal, rmse_ramal=rmse_ramal)
#     #     save = tramal.save()
#     #     for i in range(0, len(datelist)):
#     #         tdramal = DetailRamal(ramal_id=save.id, date=datelist[i], harga_aktual=actualforecast2[i], harga_ramal=pred[i])
#     #         tdramal.save()
#     data = {
#         'success': True,
#         'datefull': datefull,
#         'datepast': pastdatelist,
#         'datefuture': datelist,
#         'hargapast': actualdatalist,
#         'hargafuture': pred,
#         'hargafutureaktual': actualforecast2,
#         'mape_ramal': mape_ramal,
#         'rmse_ramal': rmse_ramal,
#         'coef': fitted_value['params']
#     }
#     return JsonResponse(data, safe=False)

@login_required(login_url=settings.LOGIN_URL)
def get_hasil_prediksi(request):
    start = request.POST['start']
    end = request.POST['end']
    komoditas_id = request.POST['komoditas_id']
    p = int(request.POST['p'])
    d = int(request.POST['d'])
    q = int(request.POST['q'])
    startf = request.POST['startf']
    endf = request.POST['endf']
    if komoditas_id:
        harga = Harga.objects.filter(date__range=[start, end],komoditas_id=komoditas_id).select_related('komoditas').values('date', 'komoditas__nama', 'harga')
    else:
        harga = Harga.objects.filter(date__range=[start, end]).select_related('komoditas').values('date', 'komoditas__nama', 'harga')
    data_asli = list(harga)
    npdata = np.array(data_asli)
    npdatanorm = pd.json_normalize(npdata)
    df = pd.DataFrame(npdatanorm, columns=['date', 'komoditas__nama', 'harga'])
    df = df.drop('komoditas__nama', axis=1)
    df = df.set_index('date')
    actualdatalist = list()
    for x in data_asli:
        actualdatalist.append(x['harga'])

    start_raw = datetime.strptime(start, '%Y-%m-%d')
    end_raw = datetime.strptime(end, '%Y-%m-%d')
    daterange = pd.date_range(start_raw, end_raw)
    pastdatelist = list()
    for single_date in daterange:
       pastdatelist.append(single_date.strftime("%Y-%m-%d"))

    startf_raw = datetime.strptime(startf, '%Y-%m-%d')
    endf_raw = datetime.strptime(endf, '%Y-%m-%d')
    daterangef = pd.date_range(startf_raw, endf_raw)
    datelist = list()
    for single_date in daterangef:
       datelist.append(single_date.strftime("%Y-%m-%d"))

    df = [x for x in df['harga']]
    fitted_value = fitted(df, p, d, q, False)
    banding_aktual_raw = Harga.objects.filter(date__range=[start, endf],komoditas_id=komoditas_id).select_related('komoditas').values('date', 'komoditas__nama', 'harga')
    banding_aktual = list(banding_aktual_raw)
    # print(len(banding_aktual))
    actualforecastall = list()
    for x in banding_aktual:
        actualforecastall.append(x['harga'])
    # forecastv = forecast(df, p, d, q, len(datelist), fitted_value['residual'], fitted_value['params'])
    # difflast = (df[-1])-(actualforecast[0])
    forecast_value = fitted(actualforecastall, p, d, q, fitted_value['params'])
    forecast_pred = forecast_value['prediction'][len(pastdatelist):]
    print(len(forecast_pred))
    print(forecast_pred)
    pred = forecast_pred
    datefull = pastdatelist+datelist
    actualforecast = actualforecastall[len(pastdatelist):]
    len_actual_pred = len(actualforecast)
    len_pred = len(pred)
    selisih = len_pred-len_actual_pred
    if selisih > 0:
        # print('selisih')
        # print(selisih)
        actualforecast2 = actualforecast[:len_actual_pred]
        for x in range(0, selisih):
           actualforecast2.append(None)
        pred2 = pred[selisih:]

        # print('pred2')
        # print(pred2)
        # print(len(pred2))
        # print('')
        # print('acfo')
        # print(actualforecast)
        # print(len(actualforecast))
        # print('')
        # print('acfo2')
        # print(actualforecast2)
        # print(len(actualforecast2))
        # print('')
        # print('pred')
        # print(pred)
        # print(len(pred))

        if len_actual_pred > 0:
            mape_ramal = mape(actualforecast, pred2)
            rmse_ramal = rmse(actualforecast, pred2)
        else:
            mape_ramal = None
            rmse_ramal = None
    else:
        actualforecast2 = actualforecast[:len_actual_pred]
        mape_ramal = mape(actualforecast, pred)
        rmse_ramal = rmse(actualforecast, pred)
        # print('acfo')
        # print(actualforecast)
        # print(len(actualforecast))
        # print('')
        # print('acfo2')
        # print(actualforecast2)
        # print(len(actualforecast2))
        # print('')
        # print('pred')
        # print(pred)
        # print(len(pred))
        # print('')
        # print('mape')
        # print(mape_ramal)
        # print('')
        # print('rmse')
        # print(rmse_ramal)
    # model = request.POST['p']+','+request.POST['d']+','+request.POST['q']
    # ramal = Ramal.objects.filter(model=model, start_train=start, end_train=end, start_ramal=startf, end_ramal=endf, komoditas_id=komoditas_id, mape_ramal=mape_ramal, rmse_ramal=rmse_ramal)
    # if len(ramal) < 1:
    #     tramal = Ramal(model=model, start_train=start, end_train=end, start_ramal=startf, end_ramal=endf, komoditas_id=komoditas_id, mape_ramal=mape_ramal, rmse_ramal=rmse_ramal)
    #     save = tramal.save()
    #     for i in range(0, len(datelist)):
    #         tdramal = DetailRamal(ramal_id=save.id, date=datelist[i], harga_aktual=actualforecast2[i], harga_ramal=pred[i])
    #         tdramal.save()
    data = {
        'success': True,
        'datefull': datefull,
        'datepast': pastdatelist,
        'datefuture': datelist,
        'hargapast': actualdatalist,
        'hargafuture': pred,
        'hargafutureaktual': actualforecast2,
        'mape_ramal': mape_ramal,
        'rmse_ramal': rmse_ramal,
        'coef': fitted_value['params']
    }
    return JsonResponse(data, safe=False)

def differencing(data, interval, number):
	# global diffData
	newNumber = number - 1
	dataDiff = list()
	for i in range(interval, len(data)):
		harga = data[i] - data[i-interval]
		dataDiff.append(harga)
	diffData = dataDiff
	if newNumber > 0:
		differencing(dataDiff, interval, newNumber)
	else:
		return diffData

def predict_ar(coef, history):
	yhat = 0.0
	for i in range(1, len(coef)+1):
		yhat += coef[i-1] * history[-i]
	return yhat

def predict_ma(coef, history):
	yhat = 0.0
	for i in range(1, len(coef)+1):
		yhat += coef[i-1] * history[-i]
	return yhat

def fitted(history, p, d, q, params):
	# model = ARIMA(history, order=(p,d,q))
	# model_fit = model.fit()
	# ar_coef = model_fit.arparams
	# ma_coef = model_fit.maparams
	if params:
		ar_coef = params['ar_coef']
		ma_coef = params['ma_coef']
	else:
		coef = innovations_mle(history, order=(p,d,q))
		ar_coef = list(coef[0].ar_params)
		ma_coef = list(coef[0].ma_params)
	print('ar_coef')
	print(ar_coef)
	print(ma_coef)
	mean = np.mean(history)
	prediction = list()
	residual = list()
	residu = [0] * q
	histo = [0] * p
	if d > 0:
		histodiff = [0] * p
		diffhist = [0] * d
		diffData = differencing(history, 1, d)
	for i in range(len(history)):
		cons = 0
		ar = 0
		ma = 0
		if d > 0:
			cons = diffhist[i]
			if i == 0:
				for h in range(len(diffhist)):
					diffData.insert(0, history[h])
		if p > 0:
			if d > 0:
				his = histodiff
			else:
				his = histo
				cons = mean*(1-np.sum(ar_coef))
				if i == 0:
					cons = cons+mean
			ar = predict_ar(ar_coef, his)
		if q > 0:
			if p < 1 and d < 1:
				cons = mean
			ma = predict_ma(ma_coef, residu)
		arima_res = cons+ar+ma
		res = history[i]-arima_res
		prediction.append(arima_res)
		residual.append(res)
		histo.append(history[i])
		residu.append(res)
		if d > 0:
			histodiff.append(diffData[i])
			diffhist.append(history[i])
    
	params = {
		'ar_coef': ar_coef,
		'ma_coef': ma_coef,
	}
	result = {
		'prediction': prediction,
		'residual': residual,
        'params': params
	}
	return result

def forecast(history, p, d, q, len_day, residual, params):
	# model = ARIMA(history, order=(p,d,q))
	# model_fit = model.fit()
	# ar_coef = model_fit.arparams
	# ma_coef = model_fit.maparams
	if params:
		ar_coef = params['ar_coef']
		ma_coef = params['ma_coef']
	else:
		coef = innovations_mle(history, order=(p,d,q))
		ar_coef = list(coef[0].ar_params)
		ma_coef = list(coef[0].ma_params)
	mean = np.mean(history)
	prediction = list()
	residu = list()
	for i in range(len_day):
		cons = 0
		ar = 0
		ma = 0
		if d > 0:
			cons = history[-1]
			diffData = differencing(history, 1, d)
		if p > 0:
			if d > 0:
				his = diffData
			else:
				his = history
				cons = mean*(1-np.sum(ar_coef))
			ar = predict_ar(ar_coef, his)
		if q > 0:
			if p < 1 and d < 1:
				cons = mean
			ma = predict_ma(ma_coef, residual)
		arima_res = cons+ar+ma
		history.append(arima_res)
		prediction.append(arima_res)
		residual.append(0)
		residu.append(0)
                
	params = {
		'ar_coef': ar_coef,
		'ma_coef': ma_coef,
	}
	result = {
		'prediction': prediction,
		'residual': residual,
		'params': params
	}
	return result

# def forecast(history, p, d, q, len_day, residual):
# 	# model = ARIMA(history, order=(p,d,q))
# 	# model_fit = model.fit()
# 	# ar_coef = model_fit.arparams
# 	# ma_coef = model_fit.maparams
# 	coef = innovations_mle(history, order=(p,d,q))
# 	ar_coef = list(coef[0].ar_params)
# 	ma_coef = list(coef[0].ma_params)
# 	mean = np.mean(history)
# 	prediction = list()
# 	residu = list()
# 	for i in range(len_day):
# 		cons = 0
# 		ar = 0
# 		ma = 0
# 		if d > 0:
# 			cons = history[-1]
# 			diffData = differencing(history, 1, d)
# 		if p > 0:
# 			if d > 0:
# 				his = diffData
# 			else:
# 				his = history
# 				cons = mean*(1-np.sum(ar_coef))
# 			ar = predict_ar(ar_coef, his)
# 		if q > 0:
# 			if p < 1 and d < 1:
# 				cons = mean
# 			ma = predict_ma(ma_coef, residual)
# 		arima_res = cons+ar+ma
# 		history.append(arima_res)
# 		prediction.append(arima_res)
# 		residual.append(0)
# 		residu.append(0)
                
# 	params = {
# 		'ar_coef': ar_coef,
# 		'ma_coef': ma_coef,
# 	}
# 	result = {
# 		'prediction': prediction,
# 		'residual': residual,
# 		'params': params
# 	}
# 	return result

@login_required(login_url=settings.LOGIN_URL)
def laporan_detail(request, id_ramal):
    title = 'Detail Laporan Hasil Prediksi'
    ramal = Ramal.objects.get(id=id_ramal)
    komoditas = Komoditas.objects.get(id=ramal.komoditas_id)
    data = {
        'title': title,
        'id_ramal': id_ramal,
        'startf': ramal.start_ramal,
        'endf': ramal.end_ramal,
        'komoditas': komoditas.nama,
        'model': ramal.model,
        'user': get_user(request)
    }
    return render(request, 'laporan_detail.html', data)

@login_required(login_url=settings.LOGIN_URL)
def get_laporan_detail(request):
    id_ramal = request.POST['id_ramal']
    ramal = Ramal.objects.get(id=id_ramal)
    harga = Harga.objects.filter(date__range=[ramal.start_train, ramal.end_train],komoditas_id=ramal.komoditas_id).select_related('komoditas').values('id', 'date', 'komoditas__nama', 'harga')
    hargap = list()
    for i in range(0, len(harga)):
        hargap.append(harga[i]['harga'])

    dramal = DetailRamal.objects.filter(ramal_id=id_ramal).values('id', 'date', 'harga_aktual', 'harga_ramal', 'ramal_id')
    dramal = list(dramal)
    hargafak = list()
    for i in range(0, len(dramal)):
        hargafak.append(dramal[i]['harga_aktual'])
    hargaf = list()
    for i in range(0, len(dramal)):
        hargaf.append(dramal[i]['harga_ramal'])

    start_raw = datetime.strptime(str(ramal.start_train), '%Y-%m-%d')
    end_raw = datetime.strptime(str(ramal.end_train), '%Y-%m-%d')
    daterange = pd.date_range(start_raw, end_raw)
    pastdatelist = list()
    for single_date in daterange:
       pastdatelist.append(single_date.strftime("%Y-%m-%d"))

    startf_raw = datetime.strptime(str(ramal.start_ramal), '%Y-%m-%d')
    endf_raw = datetime.strptime(str(ramal.end_ramal), '%Y-%m-%d')
    daterangef = pd.date_range(startf_raw, endf_raw)
    datelist = list()
    for single_date in daterangef:
       datelist.append(single_date.strftime("%Y-%m-%d"))
    datefull = pastdatelist+datelist
    data = {
        'success': True,
        'datefull': datefull,
        'datepast': pastdatelist,
        'datefuture': datelist,
        'hargapast': hargap,
        'hargafuture': hargaf,
        'hargafutureaktual': hargafak,
        'mape_ramal': ramal.mape_ramal,
        'rmse_ramal': ramal.rmse_ramal
    }
    return JsonResponse(data, safe=False)

@login_required(login_url=settings.LOGIN_URL)
def print_laporan(request, id_ramal):
    title = 'Cetak Laporan'
    ramal = Ramal.objects.get(id=id_ramal)
    komoditas = Komoditas.objects.get(id=ramal.komoditas_id)
    detailramal = DetailRamal.objects.filter(ramal_id=id_ramal).values('id', 'date', 'harga_aktual', 'harga_ramal')
    data = {
        'title': title,
        'id_ramal': id_ramal,
        'startf': ramal.start_ramal,
        'endf': ramal.end_ramal,
        'komoditas': komoditas.nama,
        'model': ramal.model,
        'detail': list(detailramal),
        'user': get_user(request)
    }
    return render(request, 'print_laporan.html', data)

@login_required(login_url=settings.LOGIN_URL)
def get_acf_pacf(request):
    timeseries = request.POST['timeseries']
    data = json.loads(timeseries)
    npdata = np.array(data)
    npdatanorm = pd.json_normalize(npdata)
    df = pd.DataFrame(npdatanorm, columns=['date', 'name', 'harga'])
    df = df.drop('name', axis=1)
    df = df.set_index('date')
    acf = get_acf(df)
    pacf = get_pacf(df)
    data = {
        'acf': acf['img'],
        'pacf': pacf['img']
    }
    return JsonResponse(data, safe=False)

def get_acf(df):
    dflen = len(df)
    if dflen > 62:
        plot_acf(df, lags=30)
    else:
        lags = int((dflen/2)-2)
        plot_acf(df, lags=lags)
    # plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic_acf = base64.b64encode(image_png)
    graphic_acf = graphic_acf.decode('utf-8')
    data = {
        'img': graphic_acf
    }
    return data

def get_pacf(df):
    dflen = len(df)
    print(dflen)
    if dflen > 62:
        plot_pacf(df, method="ldb", lags=30)
    else:
        lags = int((dflen/2)-2)
        plot_pacf(df, method="ldb", lags=lags)
    # plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic_pacf = base64.b64encode(image_png)
    graphic_pacf = graphic_pacf.decode('utf-8')
    data = {
        'img': graphic_pacf
    }
    return data

def acf(
    x,
    adjusted=False,
    nlags=None,
    qstat=False,
    fft=False,
    alpha=None,
    bartlett_confint=True,
    missing="none",
):
    x = array_like(x, "x")
    # TODO: should this shrink for missing="drop" and NaNs in x?
    nobs = x.shape[0]
    if nlags is None:
        nlags = min(int(10 * np.log10(nobs)), nobs - 1)

    avf = acovf(x, adjusted=adjusted, demean=True, fft=fft, missing=missing)
    acf = avf[: nlags + 1] / avf[0]
    if not (qstat or alpha):
        return acf
    if alpha is not None:
        if bartlett_confint:
            varacf = np.ones_like(acf) / nobs
            varacf[0] = 0
            varacf[1] = 1.0 / nobs
            varacf[2:] *= 1 + 2 * np.cumsum(acf[1:-1] ** 2)
        else:
            varacf = 1.0 / len(x)
        interval = stats.norm.ppf(1 - alpha / 2.0) * np.sqrt(varacf)
        # print('interval')
        # print(interval)
        confint = np.array(lzip(acf - interval, acf + interval))
        # print(acf)
        if not qstat:
            return acf, confint

def pacf(x, nlags=None, alpha=None):
    x = array_like(x, "x", maxdim=2)

    nobs = x.shape[0]
    if nlags is None:
        nlags = min(int(10 * np.log10(nobs)), nobs // 2 - 1)
    if nlags >= x.shape[0] // 2:
        raise ValueError(
            "Can only compute partial correlations for lags up to 50% of the "
            f"sample size. The requested nlags {nlags} must be < "
            f"{x.shape[0] // 2}."
        )

    acv = acovf(x, adjusted=False, fft=False)
    ld_ = levinson_durbin(acv, nlags=nlags, isacov=True)
    ret = ld_[2]
    # print(ret)
    if alpha is not None:
        varacf = 1.0 / len(x)  # for all lags >=1
        interval = stats.norm.ppf(1.0 - alpha / 2.0) * np.sqrt(varacf)
        confint = np.array(lzip(ret - interval, ret + interval))
        confint[0] = ret[0]  # fix confidence interval for lag 0 to varpacf=0
        return ret, confint
    else:
        return ret

def levinson_durbin(s, nlags=10, isacov=False):
    order = nlags

    if isacov:
        sxx_m = s
    else:
        sxx_m = acovf(s, fft=False)[: order + 1]  # not tested

    phi = np.zeros((order + 1, order + 1), "d")
    sig = np.zeros(order + 1)
    # initial points for the recursion
    phi[1, 1] = sxx_m[1] / sxx_m[0]
    sig[1] = sxx_m[0] - phi[1, 1] * sxx_m[1]
    for k in range(2, order + 1):
        phi[k, k] = (
            sxx_m[k] - np.dot(phi[1:k, k - 1], sxx_m[1:k][::-1])
        ) / sig[k - 1]
        for j in range(1, k):
            phi[j, k] = phi[j, k - 1] - phi[k, k] * phi[k - j, k - 1]
        sig[k] = sig[k - 1] * (1 - phi[k, k] ** 2)

    sigma_v = sig[-1]
    arcoefs = phi[1:, -1]
    pacf_ = np.diag(phi).copy()
    pacf_[0] = 1.0
    return sigma_v, arcoefs, pacf_, sig, phi  # return everything

def has_missing(data):
    return np.isnan(np.sum(data))

def acovf(x, adjusted=False, demean=True, fft=True, missing="none", nlag=None):

    x = array_like(x, "x", ndim=1)

    missing = missing.lower()
    if missing == "none":
        deal_with_masked = False
    else:
        deal_with_masked = has_missing(x)
    if deal_with_masked:
        # if missing == "raise":
        #     raise MissingDataError("NaNs were encountered in the data")
        notmask_bool = ~np.isnan(x)  # bool
        if missing == "conservative":
            # Must copy for thread safety
            x = x.copy()
            x[~notmask_bool] = 0
        else:  # "drop"
            x = x[notmask_bool]  # copies non-missing
        notmask_int = notmask_bool.astype(int)  # int

    if demean and deal_with_masked:
        # whether "drop" or "conservative":
        xo = x - x.sum() / notmask_int.sum()
        if missing == "conservative":
            xo[~notmask_bool] = 0
    elif demean:
        xo = x - x.mean()
    else:
        xo = x

    n = len(x)
    lag_len = nlag
    if nlag is None:
        lag_len = n - 1
    elif nlag > n - 1:
        raise ValueError("nlag must be smaller than nobs - 1")

    if not fft and nlag is not None:
        acov = np.empty(lag_len + 1)
        acov[0] = xo.dot(xo)
        for i in range(lag_len):
            acov[i + 1] = xo[i + 1 :].dot(xo[: -(i + 1)])
        if not deal_with_masked or missing == "drop":
            if adjusted:
                acov /= n - np.arange(lag_len + 1)
            else:
                acov /= n
        else:
            if adjusted:
                divisor = np.empty(lag_len + 1, dtype=np.int64)
                divisor[0] = notmask_int.sum()
                for i in range(lag_len):
                    divisor[i + 1] = notmask_int[i + 1 :].dot(
                        notmask_int[: -(i + 1)]
                    )
                divisor[divisor == 0] = 1
                acov /= divisor
            else:  # biased, missing data but npt "drop"
                acov /= notmask_int.sum()
        return acov

    if adjusted and deal_with_masked and missing == "conservative":
        d = np.correlate(notmask_int, notmask_int, "full")
        d[d == 0] = 1
    elif adjusted:
        xi = np.arange(1, n + 1)
        d = np.hstack((xi, xi[:-1][::-1]))
    elif deal_with_masked:
        # biased and NaNs given and ("drop" or "conservative")
        d = notmask_int.sum() * np.ones(2 * n - 1)
    else:  # biased and no NaNs or missing=="none"
        d = n * np.ones(2 * n - 1)

    acov = np.correlate(xo, xo, "full")[n - 1 :] / d[n - 1 :]

    if nlag is not None:
        # Copy to allow gc of full array rather than view
        return acov[: lag_len + 1].copy()
    return acov


def _prepare_data_corr_plot(x, lags, zero):
    zero = bool(zero)
    irregular = False if zero else True
    if lags is None:
        # GH 4663 - use a sensible default value
        nobs = x.shape[0]
        lim = min(int(np.ceil(10 * np.log10(nobs))), nobs - 1)
        lags = np.arange(not zero, lim + 1)
    elif np.isscalar(lags):
        lags = np.arange(not zero, int(lags) + 1)  # +1 for zero lag
    else:
        irregular = True
        lags = np.asanyarray(lags).astype(int)
    nlags = lags.max(0)

    return lags, nlags, irregular

def _plot_corr(
    ax,
    title,
    acf_x,
    confint,
    lags,
    irregular,
    use_vlines,
    vlines_kwargs,
    auto_ylims=False,
    **kwargs,
):
    if irregular:
        acf_x = acf_x[lags]
        if confint is not None:
            confint = confint[lags]

    if use_vlines:
        ax.vlines(lags, [0], acf_x, **vlines_kwargs)
        ax.axhline(**kwargs)

    kwargs.setdefault("marker", "o")
    kwargs.setdefault("markersize", 5)
    if "ls" not in kwargs:
        # gh-2369
        kwargs.setdefault("linestyle", "None")
    ax.margins(0.05)
    ax.plot(lags, acf_x, **kwargs)
    ax.set_title(title)

    ax.set_ylim(-1, 1)
    if auto_ylims:
        ax.set_ylim(
            1.25 * np.minimum(min(acf_x), min(confint[:, 0] - acf_x)),
            1.25 * np.maximum(max(acf_x), max(confint[:, 1] - acf_x)),
        )

    if confint is not None:
        if lags[0] == 0:
            lags = lags[1:]
            confint = confint[1:]
            acf_x = acf_x[1:]
        lags = lags.astype(float)
        lags[0] -= 0.5
        lags[-1] += 0.5
        ax.fill_between(
            lags, confint[:, 0] - acf_x, confint[:, 1] - acf_x, alpha=0.25
        )

def plot_acf(
    x,
    ax=None,
    lags=None,
    *,
    alpha=0.05,
    use_vlines=True,
    adjusted=False,
    fft=False,
    missing="none",
    title="Autocorrelation",
    zero=True,
    auto_ylims=False,
    bartlett_confint=True,
    vlines_kwargs=None,
    **kwargs,
):
    fig, ax = utils.create_mpl_ax(ax)

    lags, nlags, irregular = _prepare_data_corr_plot(x, lags, zero)
    vlines_kwargs = {} if vlines_kwargs is None else vlines_kwargs

    confint = None
    # acf has different return type based on alpha
    acf_x = acf(
        x,
        nlags=nlags,
        alpha=alpha,
        fft=fft,
        bartlett_confint=bartlett_confint,
        adjusted=adjusted,
        missing=missing,
    )
    if alpha is not None:
        acf_x, confint = acf_x[:2]

    _plot_corr(
        ax,
        title,
        acf_x,
        confint,
        lags,
        irregular,
        use_vlines,
        vlines_kwargs,
        auto_ylims=auto_ylims,
        **kwargs,
    )

    return fig


def plot_pacf(
    x,
    ax=None,
    lags=None,
    alpha=0.05,
    method=None,
    use_vlines=True,
    title="Partial Autocorrelation",
    zero=True,
    vlines_kwargs=None,
    **kwargs,
):
    fig, ax = utils.create_mpl_ax(ax)
    vlines_kwargs = {} if vlines_kwargs is None else vlines_kwargs
    lags, nlags, irregular = _prepare_data_corr_plot(x, lags, zero)

    confint = None
    if alpha is None:
        acf_x = pacf(x, nlags=nlags, alpha=alpha)
    else:
        acf_x, confint = pacf(x, nlags=nlags, alpha=alpha)

    _plot_corr(
        ax,
        title,
        acf_x,
        confint,
        lags,
        irregular,
        use_vlines,
        vlines_kwargs,
        **kwargs,
    )

    return fig