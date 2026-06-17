from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from Main.models import Files

class Command(BaseCommand):
    help = 'Deletes files that have been in the trash for more than 30 days.'

    def handle(self, *args, **options):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        old_trashed_files = Files.objects.filter(is_trashed=True, trashed_at__lt=thirty_days_ago)
        
        count = old_trashed_files.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No old trashed files found to delete.'))
            return
            
        # Delete individually to ensure post_delete signals are fired for each file
        for file in old_trashed_files:
            file.delete()
            
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old trashed files.'))
