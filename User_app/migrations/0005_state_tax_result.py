# Generated by Django 5.0.9 on 2024-11-29 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_app', '0004_state_tax_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='state_tax_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('employer_id', models.IntegerField()),
                ('disposable_earnings', models.FloatField()),
                ('monthly_garnishment_amount', models.FloatField()),
                ('net_pay', models.FloatField()),
                ('duration_of_levies', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
