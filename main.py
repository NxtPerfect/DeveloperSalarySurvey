"""
kjønn: Gender of the respondent (e.g., "mann" for male, "kvinne" for female).
utdanning: Level of education, represented numerically:
    4: Bachelor's degree
    5: Master's degree
    Other values represent different educational levels. 
erfaring: Years of professional experience in the field.
arbeidssted: Region where the respondent works (e.g., "Oslo," "Agder," "Nordland").
arbeidssituasjon: Employment type and sector, combining work setting and sector (e.g., "in-house, privat sektor," "konsulent," "offentlig/kommunal sektor").
fag: Area of expertise or specialization (e.g., "AI / maskinlæring" for AI and machine learning).
lønn: Annual salary in Norwegian Krone (NOK).
bonus?: Indicates whether the respondent receives a bonus ("Ja" for yes, "Nei" for no)
"""
import pandas as pd

def run():
    df = pd.read_csv("salaries.csv")
    print(df)
    df = df.rename(columns={
        "kjønn" : "gender",
        "utdanning" : "education",
        "erfaring" : "years of experience",
        "arbeidssted" : "region of residence",
        "arbeidssituasjon" : "employment type and sector",
        "fag" : "expertise",
        "lønn" : "salary"})
    print(df)

if __name__ == "__main__":
    run();
