from functions import (
    create_message,
    get_news_and_edited_accidents,
    parse_year_url_and_add_to_database,
    read_and_transform_csv_to_df,
)
from config import URL_YEARS


# def main(years, url):
#     for year in years:
#         print(year)
#         parse_year_url_and_add_to_database(year, url)


def main():
    df_original = read_and_transform_csv_to_df()
    for url_year in URL_YEARS:
        for year in url_year["years"]:
            parse_year_url_and_add_to_database(year, url_year["url"])
    df_new = read_and_transform_csv_to_df()
    df_news_edited = get_news_and_edited_accidents(df_original, df_new)
    if not df_news_edited.empty:
        df_news_edited["Message"] = df_news_edited.apply(
            lambda x: create_message(x), axis=1
        )
    return df_news_edited


# if __name__ == "__main__":
#     df_original = read_and_transform_csv_to_df()
#     for url_year in URL_YEARS:
#         main(url_year["years"], url_year["url"])
#     df_new = read_and_transform_csv_to_df()
if __name__ == "__main__":
    main()
