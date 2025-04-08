
# twingo-racecar-69
> Projet voiture 2025 Groupe 5

## Setup de dev

### Versions & Dependances
- Python `v3.13.2` au minimum.
- Pip `24.2` au minimum.

#### Fedora Linux
```bash
sudo dnf install make automake gcc gcc-c++ kernel-devel
```

### Dépendances
Comment installer les différentes dépendances

#### 1. Setup Environnement Virtuel
```ps1
python -m venv .venv
```

---

<br>

#### 2. Utilisation de l'environnement de dev. (si votre IDE ne le détecte pas)

Windows CMD  
```ps1
.venv/Scripts/activate.bat # cmd.exe
```

Windows Powershell  
```ps1
.venv/Scripts/Activate.ps1 # Powershell
```

<br>

Linux Bash  
```bash
source .venv/bin/activate # Bash/Zsh
```

#### 3. Pour installer les dépendances.
```ps1
pip install -r requirements.txt
```

---

<br>

#### DEBUG : installation des dépendances  
Si vous ne voulez pas utiliser les `.venv`, vous pouvez juste ouvrir un nouveau terminal et taper :

```ps1
pip install -r requirements.txt
```

<br>

## Bible & Conventions

### Nommage du code  
Différentes conventions de nommage des classes, attributs et variables.

Tous vos *Attributs*, *Méthodes*, *Variables* doivent être en `snake_case`  
Toutes vos *Classes* doivent être en `Pascal_Sake_Case`

<br>

---

### Structure des fichiers

Structure des fichiers. Nommage en `Pascal_Sake_Case.py` pour les fichiers de classes et `snake_case{.py}` pour les autres fichiers/dossiers  
```
.
├── requirements.txt
├── .gitignore
├── main.py
│
├── classes
│   └── {Nom_Classe}.py
│
├── preparation
│   └── // Exemples de code
│
└── tests
    └── test_{nom_classe}.py
```

<br>

---

### Branches  
Une tâche, une branche, le nom de la tâche en `snake_case`

<br>

---

### Commits

Pas de commits directement sur la branche `main`, vous devez faire une branche pour chaque feature, et si vous avez fini cette feature et terminé les tests (si les tests sont dans votre tâche), ensuite vous pouvez merge sur la `staging branch`

À quoi doit ressembler un commit :
```md
<type>: <commit-name>

<description>
```


<br>

---

#### type
- `feat` Ajout d'une feature ou d'une partie de feature
- `docs` Ajout de Docstring/Document/Readme/Commentaires
- `test` Ajout/Modification des tests

> Si vous voulez utiliser d'autres types de commits, vous pouvez utiliser les [standards de commit Angular](https://www.conventionalcommits.org/en/v1.0.0/) 

<br>

---