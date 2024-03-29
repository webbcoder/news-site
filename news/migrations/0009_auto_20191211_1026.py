# Generated by Django 2.2.8 on 2019-12-11 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import news.utils


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20191210_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Posted by'),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to=news.utils.get_timestamp_path, verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='List in?'),
        ),
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=news.utils.get_timestamp_path, verbose_name='Image')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Post', verbose_name='Post')),
            ],
            options={
                'verbose_name': 'Additional illustration',
                'verbose_name_plural': 'Additional illustrations',
            },
        ),
    ]
