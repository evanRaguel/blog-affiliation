"""
Module de publication pour le blog d'affiliation automatisé.
Publie le site statique sur GitHub Pages ou Netlify.
"""

import os
import shutil
import subprocess
from datetime import datetime
import sys
from typing import Dict, List, Any, Optional

# Import de la configuration
from config import GITHUB

class Publisher:
    def __init__(self, static_dir: str = 'c:\\Users\\claud\\Blog d\'Affiliation\\static'):
        """
        Initialise le module de publication.
        
        Args:
            static_dir: Répertoire contenant les fichiers statiques à publier.
        """
        self.static_dir = static_dir
        self.github_repo = GITHUB['repo_url']
        self.github_branch = GITHUB['branch']
        
        # Créer un dossier temporaire pour la publication
        self.deploy_dir = 'c:\\Users\\claud\\Blog d\'Affiliation\\deploy'
        os.makedirs(self.deploy_dir, exist_ok=True)
    
    def _run_command(self, command: List[str], cwd: str = None) -> bool:
        """
        Exécute une commande shell.
        
        Args:
            command: Liste des parties de la commande.
            cwd: Répertoire de travail pour la commande.
            
        Returns:
            True si la commande s'est exécutée avec succès, False sinon.
        """
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"[+] Commande exécutée avec succès: {' '.join(command)}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[-] Erreur lors de l'exécution de la commande: {' '.join(command)}")
            print(f"[-] Sortie: {e.stdout}")
            print(f"[-] Erreur: {e.stderr}")
            return False
    
    def publish_to_github(self) -> bool:
        """
        Publie le site sur GitHub Pages.
        
        Returns:
            True si la publication a réussi, False sinon.
        """
        # Vérifier si Git est installé
        try:
            subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("[-] Git n'est pas installé ou accessible. Veuillez l'installer.")
            return False
        
        # Préparer le répertoire de déploiement
        if os.path.exists(self.deploy_dir):
            # Supprimer le contenu existant
            for item in os.listdir(self.deploy_dir):
                item_path = os.path.join(self.deploy_dir, item)
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path) and item != '.git':
                    shutil.rmtree(item_path)
        
        # Copier les fichiers statiques dans le répertoire de déploiement
        for item in os.listdir(self.static_dir):
            src_path = os.path.join(self.static_dir, item)
            dst_path = os.path.join(self.deploy_dir, item)
            
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
            elif os.path.isdir(src_path):
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
        
        # Initialiser le dépôt Git si nécessaire
        if not os.path.exists(os.path.join(self.deploy_dir, '.git')):
            if not self._run_command(['git', 'init'], cwd=self.deploy_dir):
                return False
            
            # Configurer le dépôt distant
            if not self._run_command(['git', 'remote', 'add', 'origin', self.github_repo], cwd=self.deploy_dir):
                return False
        
        # Créer un fichier .nojekyll pour GitHub Pages
        open(os.path.join(self.deploy_dir, '.nojekyll'), 'w').close()
        
        # Ajouter tous les fichiers
        if not self._run_command(['git', 'add', '.'], cwd=self.deploy_dir):
            return False
        
        # Créer un commit
        commit_message = f"Publication automatique du {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if not self._run_command(['git', 'commit', '-m', commit_message], cwd=self.deploy_dir):
            # S'il n'y a pas de changements, ce n'est pas une erreur
            print("[*] Aucun changement à publier")
            return True
        
        # Pousser les changements
        if not self._run_command(['git', 'push', '-f', 'origin', f'master:{self.github_branch}'], cwd=self.deploy_dir):
            return False
        
        print(f"[+] Site publié avec succès sur la branche {self.github_branch}")
        return True
    
    def deploy_to_netlify(self, netlify_token: str = None) -> bool:
        """
        Déploie le site sur Netlify via l'API.
        
        Args:
            netlify_token: Token d'authentification Netlify.
            
        Returns:
            True si le déploiement a réussi, False sinon.
        """
        # Cette fonction nécessite le client Netlify CLI ou l'API Netlify
        # Exemple d'implémentation basique avec le CLI Netlify
        try:
            # Vérifier si le CLI Netlify est installé
            subprocess.run(['netlify', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("[-] Netlify CLI n'est pas installé. Veuillez l'installer via npm install -g netlify-cli")
            return False
        
        # Déployer sur Netlify
        try:
            result = subprocess.run(
                ['netlify', 'deploy', '--dir', self.static_dir, '--prod'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"[+] Site déployé sur Netlify")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"[-] Erreur lors du déploiement sur Netlify")
            print(f"[-] Sortie: {e.stdout}")
            print(f"[-] Erreur: {e.stderr}")
            return False
    
    def run(self, platform: str = 'github') -> bool:
        """
        Exécute la publication du site.
        
        Args:
            platform: Plateforme de publication ('github' ou 'netlify').
            
        Returns:
            True si la publication a réussi, False sinon.
        """
        if platform.lower() == 'github':
            return self.publish_to_github()
        elif platform.lower() == 'netlify':
            return self.deploy_to_netlify()
        else:
            print(f"[-] Plateforme non supportée: {platform}")
            return False

if __name__ == "__main__":
    # Récupérer la plateforme depuis les arguments de ligne de commande
    if len(sys.argv) > 1:
        platform = sys.argv[1]
    else:
        platform = 'github'  # Par défaut
    
    publisher = Publisher()
    success = publisher.run(platform)
    
    if success:
        print(f"[+] Publication réussie sur {platform}")
    else:
        print(f"[-] Échec de la publication sur {platform}")
        sys.exit(1)
