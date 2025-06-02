### models.py
from django.db import models
import zipfile, os
from django.conf import settings

class StaticSiteUpload(models.Model):
    zip_file = models.FileField(upload_to='static_site_zips/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def extract_to_static(self, alias_path=None):
        import zipfile, os, shutil
        from django.conf import settings

        target_dir = os.path.join(settings.MEDIA_ROOT, 'static_sites', str(self.pk))
        os.makedirs(target_dir, exist_ok=True)

        with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
            temp_extract_path = os.path.join(target_dir, 'tmp')
            os.makedirs(temp_extract_path, exist_ok=True)
            zip_ref.extractall(temp_extract_path)

            entries = os.listdir(temp_extract_path)
            if len(entries) == 1 and os.path.isdir(os.path.join(temp_extract_path, entries[0])):
                top_level_dir = os.path.join(temp_extract_path, entries[0])
                for item in os.listdir(top_level_dir):
                    shutil.move(os.path.join(top_level_dir, item), target_dir)
                shutil.rmtree(temp_extract_path)
            else:
                for item in os.listdir(temp_extract_path):
                    shutil.move(os.path.join(temp_extract_path, item), target_dir)
                shutil.rmtree(temp_extract_path)

        self.create_alias_symlink(target_dir, alias_path)
        return target_dir

    def create_alias_symlink(self, target_dir, alias_path=None):
        import os
        from django.conf import settings

        if not alias_path:
            alias_path = os.path.join(settings.MEDIA_ROOT, 'static_sites', f'alias_{self.pk}')

        try:
            # Remove existing alias if it exists
            if os.path.islink(alias_path) or os.path.exists(alias_path):
                os.unlink(alias_path)
            os.symlink(target_dir, alias_path)
            print(f"Alias created: {alias_path} -> {target_dir}")
        except OSError as e:
            print(f"Could not create alias: {e}")

    def save(self, *args, **kwargs):
        new = self.pk is None
        super().save(*args, **kwargs)
        if new:
            self.extract_to_static()