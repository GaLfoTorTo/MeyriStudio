from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_create_agendamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
