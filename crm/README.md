# Configuration de Celery pour le CRM

Ce guide explique comment configurer et exécuter les tâches planifiées avec Celery et Celery Beat dans le projet CRM.

## Prérequis

- Python 3.8+
- Redis
- Les dépendances Python listées dans `requirements.txt`

## Installation

1. **Installer Redis**

   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt update
     sudo apt install redis-server
     sudo systemctl enable redis-server
     sudo systemctl start redis-server
     ```

   - **macOS (avec Homebrew)**:
     ```bash
     brew install redis
     brew services start redis
     ```

   - **Windows**:
     Téléchargez et installez Redis depuis [https://github.com/microsoftarchive/redis/releases](https://github.com/microsoftarchive/redis/releases)
     
     Ou utilisez WSL (Windows Subsystem for Linux) et suivez les instructions pour Linux.

2. **Installer les dépendances Python**
   ```bash
   pip install -r requirements.txt
   ```

3. **Appliquer les migrations**
   ```bash
   python manage.py migrate django_celery_beat
   ```

## Exécution

1. **Démarrer le serveur Redis** (si ce n'est pas déjà fait)
   ```bash
   # Sur Linux/macOS
   redis-server
   
   # Ou comme service
   sudo systemctl start redis
   ```

2. **Démarrer le worker Celery**
   ```bash
   celery -A crm worker -l info
   ```

3. **Démarrer Celery Beat** (pour les tâches planifiées)
   ```bash
   celery -A crm beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

4. **Pour exécuter manuellement la tâche de rapport**
   ```bash
   python manage.py shell
   ```
   ```python
   from crm.tasks import generate_crm_report
   generate_crm_report.delay()
   ```

## Configuration des tâches planifiées

La tâche `generate_crm_report` est configurée pour s'exécuter tous les lundis à 6h du matin. Cette configuration se trouve dans `crm/settings.py` :

```python
CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
```

## Fichiers de logs

- **Rapports CRM**: `/tmp/crm_report_log.txt`
- **Logs du worker Celery**: S'affichent dans la console où le worker est exécuté

## Dépannage

- **Redis ne répond pas** :
  - Vérifiez que Redis est en cours d'exécution : `redis-cli ping` (doit répondre `PONG`)
  
- **Erreurs d'importation** :
  - Vérifiez que tous les packages sont installés : `pip install -r requirements.txt`
  - Vérifiez que le PYTHONPATH est correct

- **Tâches non exécutées** :
  - Vérifiez que le worker Celery et Celery Beat sont en cours d'exécution
  - Vérifiez les logs pour les erreurs potentielles
