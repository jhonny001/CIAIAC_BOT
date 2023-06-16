PARSE_DATE_FORMATS = [
    "%d de %B de %Y",
    "%-d de %B de %Y",
    "%d de %B %Y",
    "%-d de %B %Y",
]
READ_DATE_FORMAT = "%d/%m/%Y"
READ_CSV_FILENAME = "accidents.csv"
READ_CSV_SEP = ";"
WRITE_DATE_FORMAT = "%d/%m/%Y"
WRITE_CSV_FILENAME = "accidents.csv"
WRITE_CSV_SEP = ";"
MONTHS = {
    "enero": "January",
    "febrero": "February",
    "marzo": "March",
    "mayo": "May",
    "abril": "April",
    "junio": "June",
    "julio": "July",
    "agosto": "August",
    "septiembre": "September",
    "octubre": "October",
    "noviembre": "November",
    "diciembre": "December",
}
URL_YEARS = [
    {
        "url": "https://www.mitma.gob.es/organos-colegiados/ciaiac/investigacion/",
        "years": ["2017", "2019-primer-semestre", "2020", "2021", "2022", "2023"],
    },
    {
        "url": "https://www.mitma.gob.es/organos-colegiados/ciaiac/ultraligeros-motorizados-ulm/",
        "years": ["2020", "2021", "2022", "2023"],
    },
]


MESSAGE_INITIAL = """Se ha notificado un nuevo {Accidente/Incidente} en {Localización}, fecha {Fecha} con referencia {Referencia}. Para más información visita la web de la CIAIAC."""
MESSAGE_TEMPORARY = """Se ha publicado la Información Provisional 
{LINK} 
{Accidente/Incidente} ocurrido el {Fecha} con referencia {Referencia} en {Localización}."""
MESSAGE_FINAL = """Se ha publicado el Informe Final 
{LINK}
{Accidente/Incidente} ocurrido el {Fecha} con referencia {Referencia} en {Localización}."""
