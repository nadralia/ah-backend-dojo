# Generated by Django 2.1 on 2019-05-09 15:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20190507_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentEditHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited_comment', models.TextField(null=True)),
                ('edited_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('original_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.Comment')),
            ],
        ),
    ]
