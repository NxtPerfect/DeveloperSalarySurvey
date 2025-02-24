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
import seaborn as sb
import matplotlib.pyplot as plt
import streamlit as st

def run():
    df = pd.read_csv("salaries.csv")
    renameColumnsToEnglish(df)
    renameRowsToEnglish(df)
    # Norwegian currency to eur
    # 1 NOK = 0.085706417 EUR
    df.salary = (df.salary * 0.085706417).round(2)

    st.dataframe(df)
    # View expertise/salary plot
    expertiseOnSalary = sb.barplot(x="expertise", y="salary", data=df)
    plt.xticks(rotation=45)
    ylabels = ['{:,.0f}'.format(y) for y in expertiseOnSalary.get_yticks()]
    expertiseOnSalary.set_yticklabels(ylabels)

    st.pyplot(expertiseOnSalary.get_figure())
    # For some reason plot doesn't clear itself
    # If i don't show it, it gets merged to the next one
    st.pyplot(plt.show())

    # residence/salary plot
    residenceOnSalary = sb.barplot(x="residence", y="salary", data=df)
    ylabels = ['{:,.2f}'.format(y) for y in residenceOnSalary.get_yticks()]
    residenceOnSalary.set_yticklabels(ylabels)
    plt.xticks(rotation=45)
    st.pyplot(residenceOnSalary.get_figure())

def renameColumnsToEnglish(df: pd.DataFrame) -> None:
    df.rename(columns={
        "kjønn" : "gender",
        "utdanning" : "education",
        "erfaring" : "experience",
        "arbeidssted" : "residence",
        "arbeidssituasjon" : "employment type and sector",
        "fag" : "expertise",
        "lønn" : "salary"}, inplace=True)

def renameRowsToEnglish(df: pd.DataFrame) -> None:
    df.replace({'bonus?': {"Ja": "Yes", "Nei": "No"}}, inplace=True)
    df.replace({'gender': {"mann": "male", "kvinne": "female", "annet / ønsker ikke oppgi": "other / do not wish to specify"}}, inplace=True)
    df.replace({'expertise': {
        "AI / maskinlæring": "AI / machine learning",
        "annet": "other",
        "arkitektur": "architecture",
        "automatisering": "automation",
        "databaser": "databases",
        "devops / drift": "devops / operation",
        "embedded / IOT / maskinvare": "embedded / IOT / hardware",
        "ledelse/administrativt": "management / administrative",
        "programvare": "software",
        "sikkerhet": "safety",
    }}, inplace=True)
    df.replace({'employment type and sector': {
        "frilans / selvstendig næringsdrivende": "freelance / self-employed",
        "in-house, offentlig/kommunal sektor": "in-house, public/municipal sector",
        "in-house, privat sektor": "in-house, private sector",
        "konsulent": "consultant",
    }}, inplace=True)

if __name__ == "__main__":
    run();
