from functions import (
    create_message,
    get_news_and_edited_accidents,
    parse_year_url_and_add_to_database,
    read_and_transform_csv_to_df,
    save_data,
    send_message_to_telegram,
)
from config import BOT_TOKEN, CHAT_ID, URL_YEARS




def main():
    df_original = read_and_transform_csv_to_df().fillna("")
    for url_year in URL_YEARS:
        for year in url_year["years"]:
            parse_year_url_and_add_to_database(year, url_year["url"])

    df_new = read_and_transform_csv_to_df().fillna("")
    df_news_edited = get_news_and_edited_accidents(df_original, df_new)
    df_news_edited["Message"] = df_news_edited.apply(lambda x: create_message(x), axis=1)
    df_news_edited["Sent_to_telegram"] = df_news_edited.apply(lambda x: send_message_to_telegram(x, BOT_TOKEN, CHAT_ID), axis=1)
    save_data(df_news_edited.drop("Message", axis=1))
    
    return df_news_edited


if __name__ == "__main__":
    main()
