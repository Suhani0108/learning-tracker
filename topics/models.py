from django.conf import settings
from django.db import models


class Topic(models.Model):
    """A single thing I'm learning, e.g. "Django models"."""

    # The allowed values for `status`. Each pair is (value stored in the
    # database, human-readable label shown in admin and templates).
    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not started"
        IN_PROGRESS = "in_progress", "In progress"
        DONE = "done", "Done"

    # Who this topic belongs to. ForeignKey = "many topics, one user".
    # on_delete=CASCADE means deleting a user also deletes their topics.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="topics",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # blank=True makes it optional
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED,
    )
    # auto_now_add: set once, when the topic is first saved
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now: updated every time the topic is saved
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Show the most recently changed topics first
        ordering = ["-updated_at"]

    def __str__(self):
        # How a topic is displayed in admin and the Django shell
        return self.title


class Resource(models.Model):
    """A link that helps with a topic, e.g. a tutorial or docs page."""

    # related_name lets us write topic.resources.all() to get a topic's links
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=200)
    url = models.URLField("URL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.title
