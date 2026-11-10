import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_create_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidade', models.CharField(blank=True, max_length=100)),
                ('bio', models.TextField(blank=True)),
                ('anos_experiencia', models.PositiveIntegerField(default=0)),
                ('avaliacao_media', models.DecimalField(decimal_places=2, default=5.0, max_digits=3)),
                ('cadeira_ativa', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='profissional',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Profissional',
                'verbose_name_plural': 'Profissionais',
            },
        ),
    ]
