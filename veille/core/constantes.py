SEUIL_CANDIDATURE = 8.0
JOURS_MEMOIRE = 14
MAX_ANALYSES_PAR_RUN = 35
PAUSE_ENTRE_ANALYSES = 2
SEUIL_DISTANCE_RAG = 1.0
MODELE_IA = "openai/gpt-oss-120b"
MODELE_IA_VALIDATION = "qwen/qwen3.8-27b"
NOM_COLLECTION_RAG = "memoire_devsecops_v2"

LOCALISATION = "Nancy"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0"

NOM_FEUILLE = "Suivi"
FICHIER_MASTER = "suivi_candidatures_MASTER.xlsx"
COL_DATE = "Date d'ajout"
COL_ENTREPRISE = "Entreprise"
COL_TITRE = "Titre du Poste"
COL_SCORE = "Score Technique"
COL_POINTS_FORTS = "Points Forts (Maitrisés)"
COL_A_DECOUVRIR = "À Découvrir (Manquants)"
COL_VERDICT = "Verdict IA"
COL_LIEN = "Lien de l'offre"
COL_SCORE_INITIAL = "Score Initial (Groq)"
COL_AJUSTEMENT = "Ajustement Collaboratif"
COL_CV_DESIGN = "CV (design)"
COL_CV_ATS = "CV (ATS)"
COL_LINKEDIN = "Message LinkedIn"
COL_LETTRE = "Lettre Motivation"
COL_STATUT = "Statut"
COL_NOTES = "Notes perso"
COLONNES_RENOMMEES = {"Score Initial (llama)": COL_SCORE_INITIAL}

PROFIL_CANDIDAT = """
- Sécurité : Metasploit, Burp Suite, Nmap, Hydra, Wireshark, John the Ripper, Gobuster, Kali Linux.
- DevOps/Infra : Docker, Kubernetes, Jenkins, GitLab CI/CD, Traefik, Linux, Windows.
- Réseau : Configuration routeurs et switches.
- Dev/Design : Vite, Figma, Tailwind CSS.
""".strip()

MOTS_CLES_COMPLETS = [
    "SecOps", "Cloud Security Engineer", "Ingénieur SecOps", "Architecte Sécurité Cloud", "Consultant Sécurité Cloud",
    "Analyste SOC",
    "DevSecOps", "DevOps", "Site Reliability Engineer (SRE)", "Ingénieur Cloud", "Cloud Builder",
    "Ingénieur DevOps", "Ingénieur Système et Réseau", "Ingénieur de Production IT et Release Engineer",
    "Administrateur Systèmes", "Administrateur Systèmes et Réseaux",
    "Développeur Web", "Développeur Fullstack", "Développeur Mobile Flutter", "Développeur Mobile",
    "Développeur Logiciel",
]

# France Travail combine tous les mots d'un mot-clé : des intitulés longs ne renvoient rien.
# Pour ces groupes, la recherche France Travail utilise donc des mots-clés courts.
MOTS_CLES_FT_PAR_GROUPE = {
    "secu": ["cybersécurité", "sécurité informatique", "SecOps", "analyste SOC", "pentest"],
    "dev": ["développeur web", "développeur fullstack", "développeur mobile", "flutter", "développeur logiciel"],
}

ROME_PAR_GROUPE = {
    "secu": ["M1802"],
    "cloud-devops": ["M1801"],
    "infra-sre": ["M1810"],
    "dev": ["M1805"],
}
ROME_PAR_DEFAUT = ["M1801", "M1802", "M1805", "M1810"]

_REPO_BASE = "https://github.com/devBonkey/veille-devsecops-ia/blob/main/cv"
CV_PAR_GROUPE = {
    "secu": {
        "design": f"{_REPO_BASE}/CV_Bonkey_FIAGNIGBE_admin-systeme-cyber.pdf",
        "ats": f"{_REPO_BASE}/CV_Bonkey_FIAGNIGBE_admin-systeme-cyber.pdf",
    },
    "cloud-devops": {
        "design": f"{_REPO_BASE}/CV_Bonkey_FIAGNIGBE_devops.pdf",
        "ats": f"{_REPO_BASE}/CV_Bonkey_FIAGNIGBE_devops.pdf",
    },
    "infra-sre": {
        "design": f"{_REPO_BASE}/CV_Bonkey_FIAGNIGBE_admin-systeme-cyber.pdf",
        "ats": f"{_REPO_BASE}/CV_Bonkey_FIAGNIGBE_admin-systeme-cyber.pdf",
    },
    "dev": {
        "design": f"{_REPO_BASE}/CV_Bonkey_FIAGNIGBE_dev.pdf",
        "ats": f"{_REPO_BASE}/CV_Bonkey_FIAGNIGBE_dev.pdf",
    },
}
