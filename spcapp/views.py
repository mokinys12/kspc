from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from datetime import datetime


def fill_clnt(sel_fld, fnd_str, del_show):
    rez_all = []
    str_qry = "SELECT id,fam,nam,bkod,addr,is_del,ka_nam,ka_fam FROM spcapp_clients"
    if len(fnd_str):
        if sel_fld == 1:
            str_qry += " WHERE fam LIKE '%" + fnd_str + "%'"
        elif sel_fld == 2:
            str_qry += " WHERE nam LIKE '%" + fnd_str + "%'"
        elif sel_fld == 3:
            str_qry += " WHERE bkod LIKE '%" + fnd_str + "%'"

    if del_show == 0:
        if len(fnd_str):
            str_qry += " AND is_del=0"
        else:
            str_qry += " WHERE is_del=0"

    str_qry += " ORDER BY fam,nam"

    dop_rez = {"fld_num": sel_fld, "fnd_str": fnd_str, "del_show": del_show, "show": "clnt"}

    try:
        cursor = connection.cursor()
        cursor.execute(str_qry)
        rows = cursor.fetchall()

        for row in rows:
            rez_all.append({"id": row[0], "fam": row[1], "nam": row[2], "bkod": row[3],
             "addr": row[4], "is_del": row[5], "kanam": row[6], "kafam": row[7]})

        cursor.close()
    except:
        rez_all = []

    rez = {"rez_all": rez_all, "dop_rez": dop_rez}
    return rez


def fill_dict(sel_fld, fnd_str):
    rez_all = []
    dop_rez = {"fld_num": sel_fld, "fnd_str": fnd_str, "del_show": 0, "show": "dict"}
    str_qry = "SELECT spcapp_dict.id,spcapp_dict.rword,spcapp_dict.lword," \
                "spcapp_works.lwnam,spcapp_works.id" \
                " FROM spcapp_dict LEFT JOIN spcapp_works" \
                " ON spcapp_dict.wrk_type_id=spcapp_works.id"
    if len(fnd_str):
        if sel_fld == 1:
            str_qry += " WHERE rword LIKE '%" + fnd_str + "%'"
        elif sel_fld == 2:
            str_qry += " WHERE lword LIKE '%" + fnd_str + "%'"
    else:
        sel_fld == 1
        str_qry += " WHERE rword LIKE '%" + fnd_str + "%'"
    str_qry += " ORDER BY rword"

    try:
        cursor = connection.cursor()
        cursor.execute(str_qry)
        rows = cursor.fetchall()

        for row in rows:
            rez_all.append({"id": row[0], "rword": row[1], "lword": row[2], "type": row[3], "type_id": row[4]})

        cursor.close()
    except:
        rez_all = []

    rez = {"rez_all": rez_all, "dop_rez": dop_rez}
    return rez


def fill_month():
    rez_all = []
    dop_rez = {"fld_num": "", "fnd_str": "", "del_show": 0, "show": "month"}
    str_qry = "SELECT id,n_ru,n_lt,ko_lt FROM spcapp_month ORDER BY id"

    try:
        cursor = connection.cursor()
        cursor.execute(str_qry)
        rows = cursor.fetchall()

        for row in rows:
            rez_all.append({"id": row[0], "n_ru": row[1], "n_lt": row[2], "ko_lt": row[3]})

        cursor.close()
    except:
        rez_all = []

    rez = {"rez_all": rez_all, "dop_rez": dop_rez}
    return rez


# страница списка клиентов. Загрузка с параметрами по умолчанию
def vindex(request):
    fld_id = 1
    fnd_str = ""
    del_show = 0
    info = ""

    if isinstance(request.GET.get('sel_fld'), str):
        fld_id = int(request.GET.get('sel_fld'))
    if isinstance(request.GET.get('alarm'), str):
        info = request.GET.get('alarm')
    if isinstance(request.GET.get('fnd_str'), str):
        fnd_str = request.GET.get('fnd_str')
    if isinstance(request.GET.get('isdel'), str):
        del_show = int(request.GET.get('isdel'))

    # return HttpResponse("Здравствуй, Люба! Тут будет список клиентов")
    all_rez = fill_clnt(fld_id, fnd_str, del_show)
    rez = all_rez["rez_all"]
    dop_rez = all_rez["dop_rez"]
    if len(info) > 0:
        dop_rez["alarm"] = info

    return render(request, 'spcapp/clients.html', {"words": rez, "dop": dop_rez})


# скрыть/показать удаленных клиентов
def visdel(request):
    fld_id = 1
    fnd_str = ""
    del_show = 0

    if isinstance(request.GET.get('sel_fld'), str):
        fld_id = int(request.GET.get('sel_fld'))
    if isinstance(request.GET.get('isdel'), str):
        del_show = int(request.GET.get('isdel'))
    if isinstance(request.GET.get('fnd_str'), str):
        fnd_str = request.GET.get('fnd_str')

    all_rez = fill_clnt(fld_id, fnd_str, del_show)
    rez = all_rez["rez_all"]
    dop_rez = all_rez["dop_rez"]
    # dop_rez["row_id"] = -1 # текущая строка ###############
    dop_rez["show"] = "clnt"

    return render(request, 'spcapp/clients.html', {"words": rez, "dop": dop_rez})


# новый клиент либо редактирование старого
def vnew_clnt(request):
    tek_id = "0"
    fld_id = 1
    fnd_str = ""
    del_show = 0
    str_qry = ""
    rez_all = {}  # здесь может быть только одна строка
    is_good = True

    if isinstance(request.GET.get('sel_fld'), str):
        fld_id = int(request.GET.get('sel_fld'))
    if isinstance(request.GET.get('row_id'), str):
        tek_id = request.GET.get('row_id')
    if isinstance(request.GET.get('fnd_str'), str):
        fnd_str = request.GET.get('fnd_str')
    if isinstance(request.GET.get('isdel'), str):
        del_show = int(request.GET.get('isdel'))

    if int(tek_id) > 0:
        # return HttpResponse("запись № "+tek_id)
        str_qry = "SELECT id,fam,nam,bkod,addr,is_del,ka_nam,ka_fam" \
                  " FROM spcapp_clients" \
                  " WHERE id=" + tek_id
        try:
            cursor = connection.cursor()
            cursor.execute(str_qry)
            row = cursor.fetchone()

            rez_all["id"] = row[0]
            rez_all["fam"] = row[1]
            rez_all["nam"] = row[2]
            rez_all["bkod"] = row[3]
            rez_all["addr"] = row[4]
            rez_all["is_del"] = row[5]
            rez_all["kanam"] = row[6]
            rez_all["kafam"] = row[7]

            cursor.close()
        except:
            is_good = False
    else:
        rez_all["id"] = 0
        rez_all["fam"] = "P"
        rez_all["nam"] = "V"
        rez_all["bkod"] = "000-00-000"
        rez_all["addr"] = "Klaipėda"
        rez_all["is_del"] = 0
        rez_all["kanam"] = "kV"
        rez_all["kafam"] = "kP"

    dop_rez = {"fld_num": fld_id, "fnd_str": fnd_str, "del_show": del_show, "show": "clnt"}
    if not is_good:
        dop_rez["alarm"] = "Ошибка: не нашел клиента № "+tek_id

    return render(request, 'spcapp/client.html', {"words": rez_all, "dop": dop_rez})


# сохранение отредактированного клиента
def vsave_clnt(request):
    fld_id = 1
    fnd_str = ""
    del_show = 0
    tek_id = 0
    tfam = ""
    tkfam = ""
    tnam = ""
    tknam = ""
    splitnam = []
    tmp_str = ""
    tbkod = ""
    taddr = ""
    tis_del = 0  # флаг того, что текущая запись удалена
    is_good = True
    err = 0
    err_str = ""
    str_tmp = "SELECT id FROM spcapp_clients WHERE "
    str_qry = ""
    dop_rez = {}

    # проверим, передались ли необходимые данные из формы
    if request.method == "POST":
        if isinstance(request.POST.get('nam'), str):
            tnam = request.POST.get('nam')
        else:
            is_good = False
            err = 1
        if is_good:
            if isinstance(request.POST.get('kanam'), str):
                tknam = request.POST.get('kanam')
            else:
                is_good = False
                err = 1
        if is_good:
            if isinstance(request.POST.get('fam'), str):
                tfam = request.POST.get('fam')
            else:
                is_good = False
                err = 2
        if is_good:
            if isinstance(request.POST.get('kafam'), str):
                tkfam = request.POST.get('kafam')
            else:
                is_good = False
                err = 2

        if is_good:
            if isinstance(request.POST.get('bkod'), str):
                tbkod = request.POST.get('bkod')
            if isinstance(request.POST.get('addr'), str):
                taddr = request.POST.get('addr')
            if isinstance(request.POST.get('is_del'), str):
                tis_del = 1
            if isinstance(request.POST.get('sel_fld'), str):
                fld_id = int(request.POST.get('sel_fld'))
            if isinstance(request.POST.get('row_id'), str):
                tek_id = int(request.POST.get('row_id'))
            if isinstance(request.POST.get('fnd_str'), str):
                fnd_str = request.POST.get('fnd_str')
            if isinstance(request.POST.get('isdel'), str):
                del_show = int(request.POST.get('isdel'))

    # проверка введенных данных
    if is_good:
        if len(tnam.strip()) >= 5:  # думаю, короче имена не бывают
            tnam = tnam.strip()
            splitnam = tnam.split(" ")
            if len(splitnam) > 1:  # составное имя
                tnam = ""
                for tmp_str in splitnam:
                    if not tmp_str.isalpha():
                        is_good = False
                        break
                    else:
                        tnam += tmp_str.lower().capitalize()
                        tnam += " "
                if is_good:
                    tnam = tnam.strip()
            else:
                if not tnam.isalpha():
                    is_good = False
                else:
                    tnam = tnam.lower().capitalize()  # первая буква заглавная
        else:
            is_good = False
        if not is_good:
            err = 1
    if is_good:
        tknam = tknam.strip()
        if len(tknam) > 0:
            tknam = tknam.strip()
            splitnam = tknam.split(" ")
            if len(splitnam) > 1:  # составное имя
                tknam = ""
                for tmp_str in splitnam:
                    if not tmp_str.isalpha():
                        is_good = False
                        break
                    else:
                        tknam += tmp_str.lower().capitalize()
                        tknam += " "
                if is_good:
                    tknam = tknam.strip()
            else:
                if not tknam.isalpha():
                    is_good = False
                else:
                    tknam = tknam.lower().capitalize()
        else:
            is_good = False
        if not is_good:
            err = 1
    if is_good:
        if len(tfam.strip()) >= 5:
            tfam = tfam.strip()
            if not tfam.isalpha():
                is_good = False
            else:
                tfam = tfam.lower().capitalize()  # первая буква заглавная
        else:
            is_good = False
        if not is_good:
            err = 2
    if is_good:
        tkfam = tkfam.strip()
        if len(tkfam) > 0:
            if not tkfam.isalpha():
                is_good = False
            else:
                tkfam = tkfam.lower().capitalize()
        else:
            is_good = False
        if not is_good:
            err = 2
    if is_good:
        if len(tbkod.strip()) != "000-00-000":  # не по умолчанию
            tbkod = tbkod.strip()
            if len(tbkod) < 10 or len(tbkod) >11:
                is_good = False
            else:
                if not tbkod[:3].isdigit() or not tbkod[4:6].isdigit() or not tbkod[7:].isdigit():
                    is_good = False
                else:
                    if not tbkod[3] == '-' or not tbkod[6] == "-":
                        is_good = False
        if not is_good:
            err = 3

    if is_good:
        if len(taddr.strip()) < 8:  # Klaipeda
            is_good = False
            err = 4
        else:
            taddr = taddr.strip()

    if not is_good:
        if err == 0:
            err_str = "непонятная ошибка (vsave_clnt)"
        elif err == 1:
            err_str = "введите имя клиента"
        elif err == 2:
            err_str = "введите фамилию клиента"
        elif err == 3:
            err_str = "введите правильный код клиента"
        elif err == 4:
            err_str = "адрес должен содержать хотя бы название города"

        dop_rez["alarm"] = err_str
    else:  # теперь проверим на неповторяющиеся записи
        try:
            cursor = connection.cursor()
            str_qry = str_tmp + "UPPER(nam)='" + tnam.upper() + "' AND UPPER(fam)='" + tfam.upper() + "'"
            cursor.execute(str_qry)
            row = cursor.fetchone()
            if row and row[0] != tek_id:  # этот клиент с другим id
                is_good = False
                err = 1

            if is_good:
                if tbkod != "000-00-000":
                    str_qry = str_tmp + "bkod='" + tbkod + "' AND id!=" + str(tek_id)
                    cursor.execute(str_qry)
                    row = cursor.fetchone()
                    if row:
                        is_good = False
                        err = 3

            cursor.close()
        except:
            is_good = False
            err = 0

        if not is_good:
            if not is_good:
                if err == 0:
                    err_str = "не могу соединиться с базой (vsave_clnt)"
                elif err == 1:
                    err_str = "клиент с таким именем и фамилией уже существует"
                elif err == 3:
                    err_str = "такой код клиента уже существует"
        else:
            # err_str = "Начнем сохранение"
            if tek_id == 0:
                str_qry = "INSERT INTO spcapp_clients(fam,nam,bkod,addr,is_del,ka_fam,ka_nam) " \
                    "VALUES('" + tfam + "','" + tnam + "','" + tbkod + "'," \
                        "'" + taddr + "'," + str(tis_del) + ",'" + tkfam + "','" + tknam + "')"
            else:
                str_qry = "UPDATE spcapp_clients SET fam='" + tfam + "',nam='" + tnam + "'," \
                    "bkod='" + tbkod + "',addr='" + taddr + "',is_del=" + str(tis_del) + "," \
                    "ka_fam='" + tkfam + "',ka_nam='" + tknam + "' WHERE id=" + str(tek_id)
            try:
                cursor = connection.cursor()
                cursor.execute(str_qry)
                cursor.close()
                err_str = "Записано"
            except:
                err_str = "Ошибка записи"
                is_good = False

    if not is_good:
        return HttpResponse(err_str)
    else:
        all_rez = fill_clnt(fld_id, fnd_str, del_show)
        rez = all_rez["rez_all"]
        dop_rez = all_rez["dop_rez"]
        dop_rez["alarm"] = err_str

        return render(request, 'spcapp/clients.html', {"words": rez, "dop": dop_rez})


# удаление выбранного клиента
def vdelclnt(request):
    tek_id = "0"
    fld_id = 1
    fnd_str = ""
    del_show = 0
    str_qry = ""
    is_good = True

    if isinstance(request.GET.get('sel_fld'), str):
        fld_id = int(request.GET.get('sel_fld'))
    if isinstance(request.GET.get('row_id'), str):
        tek_id = request.GET.get('row_id')
    if isinstance(request.GET.get('fnd_str'), str):
        fnd_str = request.GET.get('fnd_str')
    if isinstance(request.GET.get('isdel'), str):
        del_show = request.GET.get('isdel')

    if int(tek_id) > 0:
        # str_qry = "DELETE FROM spcapp_clients WHERE id="+tek_row
        str_qry = "UPDATE spcapp_clients SET is_del=ABS(is_del-1) WHERE id=" + tek_id
        try:
            cursor = connection.cursor()
            rows = cursor.execute(str_qry)
            cursor.close()
        except:
            is_good = False
            # написать, что косяк в dop_rez["alarm"]

    # return HttpResponse(rows)
    all_rez = fill_clnt(fld_id, fnd_str, del_show)
    rez = all_rez["rez_all"]
    dop_rez = all_rez["dop_rez"]
    if not is_good or rows == 0:
        dop_rez["alarm"] = "Ошибка: не удалилась id="+tek_id

    return render(request, 'spcapp/clients.html', {"words": rez, "dop": dop_rez})


# преобразуем число в строку
def moneyToStr(sum=0):
    tmp_str = ""
    tmp_sum = ""
    tmp_val = 0
    txt100 = []
    txt10 = []
    txt11 = []
    txt1 = []

    # сотни
    txt100.append("")
    txt100.append("šimtas")
    txt100.append("šimtai")
    # массивы написания чисел
    # десятки
    txt10.append("")
    txt10.append("")
    txt10.append("dvidešimt")
    txt10.append("trysdešimt")
    txt10.append("keturiasdešimt")
    txt10.append("penkiasdešimt")
    txt10.append("šešiasdešimt")
    txt10.append("septyniasdešimt")
    txt10.append("aštuoniasdešimt")
    txt10.append("devyniasdešimt")
    # с 10 по 19
    txt11.append("dešimt")
    txt11.append("vienuolika")
    txt11.append("dvylika")
    txt11.append("trylika")
    txt11.append("keturiolika")
    txt11.append("penkiolika")
    txt11.append("šešiolika")
    txt11.append("septyniolika")
    txt11.append("aštuoniolika")
    txt11.append("devyniolika")
    # единицы
    txt1.append("")
    txt1.append("vienas")
    txt1.append("du")
    txt1.append("trys")
    txt1.append("keturi")
    txt1.append("penki")
    txt1.append("šeši")
    txt1.append("septyni")
    txt1.append("aštuoni")
    txt1.append("devini")

    # превращаем сумму в строку
    # разбиваем сумму на разряды и передаем их в массив
    tmp_val = sum % 1000  # с 1 по 999
    if tmp_val < 10:
       tmp_str = "00"
    elif tmp_val < 100:
       tmp_str = "0"
    tmp_str += str(tmp_val)  # число с лидирующими нулями

    # из tmp_str заполним tmp_sum
    # if tmp_str != "000":
    if tmp_str[0] != "0":
        tmp_sum = txt1[int(tmp_str[0])] + " "
        if int(tmp_str[0]) == 1:
            tmp_sum += txt100[1]
        else:
            tmp_sum += txt100[2]

    if tmp_str[1] != "0":
        if len(tmp_sum) > 0:  # уже записаны сотни
            tmp_sum += " "
        if tmp_str[1] == "1":
            tmp_sum += txt11[int(tmp_str[2])]  # последняя цифра определяет название
        else:
            tmp_sum += txt10[int(tmp_str[1])]

    if tmp_str[1] != "1":  # если была 1, то в предыдущей итерации все уже записали
        # if tmp_str[2] != "0":
        if len(tmp_sum) > 0 and tmp_str[0] != "0":
            tmp_sum += " "
        tmp_sum += txt1[int(tmp_str[2])]

    if tmp_str[2] == "0" and len(tmp_sum) == 0:
        tmp_sum = "nulis"

    if len(tmp_sum) > 0:
        if int(tmp_str[2]) == 0:
            if tmp_str == "000":
                tmp_sum += " euro"  # нуль евро
            else:
                tmp_sum += " eurų"
        elif int(tmp_str[2]) == 1:
            if int(tmp_str[1]) != 1:
                tmp_sum += " euras"
            else:
                tmp_sum += " eurai"
        else:
            tmp_sum += " eurai"

    return tmp_sum


# страница банковского счета выбранному клиенту
def vaccount(request):
    fld_id = 1  # номер поля в таблице для поиска в ней
    fnd_str = ""  # строка поиска
    del_show = 0  # показывать ли удаленные
    tek_id = "0"
    mnam = "XXX"
    mknam = "XXX"
    mfam = "XXX"
    mkfam = "XXX"
    mbkod = "XXX"
    now = datetime.today()
    nday = now.day
    nmon = now.month
    smon = ""
    oldmon = ""
    ngod = now.year
    oldmon = nmon - 1
    if oldmon == 0:
        oldmon = 12
    str_money = ""
    tmp_money = str_money
    val_money = 0
    pos_digit = -1
    is_good = True

    if isinstance(request.GET.get('money'), str):
        str_money = request.GET.get('money')
    if isinstance(request.GET.get('row_id'), str):
        tek_id = request.GET.get('row_id')
    if isinstance(request.GET.get('fld_num'), str):
        fld_id = int(request.GET.get('fld_num'))
    if isinstance(request.GET.get('fnd_str'), str):
        fnd_str = request.GET.get('fnd_str')
    if isinstance(request.GET.get('isdel'), str):
        del_show = int(request.GET.get('isdel'))

    if tek_id == "0" or (not str_money or str_money == "0"):
        is_good = False

    str_qry = "SELECT n_lt FROM spcapp_month WHERE id=" + str(nmon)

    try:
        cursor = connection.cursor()
        cursor = connection.cursor()
        cursor.execute(str_qry)
        row = cursor.fetchone()
        smon = row[0]  # дата заполнения

        str_qry = "SELECT ko_lt FROM spcapp_month WHERE id=" + str(oldmon)
        cursor.execute(str_qry)
        row = cursor.fetchone()
        oldmon = row[0]  # за какой месяц оплата

        str_qry = "SELECT ka_nam,ka_fam,bkod,nam,fam FROM spcapp_clients WHERE id=" + tek_id
        cursor.execute(str_qry)
        row = cursor.fetchone()
        mknam = row[0]
        mkfam = row[1]
        mbkod = row[2]
        mnam = row[3]
        mfam = row[4]

        cursor.close()
    except:
        is_good = False

    if is_good:
        tmp_money = str_money
        val_money = int(float(str_money)//1)  # целая часть числа
        if len(str(val_money)) < len(str_money):
            # то есть есть и дробная часть
            str_money = moneyToStr(val_money) + "," + str_money[(len(str(val_money)) + 1):] + "ct."
        else:
            str_money = moneyToStr(val_money) + ",00ct."

    rez = {"god": ngod, "mon": smon, "day": nday, "oldmon": oldmon, "suma": str_money, 
    "nam": mnam, "fam": mfam, "kod": mbkod, "knam": mknam, "kfam": mkfam}
    dop = {"fld_num": fld_id, "fnd_str": fnd_str, "del_show": del_show, "id": tek_id, "tmp_money": tmp_money}
    if not is_good:
        dop["alarm"] = "скорее всего, не введена сумма"

    #    return HttpResponse("Форма для банка")
    return render(request, "spcapp/account.html", {"words": rez, "dop": dop})


# страница словаря
def vdict(request):
    # return HttpResponse("Словарик")
    #    return render(request, "spcapp/dict.html")
    fld_id = 1
    fnd_str = ""
    info = ""

    if isinstance(request.GET.get('sel_fld'), str):
        fld_id = int(request.GET.get('sel_fld'))
    if isinstance(request.GET.get('alarm'), str):
        info = request.GET.get('alarm')
    if isinstance(request.GET.get('fnd_str'), str):
        fnd_str = request.GET.get('fnd_str')

    # return HttpResponse("Здравствуй, Люба! Тут будет список клиентов")
    all_rez = fill_dict(fld_id, fnd_str)
    rez = all_rez["rez_all"]
    dop_rez = all_rez["dop_rez"]
    if len(info) > 0:
        dop_rez["alarm"] = info

    return render(request, 'spcapp/dict.html', {"words": rez, "dop": dop_rez})


# поля одной записи в словаре для правки/создания новой записи (если id==0)
def vnew_dict(request):
    # return HttpResponse("Создание/редактирование перевода")
    tek_id = "0"
    fld_id = 1
    fnd_str = ""
    str_qry = ""
    rez_all = {}  # здесь может быть только одна строка
    types = [{"t_id": 0, "t_nam": ""}]
    is_good = True

    if isinstance(request.GET.get('sel_fld'), str):
        fld_id = int(request.GET.get('sel_fld'))
    if isinstance(request.GET.get('row_id'), str):
        tek_id = request.GET.get('row_id')
    if isinstance(request.GET.get('fnd_str'), str):
        fnd_str = request.GET.get('fnd_str')

    if int(tek_id) > 0:
        # return HttpResponse("запись № "+tek_id)
        str_qry = "SELECT id,rword,lword,wrk_type_id FROM spcapp_dict WHERE id=" + tek_id
        try:
            cursor = connection.cursor()
            cursor.execute(str_qry)
            row = cursor.fetchone()

            if not row:
                is_good = False
            else:
                rez_all["id"] = row[0]
                rez_all["rword"] = row[1]
                rez_all["lword"] = row[2]
                rez_all["type_id"] = row[3]

            if is_good:
                str_qry = "SELECT id,rwnam FROM spcapp_works"
                cursor.execute(str_qry)
                rows = cursor.fetchall()

                if not rows:
                    is_good = False
                else:
                    for row in rows:
                        types.append({"t_id": row[0], "t_nam": row[1]})

            cursor.close()
        except:
            is_good = False
    else:
        rez_all["id"] = 0
        rez_all["rword"] = ""
        rez_all["lword"] = ""
        rez_all["type_id"] = 0

    dop_rez = {"fld_num": fld_id, "fnd_str": fnd_str, "show": "dict"}
    if not is_good:
        dop_rez["alarm"] = "Ошибка: не нашел запись № "+tek_id

    return render(request, 'spcapp/dictrow.html', {"words": rez_all, "dop": dop_rez, "types": types})


# сохранение строки словаря
def vsave_dict(request):
    fld_id = 1
    fnd_str = ""
    tek_id = 0
    trwrd = ""
    tlwrd = ""
    tek_type = "0"
    is_good = True
    err = 0
    err_str = ""
    str_qry = ""
    dop_rez = {}

    # проверим, передались ли необходимые данные из формы
    if request.method == "POST":
        if isinstance(request.POST.get('row_id'), str):
            tek_id = int(request.POST.get('row_id'))
        if isinstance(request.POST.get('sel_fld'), str):
            fld_id = int(request.POST.get('sel_fld'))
        if isinstance(request.POST.get('fnd_str'), str):
            fnd_str = request.POST.get('fnd_str')
        if isinstance(request.POST.get('rwrd'), str):
            trwrd = request.POST.get('rwrd')
        if isinstance(request.POST.get('wtypes'), str):
            tek_type = request.POST.get('wtypes')
        else:
            is_good = False
            err = 1
        if is_good:
            if isinstance(request.POST.get('lwrd'), str):
                tlwrd = request.POST.get('lwrd')
            else:
                is_good = False
                err = 2

    # Начнем сохранение
    if is_good:
        if tek_id == 0:
            str_qry = "INSERT INTO spcapp_dict(rword,lword,wrk_type_id)" \
                        " VALUES('" + trwrd + "','" + tlwrd + "'," + tek_type + ")"
        else:
            str_qry = "UPDATE spcapp_dict SET rword='" + trwrd + "',lword='" + tlwrd + "'," \
                        "wrk_type_id=" + tek_type +" WHERE id=" + str(tek_id)

        try:
            cursor = connection.cursor()
            cursor.execute(str_qry)
            cursor.close()
            err_str = "Записано"
        except:
            err = 0
            is_good = False

    if not is_good:
        if err == 0:
            err_str = "ошибка записи (vsave_dict)"
        elif err == 1:
            err_str = "отсутствует русский перевод"
        elif err == 2:
            err_str = "отсутствует литовский перевод"

    if not is_good:
        return HttpResponse(err_str)
    else:
        all_rez = fill_dict(fld_id, fnd_str)
        rez = all_rez["rez_all"]
        dop_rez = all_rez["dop_rez"]
        dop_rez["alarm"] = err_str

    return render(request, 'spcapp/dict.html', {"words": rez, "dop": dop_rez})


# удаление выбранной строки словаря (а надо ли?)
def vdeldict(request):
    fld_id = 1
    tek_row = "0"
    fnd_str = ""
    str_qry = ""
    is_good = True
    rows = 0

    if isinstance(request.GET.get('sel_fld'), str):
        fld_id = int(request.GET.get('sel_fld'))
    if isinstance(request.GET.get('row_id'), str):
        tek_row = request.GET.get('row_id')
    if isinstance(request.GET.get('fnd_str'), str):
        fnd_str = request.GET.get('fnd_str')

    if int(tek_row) > 0:
        str_qry = "DELETE FROM spcapp_dict WHERE id="+tek_row
        try:
            cursor = connection.cursor()
            rows = cursor.execute(str_qry)
            cursor.close()
        except:
            is_good = False
            # написать, что косяк в dop_rez["alarm"]

    # return HttpResponse(rows)
    all_rez = fill_dict(fld_id, fnd_str)
    rez = all_rez["rez_all"]
    dop_rez = all_rez["dop_rez"]
    if not is_good or rows == 0:
        dop_rez["alarm"] = "Ошибка: не удалилось"

    return render(request, 'spcapp/dict.html', {"words": rez, "dop": dop_rez})


# список месяцев (вряд ли нужен)
def vmonth(request):
    #    return HttpResponse("месяцы")
    all_rez = fill_month()
    rez = all_rez["rez_all"]
    dop_rez = all_rez["dop_rez"]

    return render(request, 'spcapp/month.html', {"words": rez, "dop": dop_rez})


# выбор поля для поиска в базе
def vsel_fld(request):
    fld_id = 1  # номер поля в таблице для поиска в ней
    fnd_str = ""  # строка поиска
    del_show = 0  # показывать ли удаленные
    page_name = ""  # что именно отображается
    file_name = ""

    if isinstance(request.GET.get('fld_num'), str):
        fld_id = int(request.GET.get('fld_num'))
    if isinstance(request.GET.get('fnd_str'), str):
        fnd_str = request.GET.get('fnd_str')
    if isinstance(request.GET.get('what_show'), str):
        page_name = request.GET.get('what_show')
    if isinstance(request.GET.get('isdel'), str):
        del_show = int(request.GET.get('isdel'))

    if page_name == 'clnt':
        all_rez = fill_clnt(fld_id, fnd_str, del_show)
        file_name = 'spcapp/clients.html'
    elif page_name == 'dict':
        all_rez = fill_dict(fld_id, fnd_str)
        file_name = 'spcapp/dict.html'
    else:
        # snam='month':
        all_rez = fill_month()
        file_name = 'spcapp/month.html'

    rez = all_rez["rez_all"]
    dop_rez = all_rez["dop_rez"]
    # dop_rez["show"] = del_show

    return render(request, file_name, {"words": rez, "dop": dop_rez})


# поиск в таблице
def vfnd_row(request):
    fld_id = 1  # номер поля в таблице для поиска в ней (по умолчанию-по фамилии)
    fnd_str = ""  # строка поиска
    page_name = ""  # что именно отображается
    del_show = 0
    file_name = ""

    if isinstance(request.GET.get('sel_fld'), str):
        # если есть номер поля для поиска
        fld_id = int(request.GET.get('sel_fld'))
    if isinstance(request.GET.get('fnd_str'), str):
        # если есть строка поиска
        fnd_str = request.GET.get('fnd_str')
    if isinstance(request.GET.get('what_show'), str):
        # если есть информация об отображаемом (вообще-то, должна быть)
        page_name = request.GET.get('what_show')
    if isinstance(request.GET.get('isdel'), str):
        del_show = int(request.GET.get('isdel'))

    if page_name == 'clnt':
        all_rez = fill_clnt(fld_id, fnd_str, del_show)
        file_name = 'spcapp/clients.html'
    elif page_name == 'dict':
        all_rez = fill_dict(fld_id, fnd_str)
        file_name = 'spcapp/dict.html'
    else:
        # page_name='month':
        all_rez = fill_month()
        file_name = 'spcapp/month.html'
    # разделим всю собранную информацию на 2 кучки (для удобства)
    rez = all_rez["rez_all"]
    dop_rez = all_rez["dop_rez"]
    dop_rez["show"] = page_name

    # return render(request, 'spcapp/dict.html', {"words": rez, "dop": dop_rez})
    return render(request, file_name, {"words": rez, "dop": dop_rez})
