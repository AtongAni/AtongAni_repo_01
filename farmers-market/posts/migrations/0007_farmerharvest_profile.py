# Generated migration for adding FarmerHarvestProfile model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_post_post_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerHarvestProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_size', models.DecimalField(decimal_places=2, help_text='Land size in hectares', max_digits=8)),
                ('land_size_unit', models.CharField(default='hectares', help_text='Unit of measurement for land size', max_length=20)),
                ('crop_type', models.CharField(help_text='Type of crop/crops being grown', max_length=255)),
                ('previous_harvest_quantity', models.DecimalField(blank=True, decimal_places=2, help_text='Quantity from previous harvest', max_digits=10, null=True)),
                ('previous_harvest_unit', models.CharField(default='KG', help_text='Unit for previous harvest', max_length=20)),
                ('previous_harvest_date', models.DateField(blank=True, help_text='Date of previous harvest', null=True)),
                ('farming_experience_years', models.PositiveIntegerField(blank=True, help_text='Years of farming experience', null=True)),
                ('location', models.CharField(blank=True, help_text='Farm location', max_length=255)),
                ('notes', models.TextField(blank=True, help_text='Additional notes or farming details')),
                ('status', models.CharField(choices=[('PENDING', 'Pending Review'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20)),
                ('admin_notes', models.TextField(blank=True, help_text='Admin review notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('approved_by', models.ForeignKey(blank=True, help_text='Admin who approved this profile', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_farmers', to=settings.AUTH_USER_MODEL)),
                ('farmer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='harvest_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Farmer Harvest Profile',
                'verbose_name_plural': 'Farmer Harvest Profiles',
            },
        ),
    ]
