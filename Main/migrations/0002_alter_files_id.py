from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
    ]
