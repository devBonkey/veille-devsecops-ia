import os
from datetime import datetime

import pandas as pd

from ..core.config import CHEMIN_ARCHIVAGE, FICHIER_EXCEL, FICHIER_EXCEL_BRUT, FICHIER_RAPPORT, GROUPE_ID
from ..core.constantes import (
    COL_A_DECOUVRIR, COL_AJUSTEMENT, COL_CV_ATS, COL_CV_DESIGN, COL_DATE, COL_ENTREPRISE, COL_LETTRE, COL_LIEN,
    COL_LINKEDIN, COL_NOTES, COL_POINTS_FORTS, COL_SCORE, COL_SCORE_INITIAL, COL_STATUT, COL_TITRE, COL_VERDICT,
    COLONNES_RENOMMEES, CV_PAR_GROUPE, MODELE_IA, MODELE_IA_VALIDATION, NOM_FEUILLE, NOM_FEUILLE_BRUTE,
    SEUIL_CANDIDATURE,
)
from ..core.filtres import filtre_ecole_concurrente, filtre_secteur_public
from ..core.utils import normaliser_champ
from .excel_style import appliquer_style_suivi


def generer_rapport_markdown(offres_triees):
    print("\n📝 Rédaction du rapport structuré...")
    os.makedirs(CHEMIN_ARCHIVAGE, exist_ok=True)
    with open(FICHIER_RAPPORT, "w", encoding="utf-8") as f_rapport:
        f_rapport.write(f"# 🛡️ Veille DevSecOps consolidée - Groupe {GROUPE_ID} - {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n\n")
        if not offres_triees:
            f_rapport.write("*Aucune nouvelle offre validée aujourd'hui.*\n")
            return
        f_rapport.write(f"*{len(offres_triees)} offre(s) — triées par score technique.*\n\n")
        for titre_complet, contenu in offres_triees:
            ia = contenu["donnees_ia"]
            f_rapport.write(f"### {titre_complet}\n")
            f_rapport.write(f"- **Match DevSecOps :** {normaliser_champ(ia.get('match_tech'))}\n")
            f_rapport.write(f"- **Verdict :** {normaliser_champ(ia.get('verdict'))}\n")
            if ia.get("ajustement_collaboratif"):
                f_rapport.write(f"- **Analyse collaborative ({MODELE_IA} → {MODELE_IA_VALIDATION}) :** {ia.get('ajustement_collaboratif')}\n")
            f_rapport.write("- **Lien(s) disponible(s) :**\n")
            for lien in contenu["liens"]:
                f_rapport.write(f"  - [Postuler ici]({lien})\n")
            f_rapport.write("\n---\n\n")


def ligne_excel(contenu, cv_groupe, date_ajout):
    ia = contenu["donnees_ia"]
    return {
        COL_DATE: date_ajout,
        COL_ENTREPRISE: normaliser_champ(ia.get("nom_entreprise", "Non précisé")),
        COL_TITRE: normaliser_champ(ia.get("titre_poste", "Poste Inconnu")),
        COL_SCORE: normaliser_champ(ia.get("match_tech", "5/10")),
        COL_POINTS_FORTS: normaliser_champ(ia.get("points_forts", "Non précisé par l'IA")),
        COL_A_DECOUVRIR: normaliser_champ(ia.get("a_decouvrir", "Non précisé par l'IA")),
        COL_VERDICT: normaliser_champ(ia.get("verdict", "Pas de verdict")),
        COL_LIEN: contenu["liens"][0] if contenu["liens"] else "Aucun",
        COL_SCORE_INITIAL: ia.get("score_initial", ""),
        COL_AJUSTEMENT: ia.get("ajustement_collaboratif", ""),
        COL_CV_DESIGN: cv_groupe.get("design", ""),
        COL_CV_ATS: cv_groupe.get("ats", ""),
        COL_LINKEDIN: ia.get("message_linkedin", ""),
        COL_LETTRE: ia.get("lettre_motivation", ""),
        COL_STATUT: "",
        COL_NOTES: "",
    }


def revalider_lignes_existantes(df):
    if df.empty:
        return df
    colonnes = [c for c in (COL_ENTREPRISE, COL_TITRE, COL_VERDICT) if c in df.columns]
    if not colonnes:
        return df
    texte_verif = df[colonnes].astype(str).agg(" ".join, axis=1)
    conserver = texte_verif.apply(lambda t: filtre_secteur_public(t) and filtre_ecole_concurrente(t))
    return df[conserver].reset_index(drop=True)


def charger_excel_existant(chemin, nom_feuille=NOM_FEUILLE, revalider=True):
    if not os.path.exists(chemin):
        return pd.DataFrame()
    try:
        df = pd.read_excel(chemin, engine="openpyxl", sheet_name=nom_feuille)
    except Exception as e:
        print(f"⚠️ Feuille « {nom_feuille} » illisible ou absente, elle sera (re)créée : {e}")
        return pd.DataFrame()
    df = df.rename(columns=COLONNES_RENOMMEES)
    if not revalider:
        return df
    nb_avant = len(df)
    df = revalider_lignes_existantes(df)
    if len(df) < nb_avant:
        print(f"🧹 {nb_avant - len(df)} ancienne(s) offre(s) retirée(s) rétroactivement (secteur public / école).")
    return df


def ecrire_feuille(df, chemin, nom_feuille, styliser):
    with pd.ExcelWriter(chemin, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False, sheet_name=nom_feuille)
        styliser(writer.sheets[nom_feuille], df)


def ecrire_excel(df, chemin, seuil=SEUIL_CANDIDATURE):
    ecrire_feuille(df, chemin, NOM_FEUILLE, lambda feuille, df: appliquer_style_suivi(feuille, df, seuil))


def generer_excel(offres_triees):
    print("📊 Mise à jour du fichier Excel...")
    cv_groupe = CV_PAR_GROUPE.get(GROUPE_ID, {})
    date_ajout = datetime.now().strftime("%d/%m/%Y")
    df_nouveau = pd.DataFrame([ligne_excel(contenu, cv_groupe, date_ajout) for _, contenu in offres_triees])
    df_ancien = charger_excel_existant(FICHIER_EXCEL, NOM_FEUILLE)

    if not df_nouveau.empty and not df_ancien.empty and COL_LIEN in df_ancien.columns:
        df_nouveau = df_nouveau[~df_nouveau[COL_LIEN].isin(df_ancien[COL_LIEN].values)]

    morceaux = [df for df in (df_ancien, df_nouveau) if not df.empty]
    df_final = pd.concat(morceaux, ignore_index=True) if morceaux else pd.DataFrame()
    if df_final.empty:
        print("⚠️ Aucune donnée à écrire dans l'Excel aujourd'hui.")
        return
    ecrire_excel(df_final, FICHIER_EXCEL)
    print(f"✅ Excel mis à jour : {len(df_nouveau)} nouvelle(s) offre(s), {len(df_final)} au total.")


def generer_excel_brut(lignes_brutes):
    print("📊 Mise à jour du fichier des offres brutes...")
    df_nouveau = pd.DataFrame(lignes_brutes)
    df_ancien = charger_excel_existant(FICHIER_EXCEL_BRUT, NOM_FEUILLE_BRUTE, revalider=False)

    if not df_nouveau.empty and not df_ancien.empty and COL_LIEN in df_ancien.columns:
        df_nouveau = df_nouveau[~df_nouveau[COL_LIEN].isin(df_ancien[COL_LIEN].values)]

    morceaux = [df for df in (df_ancien, df_nouveau) if not df.empty]
    df_final = pd.concat(morceaux, ignore_index=True) if morceaux else pd.DataFrame()
    if df_final.empty:
        print("⚠️ Aucune offre brute à écrire aujourd'hui.")
        return
    ecrire_feuille(df_final, FICHIER_EXCEL_BRUT, NOM_FEUILLE_BRUTE, lambda feuille, df: appliquer_style_suivi(feuille, df, 0))
    print(f"✅ Offres brutes mises à jour : {len(df_nouveau)} nouvelle(s), {len(df_final)} au total.")
