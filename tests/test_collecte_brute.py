from veille import main
from veille.collecte_brute import collecter_lignes_brutes
from veille.core.constantes import COL_DATE, COL_ENTREPRISE, COL_LIEN, COL_SOURCE, COL_TITRE
from veille.pipeline import OffreCandidate


def test_collecter_lignes_brutes_filtre_historique_et_motif_rejet(monkeypatch):
    monkeypatch.setattr(main, "offres_france_travail", lambda: iter([
        OffreCandidate(source="France Travail", url="https://ft/vue", texte_ia="Alternance DevOps", nom_entreprise="ACME", titre="DevOps"),
        OffreCandidate(source="France Travail", url="https://ft/ecole", texte_ia="Formation CESI en alternance", nom_entreprise="CESI", titre="Alternance"),
        OffreCandidate(source="France Travail", url="", texte_ia="Sans URL"),
        OffreCandidate(source="France Travail", url="https://ft/ok", texte_ia="Alternance DevOps à Nancy", nom_entreprise="ACME", titre="DevOps"),
    ]))
    monkeypatch.setattr(main, "offres_la_bonne_alternance", lambda: iter([
        OffreCandidate(source="La Bonne Alternance", url="https://lba/ok", texte_ia="Alternance Cloud", nom_entreprise="Globex", titre="Cloud"),
    ]))
    monkeypatch.setattr(main, "offres_scraping", lambda historique, bilan: iter([
        OffreCandidate(source="HelloWork", url="https://hw/ok", texte_ia="Alternance SecOps", nom_entreprise="Initech", verifier_contrat=True),
    ]))

    historique = {"https://ft/vue": "2026-09-01T00:00:00"}
    lignes = collecter_lignes_brutes(historique)

    liens = [l[COL_LIEN] for l in lignes]
    assert liens == ["https://ft/ok", "https://lba/ok", "https://hw/ok"]
    assert lignes[0][COL_ENTREPRISE] == "ACME" and lignes[0][COL_TITRE] == "DevOps" and lignes[0][COL_SOURCE] == "France Travail"
    assert lignes[2][COL_TITRE] == "(voir lien)"
    assert all(COL_DATE in l for l in lignes)


def test_collecter_lignes_brutes_deduplique_par_url_entre_sources(monkeypatch):
    monkeypatch.setattr(main, "offres_france_travail", lambda: iter([
        OffreCandidate(source="France Travail", url="https://doublon", texte_ia="Alternance DevOps à Nancy", nom_entreprise="ACME"),
    ]))
    monkeypatch.setattr(main, "offres_la_bonne_alternance", lambda: iter([
        OffreCandidate(source="La Bonne Alternance", url="https://doublon", texte_ia="Alternance DevOps à Nancy", nom_entreprise="ACME"),
    ]))
    monkeypatch.setattr(main, "offres_scraping", lambda historique, bilan: iter([]))

    lignes = collecter_lignes_brutes({})

    assert len(lignes) == 1
    assert lignes[0][COL_SOURCE] == "France Travail"
