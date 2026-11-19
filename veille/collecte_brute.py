from datetime import datetime

from .core.constantes import COL_DATE, COL_ENTREPRISE, COL_LIEN, COL_SOURCE, COL_TITRE
from .pipeline import motif_rejet


def collecter_lignes_brutes(historique):
    from .main import offres_france_travail, offres_la_bonne_alternance, offres_scraping

    date_ajout = datetime.now().strftime("%d/%m/%Y")
    urls_vues = set()
    lignes = []
    generateurs = (offres_france_travail(), offres_la_bonne_alternance(), offres_scraping(historique, None))
    for generateur in generateurs:
        for candidate in generateur:
            if not candidate.url or candidate.url in historique or candidate.url in urls_vues:
                continue
            if motif_rejet(candidate):
                continue
            urls_vues.add(candidate.url)
            lignes.append({
                COL_DATE: date_ajout,
                COL_SOURCE: candidate.source,
                COL_ENTREPRISE: candidate.nom_entreprise or "Non précisé",
                COL_TITRE: candidate.titre or "(voir lien)",
                COL_LIEN: candidate.url,
            })
    return lignes
