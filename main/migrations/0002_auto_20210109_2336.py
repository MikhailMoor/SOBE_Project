# Generated by Django 3.1.4 on 2021-01-09 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatarimage',
            name='pic',
            field=models.ImageField(upload_to='avatar_img/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='pic',
            field=models.ImageField(upload_to='lots_img/'),
        ),
        migrations.AlterField(
            model_name='lots',
            name='category',
            field=models.ManyToManyField(help_text='Enter lot category', null=True, to='main.Categories'),
        ),
        migrations.AlterField(
            model_name='lots',
            name='region',
            field=models.ManyToManyField(help_text='Enter lot region', null=True, to='main.Regions'),
        ),
        migrations.AlterField(
            model_name='lots',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.sellers'),
        ),
    ]