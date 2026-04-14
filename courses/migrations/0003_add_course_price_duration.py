# Generated manually for Course price and duration_minutes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_lessoncompletion'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration_minutes',
            field=models.IntegerField(blank=True, help_text='Estimated duration in minutes', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Course price if applicable', max_digits=10, null=True),
        ),
    ]
