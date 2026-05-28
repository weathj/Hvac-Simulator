import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hvac', '0018_alter_airunit_session_id'),
    ]

    operations = [
        migrations.RemoveField(model_name='airunit', name='session_id'),
        migrations.AddField(
            model_name='airunit',
            name='session_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.RemoveField(model_name='zone', name='session_id'),
        migrations.AddField(
            model_name='zone',
            name='session_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
