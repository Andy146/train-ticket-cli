#!/usr/bin/python3
import re
import sqlite3 as sql
import time
import datetime

con = sql.connect("trains.db")
cursor = sql.Cursor(con)

#Printer tabellinformasjon på en relativt pen måte
# utifra overskrifter og radinfo fra sql
def printTable(headers,rows):
    header_len = 0
    col_lens = []
    headerToPrint = "|"
    for item in headers:
        #Initialiserer nødvendig bredde på hver kolonne
        col_lens.append(len(str(item))+1)

    #Finner hvor bred tabellen er nødt til å være
    for row in rows:
        length = 0
        col = 0
        for item in row:
            #Oppdaterer bredden på kolonnen
            if(len(str(item))+1>col_lens[col]):
                col_lens[col] = len(str(item))+1
            col+=1
    col = 0
    for item in headers:
        diff = col_lens[col] - len(str(item))+1
        col+=1
        headerToPrint += " "*(diff//2) + str(item)+ " "*(diff-diff//2) +"|"
    divider_len = sum(col_lens)+2*len(col_lens)+1
    divider = "-"*divider_len
    print(divider)
    print(headerToPrint)

    #Printer annen divider under overskriftene
    print("#"*divider_len)
    for row in rows:
        rowToPrint = "|"
        col = 0
        for item in row:
            if(item==None):
                item = "--"
            diff = col_lens[col] - len(str(item))+1
            col+=1
            rowToPrint += " "*(diff//2) + str(item)+ " "*(diff-diff//2) +"|"
        print(rowToPrint)
        print(divider)


#Åpner menyen for å gi brukeren valg
def menuSelection(validChoices):
    header = "Hva ønsker du å gjøre? (skriv inn teksten som står inne i '[]')"
    divider = "-"*len(header)
    while True:
        print(header)
        print(divider)
        for key, desc in validChoices.items():
            print(desc, "[" + key + "]")
        print("\n")
        selection = input("Ditt valg: ")
        for key in validChoices.keys():
            if(selection==key):
                return selection
        print("Beklager, men "+selection+" er ikke et gyldig valg, vennligst prøv igjen")

#Registrerer en ny bruker utifra informasjonen kunden gir
# og returnerer kundenummeret til den nye kunden
def registerCustomer():
    name = input("Hva er ditt fulle navn? ")
    while True:
        email = input("Hva er din epost-adresse? ")
        if(not re.match("^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$",email)):
            print("Vennligst skriv inn en gyldig epost-adresse\n")
            continue
        break
    while True:
        phone = input("Hva er ditt mobilnummer? (8 siffer) ")
        if(not re.match("^[0-9]{8}$",phone)):
            print("Vennligst skriv inn et gyldig mobilnummer (8 siffer)\n")
            continue
        break
    insert = f"INSERT INTO Kunde (navn, epost, mobilnummer) VALUES (\"{name}\", \"{email}\", \"{phone}\")"
    cursor.execute(insert)

    getID = "SELECT * FROM Kunde WHERE kundenummer IN (SELECT max(kundenummer) FROM Kunde);"
    cursor.execute(getID)
    result = cursor.fetchall()
    con.commit()
    printTable(["Kundenummer", "Navn", "Epost", "Mobilnummer"], result)
    print("\nDet er viktig at du husker ditt kundenummer:", result[0][0],"\n")
    time.sleep(3)
    return result[0]

#Logger inn en eksisterende kunde og returnerer
# kundenummeret til denne kunden
def logIn():
    while True:
        number = input("Hva er ditt kundenummer? ")
        query = f"SELECT * FROM Kunde WHERE kundenummer={number};"
        cursor.execute(query)
        result = cursor.fetchall()
        if(len(result)==0):
            print("Beklager, men dette kundenummeret tilhører ingen bruker, vennligst prøv igjen")
            continue
        break
    return result[0]


#Printer ut alle billetter en bruker har i fremtiden
# feiler hvis brukeren ikke er logget inn
def viewTickets(customerID):
    if(customerID==-1):
        print("Du er ikke logget inn, og har derav ingen kjøp å vise")
        return
    
    query_seattickets = f"SELECT Ordre.ordrenummer, Ordre.ordredato, Ordre.ordretid, Billett.ruteID, Billett.start, Start.avreise, Billett.ende, Ende.ankomst, Billett.dato AS avreisedato, VognOppsett.vognnummer, SitteBillett.setenummer FROM Ordre JOIN Billett USING(ordrenummer) JOIN SitteBillett USING(billettID) JOIN Sete USING(vognID, setenummer) JOIN Vogn USING(vognID) JOIN VognOppsett USING(vognID, ruteID) JOIN Togrute USING(ruteID) JOIN Rutetabell as Start ON Start.ruteID=Billett.ruteID AND Start.stasjonNavn=Billett.start JOIN Rutetabell as Ende ON Ende.ruteID=Billett.ruteID AND Ende.stasjonNavn=Billett.ende WHERE DATE(Billett.dato)>DATE(\"{datetime.datetime.now().date()}\") AND Ordre.kundenummer={customerID} ORDER BY Billett.dato, Ordre.ordrenummer, Billett.ruteID;"
    cursor.execute(query_seattickets)
    seattickets = cursor.fetchall()

    query_sleeptickets = f"SELECT Ordre.ordrenummer, Ordre.ordredato, Ordre.ordretid, Billett.ruteID, Billett.start, Start.avreise, Billett.ende, Ende.ankomst, Billett.dato AS avreisedato, VognOppsett.vognnummer, SoveBillett.kupeenummer FROM Ordre JOIN Billett USING(ordrenummer) JOIN SoveBillett USING(billettID) JOIN Kupee USING(vognID, kupeenummer) JOIN Vogn USING(vognID) JOIN VognOppsett USING(vognID, ruteID) JOIN Togrute USING(ruteID) JOIN Rutetabell as Start ON Start.ruteID=Billett.ruteID AND Start.stasjonNavn=Billett.start JOIN Rutetabell as Ende ON Ende.ruteID=Billett.ruteID AND Ende.stasjonNavn=Billett.ende WHERE DATE(Billett.dato)>DATE(\"{datetime.datetime.now().date()}\") AND Ordre.kundenummer={customerID} ORDER BY Billett.dato, Ordre.ordrenummer, Billett.ruteID;"
    cursor.execute(query_sleeptickets)
    sleeptickets = cursor.fetchall()

    print("Her er dine kjøp for fremtidige reiser")
    print("\nSitteplasser")
    printTable(["Ordrenummer", "Ordredato", "Ordretidspunkt", "Rutenummer", "Startstasjon", "Avreise", "Endestasjon", "Ankomst", "Avreisedato", "Vogn", "Sete"], seattickets)

    print("\n\nSoveplasser")
    printTable(["Ordrenummer", "Ordredato", "Ordretidspunkt", "Rutenummer", "Startstasjon", "Avreise", "Endestasjon", "Ankomst", "Avreisedato", "Vogn", "Kupee"], sleeptickets)

    return

#Viser alle ruter som går forbi en stasjon brukeren velger på en ukedag
# brukeren velger
def viewRoutes():
#TODO endre på query slik at man kan se hvor toget går hen
    while True:
        station = input("Hvilken stasjon ønsker du å se ruter for? (skriv 'hjelp' for en liste over stasjoner) ")
        if(station=="lukk"):
            break
        if(station=="hjelp"):
            query = "SELECT navn FROM Stasjon;"
            cursor.execute(query)
            result = cursor.fetchall()
            print("Her er en liste over alle stasjoner:")
            printTable(["Stasjon"], result)
            continue
        day = input("Hvilken ukedag ønsker du å se ruter for? ")
        
        query = f"SELECT Togrute.ruteID as rutenummer,Rutetabell.stasjonNavn as stasjon, endestasjon, Rutetabell.ankomst, Rutetabell.avreise, KjørerPåDag.ukedag FROM Rutetabell JOIN Togrute ON Togrute.ruteID=Rutetabell.ruteID JOIN KjørerPåDag ON Togrute.ruteID=KjørerPåDag.ruteID JOIN (SELECT Rutetabell.stasjonNavn AS endestasjon, Togrute.ruteID FROM Rutetabell JOIN Togrute ON Rutetabell.ruteID=Togrute.ruteID WHERE Rutetabell.avreise IS NULL) USING(ruteID) WHERE LOWER(ukedag)=LOWER(\"{day}\") AND LOWER(stasjonNavn)=LOWER(\"{station}\");"        
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"Her er alle rutene som passererer {station} på {day}er")
        printTable(["Rutenummer", "Stasjon", "Reiser mot","Ankomst", "Avreise", "Ukedag"], result)

        print("Skriv 'lukk' for å gå tilbake til hovedmenyen")

    return

#Lar brukeren søke etter togruter mellom to valgte stasjoner på en gitt dato
def searchRoutes():
    start = input("Hvor reiser du fra? ")
    end = input("Hvor ønsker du å reise? ")

    #TODO gi ordentlig feilmelding/repeter input dersom input er på feil format
    date_input = input("Hvilken dato ønsker du å reise (DD.MM.YYYY) ")
    time_input = input("Hvilket klokkeslett ønsker du å søke fra? (hh:mm) ")
    
    date = datetime.datetime.strptime(date_input, "%d.%m.%Y").date()
    time = datetime.datetime.strptime(time_input, "%H:%M").time()


    #Ikke endre rekkefølgen her, da det for virkninger ellers i koden
    query = f"SELECT Togrute.ruteID, Start.stasjonNavn AS start, Start.avreise,Ende.stasjonNavn AS ende, Ende.ankomst, dato FROM Rutetabell AS Start JOIN Togrute USING(ruteID) JOIN TogruteForekomst USING(ruteID) JOIN Rutetabell AS Ende USING(ruteID) WHERE (dato=\"{date}\" OR dato=\"{date + datetime.timedelta(days=1)}\") AND LOWER(start)=LOWER(\"{start}\") AND LOWER(ende)=LOWER(\"{end}\") AND ((Ende.ankomst>Start.avreise AND Start.neste_dag=Ende.neste_dag) OR (Ende.neste_dag=1 AND Start.neste_dag=0)) ORDER BY dato, Start.avreise;"
    cursor.execute(query)
    result = cursor.fetchall()

    result_to_print = list()
    for row in result:
        departure = datetime.datetime.strptime(row[2], "%H:%M").time()
        dep_date = datetime.datetime.strptime(row[-1], "%Y-%m-%d").date()
        if(departure>=time and dep_date==date):
            result_to_print.append(row)
            continue
        if(dep_date>date):
            result_to_print.append(row)
            continue
    if(len(result_to_print)==0):
        print("Ingen ruter tilgjengelig for denne reisen, vennligst prøv en annen reise")
        return searchRoutes()
    else:
        #Ikke endre rekkefølgen her, da det for virkninger ellers i koden
        printTable(["Rutenummer", "Fra", "Avreise", "Til", "Ankomst", "Dato"], result_to_print)
    return result_to_print


#Lar brukeren velge en togruteforekomst og kjøpe billett til denne
def buyTicket(customerID):
    if(customerID==-1):
        print("Du er nødt til å være registrert kunde/logget inn for å kjøpe billetter")
        return
    #Lar brukeren søke etter en reise mellom stasjoner ved klokkeslett osv.
    valid_routes = searchRoutes()

    #Sørger for gyldie input
    while True:
        row = input("Hvilken av disse vil du kjøpe billett til? (skriv inn radnummer) ")
        if(row=="lukk"):
            return
        try:
            row = int(row)
            break
        except:
            print("Vennligst skriv inn et tall")
            continue
        if(row>len(valid_routes)):
            print("Vennligst skriv inn et tall mellom","1","og",len(valid_routes))
            continue
    ruteID = valid_routes[row-1][0]
    date = datetime.datetime.strptime(valid_routes[row-1][-1],"%Y-%m-%d").date()
    start = valid_routes[row-1][1]
    end = valid_routes[row-1][3]

    #Printer alle gyldige seter/kupeer som brukeren kan kjøpe (altså seter som ikke er opptatt på deres reise, og kupeer som ikke er solgt)
    print("Her er alle de ledige setene/kupeene på din valgte reise:\n\n")
    #TODO print gyldige seter penere og med vognnummer istedet for vognID
    print("Sitteplasser: ")
    valid_seats = findValidSeats(ruteID, date, start, end)
    printTable(["Vognnummer", "Setenummer"], valid_seats)
    print("\n")

    print("Soveplasser: ")
    print("(Hver kupee har 2 soveplasser)")
    #TODO print gyldige senger/kupeer med vognnummer
    valid_bedrooms = findValidBeds(ruteID, date)
    printTable(["Vognnummer", "Kupeenummer"], valid_bedrooms)

    desired_tickets = list()
    print("Skriv 'lukk' for å gå tilbake til hovedmeny\n")

    #Henter vognnummer med korresponderende vognID for hver vogn på ruten
    query = f"SELECT vognnummer, vognID FROM VognOppsett WHERE ruteID={ruteID};"
    cursor.execute(query)
    result = cursor.fetchall()

    #Lager oversettelse fra vognnummer til vognID (trenger vognID for innsetting av nye billetter, men kunder velger åpenbart vognnummer)
    cart_dict = dict()
    for cart in result:
        cart_dict[str(cart[0])] = cart[1]

    time_now = datetime.datetime.now()
    new_order = f"INSERT INTO Ordre (kundenummer, ordredato, ordretid) VALUES ({customerID}, \"{time_now.date()}\",\"{time_now.time().strftime('%H:%M')}\");"
    cursor.execute(new_order)

    get_order_num = f"SELECT max(ordrenummer) FROM Ordre WHERE kundenummer={customerID}"
    cursor.execute(get_order_num)
    ordernumber = cursor.fetchall()[0][0]


    while True:
        desired_cart = input("Hvilken vogn vil du ha plass på? ")
        if(desired_cart=="lukk"):
            return
        desired_number = input("Hvilken sitteplass/sovekupee vil du ha? ")
        try:
            desired_ticket = (int(desired_cart), int(desired_number))
        except:
            print("Vennligst bare skriv inn tall")
            continue
        #Sjekker om valgt vogn og sete/kupee er gyldig valg
        if(not (desired_ticket in valid_seats) and not (desired_ticket in valid_bedrooms)):
            print("Vennligst skriv inn vognnummer og sete/kupeenummer fra utskriften ovenfor")
            continue
        if(desired_ticket in desired_tickets):
            print("Du har allerede valgt denne billetten ")
            continue
        
        #Lager en ny billett på gitt distanse osv.
        insert_ticket = f"INSERT INTO Billett (start, ende, ordrenummer, ruteID, dato) VALUES (\"{start}\", \"{end}\", {ordernumber}, {ruteID}, \"{date}\")"
        cursor.execute(insert_ticket)

        #Finner billettID for den nylig skapte billetten
        find_ticket_number = f"SELECT max(billettID) FROM Billett WHERE ordrenummer={ordernumber}"
        cursor.execute(find_ticket_number)
        ticketnumber = cursor.fetchall()[0][0]


        if(desired_ticket in valid_seats):
            insert_category_ticket = f"INSERT INTO SitteBillett (billettID, vognID, setenummer) VALUES ({ticketnumber}, {cart_dict[str(desired_ticket[0])]}, {desired_ticket[1]})"
        else:
            insert_category_ticket = f"INSERT INTO SoveBillett (billettID, vognID, kupeenummer) VALUES ({ticketnumber}, {cart_dict[str(desired_ticket[0])]}, {desired_ticket[1]})"
        cursor.execute(insert_category_ticket)

        #Legge til nylig konstruert billett i en liste for å sørge for at samme kunde ikke kjøper flere av samme sete e.l.
        desired_tickets.append(desired_ticket)


        more_tickets = input("Vil du legge til flere billetter? (ja/nei)")
        if(more_tickets.lower()=="nei"):
            break

    complete_purchase = input("Fullfør kjøpet? (ja/nei) ")
    if(complete_purchase.lower()=="ja"):
        con.commit()
    return
        



#TODO test på nattog (evt. fix)
def findValidSeats(rute,date,start,end):
    #Finner alle setebilletter som er solgt på denne togruten (med avreise for start, og ankomst tid i endestasjon)
    query = f"SELECT Sete.vognID, Sete.setenummer, Billett.start,Billett.ende FROM Togrute JOIN VognOppsett USING(ruteID) JOIN Vogn USING(vognID) JOIN Sete USING(vognID) JOIN SitteBillett ON Sete.vognID=SitteBillett.vognID AND Sete.setenummer=SitteBillett.setenummer JOIN Billett USING(billettID) JOIN Rutetabell AS Start ON Billett.start=Start.stasjonNavn AND Togrute.ruteID=Start.ruteID JOIN Rutetabell AS Ende ON Billett.ende=Ende.stasjonNavn AND Togrute.ruteID=Ende.ruteID WHERE Togrute.ruteID={rute} AND Billett.dato=\"{date}\";"
    cursor.execute(query)
    purchased_tickets = cursor.fetchall()

    #Henter ut alle delstrekninger på banestrekningen ruten kjører på
    query = f"SELECT stasjonA, stasjonB FROM Togrute JOIN Banestrekning USING(strekningID) JOIN Delstrekning USING(strekningID) WHERE ruteID={rute};"
    cursor.execute(query)
    stretches = cursor.fetchall()


    #Finner rekkefølgen stasjonene kommer i på strekningen ruten kjører på (ikke nødvendigvis i rutens kjøreretning)
    station_order = list()
    stretch_count = dict()
    for stretch in stretches:
        if(stretch_count.get(str(stretch[0]))==None):
            stretch_count[str(stretch[0])] = 0
        if(stretch_count.get(str(stretch[1]))==None):
            stretch_count[str(stretch[1])] = 0
        stretch_count[str(stretch[0])] += 1
        stretch_count[str(stretch[1])] += 1
    for key, val in stretch_count.items():
        if(val==1):
            station_order.append(key)
            break
    for _ in stretches:
        station = station_order[-1]
        to_append = str()
        for stretch in stretches:
            if(station in stretch):
                if(stretch[0] in station_order and stretch[1] in station_order):
                    continue
                to_append = stretch[0]
                if(to_append == station):
                    to_append=stretch[1]
        station_order.append(to_append)
    

    #Reverserer stasjonsrekkefølgen dersom ruten kjører den andre veien
    if(station_order.index(start)>station_order.index(end)):
        station_order.reverse()
    departure = station_order.index(start)
    arrival = station_order.index(end)
    
    #Finner billetter som ikke kan selges til brukeren
    cant_purchase = list()
    for ticket in purchased_tickets:
        taken_dep = station_order.index(ticket[2])
        taken_ariv = station_order.index(ticket[3])


        if(taken_dep<arrival and arrival<=taken_ariv):
            #Legger til vognID, setenummer i billetter som ikke kan kjøpes
            cant_purchase.append((ticket[0], ticket[1]))
            continue
        if(taken_dep<=departure and departure<taken_ariv):
            cant_purchase.append((ticket[0], ticket[1]))
            continue
        if(taken_ariv<=arrival and departure<=taken_dep):
            cant_purchase.append((ticket[0], ticket[1]))
            continue
    
    #Workaround for weird bug with list to tuple conversion in python
    if(len(cant_purchase)==1):
        cant_purchase.append(cant_purchase[-1])


    cant_purchase = tuple(cant_purchase)


    query = f"SELECT vognnummer, setenummer FROM Sete JOIN Vogn USING(vognID) JOIN VognOppsett USING(vognID) WHERE VognOppsett.ruteID={rute} AND (Sete.vognID, Sete.setenummer) NOT IN {cant_purchase}"
    cursor.execute(query)
    result = cursor.fetchall()

    
    return result


def findValidBeds(rute, date):

    #Finner alle kupeer som er solgt
    query = f"SELECT VognOppsett.vognnummer, Kupee.kupeenummer FROM Kupee JOIN Vogn USING(vognID) JOIN VognOppsett USING(vognID) WHERE (Kupee.vognID, Kupee.kupeenummer) NOT IN (SELECT SoveBillett.vognID, SoveBillett.kupeenummer FROM Billett JOIN SoveBillett USING(billettID) WHERE Billett.dato=\"{date}\") AND VognOppsett.ruteID={rute}"
    cursor.execute(query)
    available_bedrooms = cursor.fetchall()
    return available_bedrooms
        

#Hovedprogrammet
def main():
    customer = [-1]
    validChoices = {
        "logginn":"Logge inn til eksisterende bruker",
        "registrer":"Registrer ny kunde",
        "billetter":"Se dine fremtidige reiser",
        "ruter":"Hvilke ruter passerer min stasjon på en gitt ukedag",
        "reise":"Finn togruter mellom to stasjoner på valgt tidspunkt",
        "kjøpe":"Kjøpe billett for ønsket rute",
        "lukk":"Lukk programmet"
    }
    print("----Velkommen til jernbanens nye høyteknologiske billettsystem----")
    while True:
        print("\n\n\n")
        selected = menuSelection(validChoices)

        match selected:
            case "lukk":
                return
            case "registrer":
                customer = registerCustomer()
                print("Du er nå logget inn som:",customer[1],"("+str(customer[0])+")")
            case "logginn":
                customer = logIn()
                print("Du er nå logget inn som:",customer[1],"("+str(customer[0])+")")
            case "billetter":
                viewTickets(customer[0])
            case "ruter":
                viewRoutes()
            case "reise":
                searchRoutes()
            case "kjøpe":
                buyTicket(customer[0])
            case _:
                print("Beklager, noe gikk galt, prøv igjen senere")

if __name__=="__main__":
    main()

cursor.close()
con.close()