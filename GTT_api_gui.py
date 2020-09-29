from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import requests
import GTT_api_gui_x
import json


def licenses():
    message = "GTT API \n Copyright (C) 2020 Laurence Bird \n" \
               "This program is free software: you can redistribute it and/or modify " \
               "it under the terms of the GNU General Public License as published by " \
               "the Free Software Foundation, either version 3 of the License, or " \
               "(at your option) any later version. \n \n" \
               "This program is distributed in the hope that it will be useful, " \
               "but WITHOUT ANY WARRANTY; without even the implied warranty of " \
               "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the " \
               "GNU General Public License for more details. \n \n" \
               "You should have received a copy of the GNU General Public License " \
               "along with this program.  If not, see https://www.gnu.org/licenses/ "
    messagebox.showinfo("License", message)

def disclaimer():
    message = "This software has been approved for release by the " \
              "Author. Although the software " \
              "has been subjected to rigorous review, the author reserves " \
              "the right to update the software as needed pursuant to " \
              "further analysis and review. No warranty, expressed or " \
              "implied, is made by the author as to " \
              "the functionality of the software and related material nor shall " \
              "the fact of release constitute any such warranty. Furthermore, " \
              "the software is released on condition that neither the author " \
              "shall not be held liable for any damages " \
              "resulting from its authorized or unauthorized use"
    messagebox.showinfo("Disclaimer", message)

def question():
    message = 'Input forms: \n' \
              'YYYY\n' \
              'YYYY-MM\n' \
              'YYYYMM'
    messagebox.showinfo('?', message)

def question_b():
    message_v = 'Select how time period\n' \
                'is to be returned'
    messagebox.showinfo('?', message_v)

def question_c():
    message_c = 'Returned file format\n' \
                'select CSV or xls for excel\n' \
                'select JSON for database format\n'
    messagebox.showinfo('?', message_c)


def question_d():
    message_d = 'Enter multiple codes seperated by , '
    messagebox.showinfo('?', message_d)

def display():
    GTT_api_gui_x.country_displays()

def saveysav(dir_gui, search, formata):
    root = Tk()
    root.filename = filedialog.asksaveasfilename(initialdir=dir_gui, initialfile=search, title="Save file", defaultext="."+formata, filetypes=(
        (formata +" files", "*."+formata), ("all files", "*.*")))
    print(root.filename)
    x = root.filename

    root.withdraw()

    return x


def passwords_for_access(base, username, psswd):
    try:
        tokenResponse = requests.get(base + "/gettoken?userid=" + username + "&password=" + psswd)
    except:
        tokenResponse = requests.get(base + "/gettoken?userid=" + username + "&password=" + psswd, verify=False)

    if tokenResponse.status_code != 200:
        m = tokenResponse.status_code
        messagebox.showinfo('error', m)

    return tokenResponse.text


def imgoing_to_run(*args):
    base = 'https://www.globaltradetracker.com/api/rest'
    username = user_name.get()
    psswd = password.get()
    token = passwords_for_access(base, username, psswd)
    dir_path = folder_path.get()
    print(token)
    if token != []:
        impexp = trade_select.get()
        save_i_e = impexp
        impexp = GTT_api_gui_x.trade_d(impexp)
        period_typo = time_p.get()
        if period_typo == "year to date":
            period_typo = "ytd"
        else:
            period_typo = period_typo[0]
        form = froma.get()
        form = form.rstrip()
        to = to_a.get()
        to = to.rstrip()
        reporter_a = reporter.get()
        reporter_a = reporter_a.rstrip()
        reporter_a_save = reporter_a
        if len(reporter_a) != 2:
            reporter_a = GTT_api_gui_x.country_finder(reporter_a.capitalize())
        else:
            reporter_a = reporter_a.lower()
        partner_a = partner.get()
        partner_a = partner_a.rstrip()
        if partner_a == "All":
            partner_a = ""
        else:
            if len(partner_a) != 2:
                partner_a = GTT_api_gui_x.country_finder(partner_a.capitalize())
            else:
                partner_a = partner_a.lower()
        source = source_gui.get()
        source = source.upper()
        if source == "Un comtrade":
            source = "COMTRADE"
        trade_d = detail.get()
        trade_d = GTT_api_gui_x.details(trade_d)
        hs_codes = search.get()
        hs_level = level_select.get()
        hs_level = GTT_api_gui_x.level_s(hs_level)
        currency = currency_gui.get()
        currency = GTT_api_gui_x.money(currency)
        decimal = deci.get()
        formata = format_select.get()
        formata = formata.rstrip()
        formata = formata.lower()

    urlReport = base + "/getreport?token=" + token + '&impexp=' + impexp + '&periodtype=' + period_typo + '&from=' + form + '&to=' + to + '&reporter=' + reporter_a + '&partner=' + partner_a + '&source=' + source + '&tradedetails=' + trade_d + '&hscode=' + hs_codes + '&hslevel=' + hs_level + '&currency=' + currency + '&decimalscale=' + decimal + '&format=' + formata
    print(urlReport)
    try:
        res2 = requests.get(urlReport)
    except:
        res2 = requests.get(urlReport, verify=False)

    if res2.status_code != 200:
        errr = res2.status_code
        messagebox.showinfo('error', errr)

    else:
        print(res2.status_code)
        print("download complete")
        a = saveysav(dir_path, save_i_e + " " + reporter_a_save + " " + form + " to " + to, formata)

        if formata == 'json':
            r18 = res2.json()
            with open(a , "w") as f:
                json.dump(r18, f)
        elif formata == 'csv':
            with open(a, 'wb') as f:
                f.write(res2.content)
        elif formata == 'xlsx':
            output = open(a, 'wb')
            output.write(res2.content)
            output.close()


if __name__ == "__main__":
    root = Tk()
    root.title("GTT API version 1.0.0")

    mainframe = ttk.Frame(master=root, padding="1 1 1 1", width=1000000, height=100000)
    mainframe.grid(column=50, row=50, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    menubar = Menu(mainframe)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Licence", command=licenses)
    helpmenu.add_command(label="Disclaimer", command=disclaimer)
    menubar.add_cascade(label="Info", menu=helpmenu)

    # vaiables
    search = StringVar()
    user_name = StringVar()
    password = StringVar()
    reporter = StringVar()
    partner = StringVar(value="All")
    folder_path = StringVar(value="C:/")
    froma = StringVar()
    to_a = StringVar()

    # boxes
    search_entry = ttk.Entry(mainframe, width=15, textvariable=search)
    search_entry.grid(column=4, row=6, sticky=(W, E))

    user_name_entry = ttk.Entry(mainframe, width=15, textvariable=user_name)
    user_name_entry.grid(column=2, row=1, sticky=(W, E))
    password_entry = ttk.Entry(mainframe, show="*", width=15, textvariable=password)
    password_entry.grid(column=4, row=1, sticky=(W, E))
    reporter_entry = ttk.Entry(mainframe, width=15, textvariable=reporter)
    reporter_entry.grid(column=2, row=2, sticky=(W, E))
    partner_entry = ttk.Entry(mainframe, width=15, textvariable=partner)
    partner_entry.grid(column=4, row=2, sticky=(W, E))
    from_entry = ttk.Entry(mainframe, width=15, textvariable=froma)
    from_entry.grid(column=2, row=3, sticky=(W, E))
    to_entry = ttk.Entry(mainframe, width=15, textvariable=to_a)
    to_entry.grid(column=4, row=3, sticky=(W, E))

    # buttons
    ttk.Button(mainframe, text="Access data", command=imgoing_to_run).grid(column=1, row=9, sticky=W)
    ttk.Button(mainframe, text="Available countries", command=display).grid(column=5, row=2, sticky=W)
    ttk.Button(mainframe, text="?", command=question).grid(column=5, row=3, sticky=W)
    ttk.Button(mainframe, text="?", command=question_b).grid(column=5, row=4, sticky=W)
    ttk.Button(mainframe, text="?", command=question_c).grid(column=3, row=8, sticky=W)
    ttk.Button(mainframe, text="?", command=question_d).grid(column=5, row=6, sticky=W)

    # Labels
    ttk.Label(mainframe, text="User name").grid(column=1, row=1, sticky=W)
    ttk.Label(mainframe, text="Password").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="Reporter").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, text="Partner").grid(column=3, row=2, sticky=W)
    ttk.Label(mainframe, text="Date from").grid(column=1, row=3, sticky=W)
    ttk.Label(mainframe, text="Date to").grid(column=3, row=3, sticky=W)
    ttk.Label(mainframe, text="Trade").grid(column=1, row=4, sticky=W)
    ttk.Label(mainframe, text="time period").grid(column=3, row=4, sticky=W)
    ttk.Label(mainframe, text="Source").grid(column=1, row=5, sticky=W)
    ttk.Label(mainframe, text="Additional detail").grid(column=3, row=5, sticky=W)
    ttk.Label(mainframe, text="HS code level").grid(column=1, row=6, sticky=W)
    ttk.Label(mainframe, text="HS code(s)").grid(column=3, row=6, sticky=W)
    ttk.Label(mainframe, text="Currency").grid(column=1, row=7, sticky=W)
    ttk.Label(mainframe, text="Decimal format").grid(column=3, row=7, sticky=W)
    ttk.Label(mainframe, text="file format").grid(column=1, row=8, sticky=W)

    # drop down for database cut button selection code in the cut file

    level_select = StringVar(mainframe)
    level_select_s = ["Do not expand", "HS2 level", "HS4 level", "HS6 level", "Tariff line"]
    level_select.set(level_select_s[0])
    ls_to_search = OptionMenu(mainframe, level_select, *level_select_s)
    ls_to_search.grid(row=6, column=2, columnspan=1)
    ls_to_search.config(width=12, font=('Helvetica', 8))


    format_select = StringVar(mainframe)
    format_select_s = ["JSON", "CSV","XLSX"]
    format_select.set(format_select_s[2])
    format_to_search = OptionMenu(mainframe, format_select, *format_select_s)
    format_to_search.grid(row=8, column=2, columnspan=1)
    format_to_search.config(width=12, font=('Helvetica', 8))

    trade_select = StringVar(mainframe)
    trade_select_s = ["Exports", "Imports", "Regional imports", "Regional exports", "Net imports", "Net exports"]
    trade_select.set(trade_select_s[0])
    trade_to_search = OptionMenu(mainframe, trade_select, *trade_select_s)
    trade_to_search.grid(row=4, column=2, columnspan=1)
    trade_to_search.config(width=12, font=('Helvetica', 8))

    detail = StringVar(mainframe)
    detail_s = ["None", "Port", "Subdivision", "Transport", "Customs Regime", "Foreign port"]
    detail.set(detail_s[0])
    detail_to_search = OptionMenu(mainframe, detail, *detail_s)
    detail_to_search.grid(row=5, column=4, columnspan=1)
    detail_to_search.config(width=12, font=('Helvetica', 8))

    source_gui = StringVar(mainframe)
    source_s = ["Default", "UN comtrade", "Eurostate"]
    source_gui.set(source_s[0])
    source_to_search = OptionMenu(mainframe, source_gui, *source_s)
    source_to_search.grid(row=5, column=2, columnspan=1)
    source_to_search.config(width=12, font=('Helvetica', 8))

    time_p = StringVar(mainframe)
    time_p_s = ["Month", "Year", "Quartly", "Semester", "year to date"]
    time_p.set(time_p_s[0])
    time_p_to_search = OptionMenu(mainframe, time_p, *time_p_s)
    time_p_to_search.grid(row=4, column=4, columnspan=1)
    time_p_to_search.config(width=12, font=('Helvetica', 8))

    currency_gui = StringVar(mainframe)
    currency_s = ["$", "€", "£", "A$", "other"]
    currency_gui.set(currency_s[0])
    currency_to_search = OptionMenu(mainframe, currency_gui, *currency_s)
    currency_to_search.grid(row=7, column=2, columnspan=1)
    currency_to_search.config(width=12, font=('Helvetica', 8))

    deci = StringVar(mainframe)
    deci_s = ["0", "1", "2", "3"]
    deci.set(deci_s[0])
    deci_to_search = OptionMenu(mainframe, deci, *deci_s)
    deci_to_search.grid(row=7, column=4, columnspan=1)
    deci_to_search.config(width=12, font=('Helvetica', 8))


    mainframe.bind('<Return>', imgoing_to_run)
    root.config(menu=menubar)
    root.mainloop()