# A "data migration": instead of changing tables, it changes rows.
# Topics created before we added `owner` have no owner, so we give them
# to the first admin user. This runs once, between migrations 0002 and 0004.

from django.db import migrations


def assign_owner(apps, schema_editor):
    # Use apps.get_model (not a direct import) so we get the model as it
    # looked at this point in the migration history.
    Topic = apps.get_model("topics", "Topic")
    User = apps.get_model("auth", "User")

    ownerless = Topic.objects.filter(owner__isnull=True)
    if not ownerless.exists():
        return  # fresh database, nothing to do

    owner = (
        User.objects.filter(is_superuser=True).order_by("id").first()
        or User.objects.order_by("id").first()
    )
    if owner is None:
        # No users at all, so these topics can't belong to anyone.
        ownerless.delete()
    else:
        ownerless.update(owner=owner)


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_alter_topic_options_topic_owner_topic_updated_at_and_more'),
    ]

    operations = [
        # The second function runs if you ever migrate backwards; doing nothing is fine.
        migrations.RunPython(assign_owner, migrations.RunPython.noop),
    ]
