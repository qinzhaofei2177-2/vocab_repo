# Generated by Django 3.0.8 on 2020-07-28 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocabexam', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.BooleanField(choices=[(0, 'male'), (1, 'female')], default=0, max_length=1, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='wechat_openid',
            field=models.CharField(blank=True, max_length=127),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='wechat_unionid',
            field=models.CharField(blank=True, max_length=127),
        ),
    ]
