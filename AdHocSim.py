try:
    import sys
    from math import sqrt


    komut = open("commands", "r")
    time = int(sys.argv[1])
    commands = []  # tum komutlarin bulundugu liste
    crnode = []  # 0 saniyedeki crnodeler
    kapsama = []  # kapsama ile islem yapilmis halleri
    crnode2 = []
    similator = []
    for i in komut:
        i = str(i).strip("\n")
        i = str(i).split("\t")
        commands.append(i)

    for i in commands:
        if i[0] == "0" and i[1] == "CRNODE":
            i[3] = str(i[3]).split(";")
            i[4] = str(i[4]).split(";")
        if i[0] != "0":
            if i[1] == "MOVE":
                i[3] = i[3].split(";")
            similator.append(i)

    send = []
    for i in commands:
        if i[1] == "CRNODE":
            crnode.append(i)
        if i[0] == "0" and i[1] == "SEND":
            send.append(i)
    for i in commands:
        if i[0] == "0" and i[1] == "CRNODE":
            kapsama.append(i)

    for i in crnode:

        crnode2.append(i)

    for i in kapsama: #konumlari ve kapsamalarini birlestirip onun uzerinden islem yaptim
        i[4][0] = int(i[3][0]) + int(i[4][0])  # dogu
        i[4][1] = int(i[3][0]) - int(i[4][1])  # bati
        i[4][2] = int(i[3][1]) + int(i[4][2])  # kuzey
        i[4][3] = int(i[3][1]) - int(i[4][3])  # guney

    for i in kapsama: #konumlarini int e cevirdim
        i[3][0] = int(i[3][0])
        i[3][1] = int(i[3][1])

    deneme = []
    deneme2 = []
    deneme3 = []
    dic = {}
    nodesayisi = [i[2] for i in crnode if i[0]=="0"]      #baslangictaki node sayisi x1,x2,x3,,,x9


    def komsubulucu():                   #komsularini bulup duzenleyip belli bir formata getirip dic e atan fonksiyon
        for i in kapsama:
            for j in kapsama:
                if i == j:
                    continue
                else:
                    if i[4][1]<=j[3][0]<=i[4][0] and i[4][3]<=j[3][1]<=i[4][2]:
                        deneme.append(i[2])
                        deneme.append(j[2])
                        deneme.append("*")

        sayac = 0
        for i in deneme:

            if sayac == 1:
                b = i
                sayac = sayac + 1
            if sayac == 0:
                a = i
                sayac = sayac + 1
            if i == "*":
                c = a + ":" + b
                deneme2.append(c)
                sayac = 0

        for i in deneme2:
            i = i.split(":")
            deneme3.append(i)

        deneme4=[]
        for i in deneme3:
            for j in deneme3:
                if i == j:
                    continue
                else:
                    if i[0] == j[0]:
                        if i[1] not in deneme4:
                            deneme4.append(i[1])
                        deneme4.append(j[1])
            if len(deneme4)==0:
                dic[i[0]]=[i[1]]
            else:

                dic[i[0]]=deneme4
                deneme4=[]

        for i in crnode:
            if i[0]=="0" and i[2] not in dic.keys():
                dic[i[2]] = [" "]        #komsulari olmayan degerleri dic e ekledim
                                        #dic sozluk tum komsulari icerir.
    komsubulucu()


    a = send[0][2]  # gonderici x1
    b = send[0][3]  # alici     x9
    c = send[0][4]  # byt     miktar
    kolaylik = []


    def kolayliste():            #daha kolay islem yapabilmek icin  x1 [konum],[kapsama] sekline getirdim
        kolaylik2 = []
        for i in crnode:
            kolaylik2.append(i[2])
            kolaylik2.append(i[3])
            kolaylik2.append(i[5])
            kolaylik.append(kolaylik2)
            kolaylik2 = []
    kolayliste()

    guzergah = []
    rota = []
    rota.append([a])

    toplam = 0


    def Navigator(alici):                   #rota bulucu
        if rota[0][-1] ==" ":
            del rota[0]
        if len(rota) != 0:
            yol = rota.pop(0)
            ayrim = yol[-1]

            if ayrim == alici:
                for i in range(len(yol) - 1):
                    aa = yol[i]
                    bb = yol[i + 1]
                    for j in kolaylik:
                        if aa in j:
                            c12 = j[1][0]
                            d12 = j[1][1]
                            e12 = j[2]
                        if bb in j:
                            c21 = j[1][0]
                            d21 = j[1][1]
                            e21 = j[2]
                    asd = sqrt(((c21 - c12) ** 2) + ((d21 - d12) ** 2))
                    sdf = asd / int(e21)
                    global toplam
                    toplam = toplam + sdf
                ara = []
                ara.append(yol)
                ara.append(toplam)
                guzergah.append(ara)                #bu kisimda x1-x3-x5-x7-x9 4.122242 sekline getirdim
                toplam = 0

                if len(rota) != 0:
                    return Navigator(b)


            for i in dic[ayrim]:
                yeniyol = list(yol)
                yeniyol.append(i)
                rota.append(yeniyol)
            return Navigator(b)


        else:
            if len(guzergah) == 0:
                print(a,"ile",b,"arasi guzergah yoktur.")


    Navigator(b)

    print('********************************')
    print('AD-HOC NETWORK SIMULATOR - BEGIN')
    print('********************************')
    print('SIMULATION TIME: ' + str().zfill(2) + ':' + str().zfill(2) + ':' + str().zfill(2))
    for i in nodesayisi:
        print("\tCOMMAND *CRNODE*: New node " + i + " is created")

    print("\tCOMMAND *SEND*: Data is ready to send from " + a + " to " + b)

    komsular = []


    def komsuyazdirici():
        for i in dic.items():
            komsular.append(i)

        print('\tNODES & THEIR NEIGHBORS:',komsular)
        sayi = str(len(guzergah))
        print("\t" + sayi + ' ROUTE(S) FOUND:')


    komsuyazdirici()

    belirleme1 = []


    def rotayazdirici():
        belirleme = []
        guzergah.sort()
        a = 1
        for i in guzergah:
            print('\tROUTE ' + str(a) + ': ' + " -> ".join(i[0]) + '\t COST: {0:.4f}'.format(i[1]))
            wewq = str(a)
            belirleme.append(wewq)
            belirleme.append(i)
            belirleme1.append(belirleme)
            a = a + 1
            belirleme = []


    rotayazdirici()
    guzergah = (sorted(guzergah, key=lambda i: i[1]))
    simtime = (int(c) // time)


    def secilenrota():
        for i in belirleme1:
            if guzergah[0] in i:
                rotam = i[0]

        print("\tSELECTED ROUTE (ROUTE " + rotam + "): " + " -> ".join(guzergah[0][0]))


    secilenrota()

    print("\tPACKET " + "1" + " HAS BEEN SENT")
    print("\tREMAINING DATA SIZE: " + '{0:.6}'.format(str(int(c) - time)) + " BYTE")
    cikart = (int(c) - time)
    start = 1

    while start <= simtime:
        hh = start // 3600
        mm = start // 60
        ss = start % 60

        cikart = cikart - time
        print('SIMULATION TIME: ' + str(hh).zfill(2) + ':' + str(mm).zfill(2) + ':' + str(ss).zfill(2))
        for i in similator:
            if start == int(i[0]):
                if i[1] == "MOVE":        #komutlari ekledim komutlara gereken islemleri yapip tum islemleri tekrarladim
                    ii = i[2]
                    ix = i[3][0]
                    iy = i[3][1]
                    for j in kapsama:
                        if ii == j[2]:
                            print("\tCOMMAND *MOVE*: The location of node " + ii + " is changed")
                            j[4][0] = int(j[4][0]) - int(j[3][0])  # dogu
                            j[4][1] = int(j[3][0]) - int(j[4][1])  # bati
                            j[4][2] = int(j[4][2]) - int(j[3][1])  # kuzey
                            j[4][3] = int(j[3][1]) - int(j[4][3])  # guney
                            j[3][0] = int(ix)
                            j[3][1] = int(iy)
                            j[4][0] = int(j[3][0]) + int(j[4][0])  # dogu
                            j[4][1] = int(j[3][0]) - int(j[4][1])  # bati
                            j[4][2] = int(j[3][1]) + int(j[4][2])  # kuzey
                            j[4][3] = int(j[3][1]) - int(j[4][3])  # guney
                            deneme = []
                            deneme2 = []
                            deneme3 = []
                            komsular = []
                            guzergah = []
                            rota = []
                            belirleme1 = []
                            rota.append([send[0][2]])
                            kolaylik = []
                            dic = {}
                            komsubulucu()
                            kolayliste()
                            Navigator(send[0][3])
                            komsuyazdirici()
                            rotayazdirici()
                            guzergah = (sorted(guzergah, key=lambda i: i[1]))
                            secilenrota()



                elif i[1] == "CRNODE":
                    print("\tCOMMAND *CRNODE*: New node " + str(i[2]) + " is created")
                    i[3] = str(i[3]).split(";")
                    i[4] = str(i[4]).split(";")
                    i[3][0] = int(i[3][0])
                    i[3][1] = int(i[3][1])
                    i[4][0] = int(i[4][0])
                    i[4][1] = int(i[4][1])
                    i[4][2] = int(i[4][2])
                    i[4][3] = int(i[4][3])
                    i[4][0] = int(i[3][0]) + int(i[4][0])  # dogu
                    i[4][1] = int(i[3][0]) - int(i[4][1])  # bati
                    i[4][2] = int(i[3][1]) + int(i[4][2])  # kuzey
                    i[4][3] = int(i[3][1]) - int(i[4][3])  # guney
                    kapsama.append(i)
                    deneme = []
                    deneme2 = []
                    deneme3 = []
                    komsular = []
                    guzergah = []
                    rota = []
                    belirleme1 = []
                    rota.append([send[0][2]])
                    kolaylik = []
                    dic = {}
                    komsubulucu()
                    kolayliste()
                    Navigator(send[0][3])
                    komsuyazdirici()
                    rotayazdirici()
                    guzergah = (sorted(guzergah, key=lambda i: i[1]))
                    secilenrota()


                elif i[1] == "CHBTTRY":
                    print("\tCOMMAND *CHBTTRY*: Battery level of node " + i[2] + " is changed to " + str(i[3]))
                    bataryax = i[2]
                    bataryadeger = i[3]
                    for j in kapsama:
                        if j[2] == bataryax:
                            j[5] = str(bataryadeger)
                            deneme = []
                            deneme2 = []
                            deneme3 = []
                            komsular = []
                            guzergah = []
                            rota = []
                            belirleme1 = []
                            rota.append([send[0][2]])
                            kolaylik = []
                            dic = {}
                            komsubulucu()
                            kolayliste()
                            Navigator(send[0][3])
                            komsuyazdirici()
                            rotayazdirici()
                            guzergah = (sorted(guzergah, key=lambda i: i[1]))
                            secilenrota()



                elif i[1] == "RMNODE":
                    print("\tCOMMAND *RMNODE*: Node " + i[2] + " is removed")
                    kaldirx = i[2]
                    for j in kapsama:
                        if kaldirx == j[2]:
                            kapsama.remove(j)
                            deneme = []
                            deneme2 = []
                            deneme3 = []
                            komsular = []
                            guzergah = []
                            rota = []
                            belirleme1 = []
                            rota.append([send[0][2]])
                            kolaylik = []
                            dic = {}
                            komsubulucu()
                            kolayliste()
                            Navigator(send[0][3])
                            komsuyazdirici()
                            rotayazdirici()
                            guzergah = (sorted(guzergah, key=lambda i: i[1]))
                            secilenrota()

        print("\tPACKET " + str(start + 1) + " HAS BEEN SENT")
        start += 1
        if cikart > 0:
            print("\tREMAINING DATA SIZE: " + '{0:.6}'.format(str(cikart)) + " BYTE")
        else:
            print("\tREMAINING DATA SIZE: " + '{0:.6}'.format("0") + " BYTE")
            print('******************************')
            print('AD-HOC NETWORK SIMULATOR - END')
            print('******************************')


except Exception:
    print("OPPS,There is an exception.Please Check my code sir")
