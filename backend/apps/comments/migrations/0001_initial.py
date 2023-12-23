# Generated by Django 3.2.9 on 2023-12-23 23:27

from django.db import migrations, models
import django.db.models.deletion
import django_lifecycle.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('home_page', models.URLField(blank=True, null=True, verbose_name='Home Page')),
                ('text', models.TextField(verbose_name='Comment text')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.comment')),
            ],
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]