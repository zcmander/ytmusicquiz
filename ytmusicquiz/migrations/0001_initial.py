# Generated by Django 2.2.5 on 2019-11-24 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionTrack',
            fields=[
                ('videoId', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Youtube Video ID')),
                ('state', models.CharField(choices=[('DRAFT', 'DRAFT'), ('DONE', 'DONE')], max_length=10)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField(blank=True, null=True)),
                ('released', models.IntegerField(blank=True, null=True)),
                ('cover', models.BooleanField(blank=True, default=False)),
                ('is_finnish', models.BooleanField(blank=True, null=True)),
                ('rule10s', models.BooleanField(blank=True, default=False)),
                ('disliked', models.BooleanField(blank=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('artist', models.CharField(max_length=255)),
                ('track', models.CharField(max_length=255)),
                ('feat', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('answered', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ytmusicquiz.Game')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ytmusicquiz.QuestionTrack')),
            ],
            options={
                'unique_together': {('game', 'index'), ('game', 'track')},
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=255)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ytmusicquiz.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ytmusicquiz.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ytmusicquiz.Player')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ytmusicquiz.Question')),
            ],
        ),
    ]
