# Generated migration for changing image field from URLField to ImageField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_quantity_post_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Product image', null=True, upload_to='posts/'),
        ),
    ]
