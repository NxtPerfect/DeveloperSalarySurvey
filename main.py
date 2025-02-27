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

    convertSalaryToEur(df)

    st.dataframe(df)
    showExpertiseOnSalaryPlot(df)
    showResidenceOnSalaryPlot(df)
    showExperienceOnSalaryPlot(df)
    showSalaryHistPlot(df)
    showExperienceHistPlot(df)
    showGenderHistPlot(df)
    showGenderOnSalaryPlot(df)

    showTop1Percent(df)
    showBottom10Percent(df)
    showMedianPerExpertise(df)


def renameColumnsToEnglish(df: pd.DataFrame) -> None:
    df.rename(columns={
        "kjønn" : "gender",
        "utdanning" : "education",
        "erfaring" : "experience",
        "arbeidssted" : "residence",
        "arbeidssituasjon" : "employment type and sector",
        "fag" : "expertise",
        "lønn" : "salary"},
              inplace=True)

def renameRowsToEnglish(df: pd.DataFrame) -> None:
    df.replace({'bonus?': {"Ja": "Yes",
                           "Nei": "No"}},
               inplace=True)
    df.replace({'gender': {"mann": "male",
                           "kvinne": "female",
                           "annet / ønsker ikke oppgi": "other / do not wish to specify"}},
               inplace=True)
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

def convertSalaryToEur(df: pd.DataFrame) -> None:
    df.salary = (df.salary * 0.085706417).round(2)

def showExpertiseOnSalaryPlot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    sb.barplot(x="expertise", y="salary", data=df, ax=ax)
    ax.tick_params(axis='x', rotation=45)
    ylabels = ['{:,.0f}'.format(y) for y in ax.get_yticks()]
    ax.set_yticklabels(ylabels)
    st.pyplot(fig)

def showResidenceOnSalaryPlot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    sb.barplot(x="residence", y="salary", data=df)
    ylabels = ['{:,.2f}'.format(y) for y in ax.get_yticks()]
    ax.tick_params(axis='x', rotation=45)
    ax.set_yticklabels(ylabels)
    st.pyplot(fig)

def showExperienceOnSalaryPlot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    ylabels = ['{:,.2f}'.format(y) for y in ax.get_yticks()]
    ax.set_yticklabels(ylabels)
    sb.kdeplot(x="experience", y="salary", data=df)
    st.pyplot(fig)

def showSalaryHistPlot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    sb.histplot(x="salary", data=df)
    xlabels = ['{:,.0f}'.format(x) for x in ax.get_xticks()]
    ax.set_xticklabels(xlabels)
    st.pyplot(fig)

def showExperienceHistPlot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    sb.histplot(x="experience", data=df)
    xlabels = ['{:,.0f}'.format(x) for x in ax.get_xticks()]
    ax.set_xticklabels(xlabels)
    st.pyplot(fig)

def showGenderHistPlot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    sb.histplot(x="gender", data=df)
    xlabels = ['{:,.0f}'.format(x) for x in ax.get_xticks()]
    ax.set_xticklabels(xlabels)
    st.pyplot(fig)

def showGenderOnSalaryPlot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    sb.barplot(x="gender", y="salary", data=df)
    xlabels = ['{:,.0f}'.format(x) for x in ax.get_xticks()]
    ax.set_xticklabels(xlabels)
    st.pyplot(fig)

def showTop1Percent(df: pd.DataFrame) -> None:
    howManyRows = len(df)
    howManyTop1Percent = round(howManyRows * 0.01)
    st.markdown("# Top 1% Salary")
    top1Percent = df.nlargest(howManyTop1Percent, "salary")
    st.text(f"Range: {top1Percent.min()["salary"]:,.0f}€ - {top1Percent.max()["salary"]:,.0f}€")
    st.text(f"Average: {top1Percent.loc[:, 'salary'].mean():,.2f}€")
    st.text(f"Median: {top1Percent.loc[:, 'salary'].median():,.2f}€")

    fig, ax = plt.subplots()
    sb.histplot(x="salary", data=top1Percent)
    st.pyplot(fig)

def showBottom10Percent(df: pd.DataFrame) -> None:
    howManyRows = len(df)
    howManyBottom10Percent = round(howManyRows * 0.1)
    st.markdown("# Bottom 10% Salary")
    bottom10Percent = df.tail(howManyBottom10Percent)
    st.text(f"Range: {bottom10Percent.min()["salary"]:,.0f}€ - {bottom10Percent.max()["salary"]:,.0f}€")
    st.text(f"Average: {bottom10Percent.loc[:, 'salary'].mean():,.2f}€")
    st.text(f"Median: {bottom10Percent.loc[:, 'salary'].median():,.2f}€")

    fig, ax = plt.subplots()
    sb.histplot(x="salary", data=bottom10Percent)
    st.pyplot(fig)

def showMedianPerExpertise(df: pd.DataFrame) -> None:
    pass
    group = df.groupby("expertise")
    # Get each expertise
    # show median per each

if __name__ == "__main__":
    run();
