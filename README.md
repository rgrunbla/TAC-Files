# TAC Files

Ce dépôt contient des fichiers relatifs à l'application Tous Anti Covid (TAC) et Tous Anti Covid Vérif (TAC-V), notamment:

- Les listes noires de pass sanitaires:
    - `blacklist_2ddoc.json` et `blacklist_qrcode.json`, pour les 2D-Doc codes QR dans TAC
    - `blacklist_2ddoc_tacv.json`  et `blacklist_qrcode_tacv.json`, pour les 2D-Doc et les codes QR dans TAC-V
- La liste des autorités de certifications reconnues par TAC-V dans `certificates.txt`, extraite de la config TAC-V présente dans `TAC-V_conf.json`.

Ces fichiers sont téléchargés toutes les 15 minutes en utilisant l'intégration continue fournie par GitHub.