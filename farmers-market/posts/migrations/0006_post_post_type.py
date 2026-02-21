# Generated migration for adding post_type field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(
                choices=[('DEFAULT', 'Default Post'), ('HARVEST_FORECAST', 'Harvest Forecast')],
                default='DEFAULT',
                help_text='Type of post',
                max_length=20
            ),
        ),
    ]
