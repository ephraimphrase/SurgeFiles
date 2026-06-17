from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0002_alter_files_id'),
    ]

    operations = [
        # Create Folder model
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='folders',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['name'],
            },
        ),

        # Add folder FK to Files
        migrations.AddField(
            model_name='files',
            name='folder',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='files',
                to='Main.folder',
            ),
        ),

        # Add share_id for public sharing
        migrations.AddField(
            model_name='files',
            name='share_id',
            field=models.CharField(blank=True, max_length=16, null=True, unique=True),
        ),

        # Add file size tracking
        migrations.AddField(
            model_name='files',
            name='size',
            field=models.BigIntegerField(default=0),
        ),

        # Add soft delete fields
        migrations.AddField(
            model_name='files',
            name='is_trashed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='files',
            name='trashed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),

        # Update Files owner related_name
        migrations.AlterField(
            model_name='files',
            name='owner',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='files',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # Add Meta options
        migrations.AlterModelOptions(
            name='files',
            options={'ordering': ['-date'], 'verbose_name_plural': 'Files'},
        ),
    ]
