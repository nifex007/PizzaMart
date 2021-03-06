# Generated by Django 3.2 on 2021-05-02 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavour', models.CharField(choices=[('MARGARITA', 'margarita'), ('MARINARA', 'marinara'), ('SALAMI', 'salami')], max_length=10)),
                ('size', models.CharField(choices=[('SMALL', 'small'), ('MEDIUM', 'medium'), ('LARGE', 'large')], max_length=6)),
                ('count', models.IntegerField(default=1)),
                ('order_status', models.CharField(choices=[('RECIEVED', 'recieved'), ('TRANSIT', 'transit'), ('DELIVERED', 'delivered')], default='RECIEVED', max_length=10)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
