import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import pandas as pd

from config import (
    MONTHS,
    N_DAYS_TO_SEND,
    PARSE_DATE_FORMATS,
    READ_CSV_FILENAME,
    READ_CSV_SEP,
    READ_DATE_FORMAT,
    WRITE_CSV_FILENAME,
    WRITE_CSV_SEP,
    WRITE_DATE_FORMAT,
    MESSAGE_INITIAL,
    MESSAGE_TEMPORARY,
    MESSAGE_FINAL,
)


def create_message(row):
    link = row.link
    place = row.Place
    date = row.Date.strftime(WRITE_DATE_FORMAT)
    reference = row.name
    status = row.Status
    name_type = "Accidente" if "A-" in reference else "Incidente"
    if status == "INITIAL":
        message = MESSAGE_INITIAL
    elif status == "TEMPORARY":
        message = MESSAGE_TEMPORARY
    elif status == "FINAL":
        message = MESSAGE_FINAL
    else:
        raise NameError("Status not contemplated")
    return (
        message.replace("{Accidente/Incidente}", name_type)
        .replace("{Localización}", place)
        .replace("{Referencia}", reference)
        .replace("{Fecha}", date)
        .replace("{LINK}", link)
    )

def check_if_sent_to_telegram(row, to_send_indexes):

    if row.name in to_send_indexes:
        return False
    if not row.Sent_to_telegram:
        if row.Date > (datetime.now()-timedelta(days=N_DAYS_TO_SEND)):
            return False
    return True



def get_news_and_edited_accidents(df_original, df_new):
    news = df_new[~(df_new.index.isin(df_original.index))]
    edited = df_new.drop(news.index)[
                                        df_new.drop(news.index).Status != df_original.Status]

    change_sent_to_telegram = pd.concat([news, edited])
    df_new["Sent_to_telegram"] = df_new.apply(
                                    lambda x: check_if_sent_to_telegram(
                                            x, change_sent_to_telegram.index), axis=1)
    return df_new


def translate_month(s):
    for month in MONTHS:
        s = s.replace(month, MONTHS[month])
    return s


def get_information(text):
    data_list = text.split(".")
    data = {}
    data["Date"] = translate_month(data_list[0].strip())

    data["Ref"] = data_list[-1].strip()

    data["Place"] = get_place(data_list).strip()
    aircrafts, registrations = get_plane_info(data_list)
    data["Aircrafts"] = aircrafts
    data["Registrations"] = registrations
    data["Text"] = text
    data["Modified"] = False
    data["Sent_to_telegram"] = False
    return data


def get_place(data_list):
    for data in data_list:
        if "(" in data and ")" in data:
            return data
    return ""


def get_plane_info(data_list):
    pattern1 = "[aeronave|helicoptero|helicóptero] (.*),{0,1} matr[íi]cula:{0,1} (.*)"
    pattern2 = (
        "[aeronave|helicoptero|helicóptero] \w{1}:{0,1} (.*), matr[íi]cula:{0,1} (.*)"
    )
    registrations = []
    aircrafts = []
    for data in data_list:
        if m := re.search(pattern2, data.lower()):
            aircrafts.append(m.group(1).strip(" ,").replace("modelo", "").capitalize())
            registrations.append(m.group(2).strip(" ,").replace("modelo", "").upper())
        elif m := re.search(pattern1, data.lower()):
            aircrafts.append(m.group(1).strip(" ,").replace("modelo", "").capitalize())
            registrations.append(m.group(2).strip(" ,").replace("modelo", "").upper())
    return aircrafts, registrations


def get_status(soup_element):
    try:
        status = soup_element.find_next_sibling().text
        link = soup_element.find_next_sibling().find("a")["href"]
        if "final" in status.lower():
            return "FINAL", link
        elif "provisional" in status.lower():
            return "TEMPORARY", "https://www.mitma.gob.es" + link
        else:
            return "INITIAL", ""
    except Exception:
        return "INITIAL", ""


def parse_date(s):
    for date_format in PARSE_DATE_FORMATS:
        try:
            dt = datetime.strptime(s, date_format)
            # print(date_format, dt)
            return dt
        except Exception:
            # print(e)
            pass


def read_and_transform_csv_to_df(file_name=READ_CSV_FILENAME, sep=READ_CSV_SEP):
    df_original = pd.read_csv(file_name, sep=sep).set_index("Ref")
    df_original["Date"] = pd.to_datetime(df_original["Date"], format=READ_DATE_FORMAT)
    df_original["Modified"] = df_original["Modified"].astype(bool)
    return df_original


def parse_year_url_and_add_to_database(year, url):
    df_original = read_and_transform_csv_to_df()
    url += year
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "lxml")

    results = [i for i in soup.find_all("h2") if "Aeronave" in i.text]
    data_final = []
    for result in results:
        # print(result)
        data = get_information(result.text)
        data["Status"], data["link"] = get_status(result)
        data_final.append(data)
    df = pd.DataFrame.from_records(data_final).set_index("Ref")
    df["Date"] = df["Date"].apply(lambda x: parse_date(x))
    df = df.sort_values(by="Date")

    df.update(df_original["Modified"])
    df.update(df_original["Sent_to_telegram"])
    df_original.update(df[df["Modified"] == 0])
    df_original.update(df[["Status", "link", "Sent_to_telegram"]])
    df_original = df_original.combine_first(df)
    save_data(df_original)


def save_data(df, write_csv_filename=WRITE_CSV_FILENAME, sep=WRITE_CSV_SEP):
    df = df.sort_values(by="Date")
    df["Date"] = df.Date.dt.strftime(WRITE_DATE_FORMAT)
    df.to_csv(write_csv_filename, sep=WRITE_CSV_SEP)



def send_message_to_telegram(row, token, chat_id):
    if not row.Sent_to_telegram:
        url = (
            "https://api.telegram.org/bot"
            + token
            + "/sendMessage?chat_id="
            + chat_id
            + "&parse_mode=Markdown&text="
            + row.Message
        )
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False
    else:
        return row.Sent_to_telegram



