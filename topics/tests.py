from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Resource, Topic


# Each test runs on a fresh, empty test database (your real db.sqlite3 is
# never touched). Run them with:  python manage.py test
class TopicTestCase(TestCase):
    def setUp(self):
        # setUp runs before every test: create two users with one topic each
        self.user = User.objects.create_user("alice", password="test-pass-123")
        self.other_user = User.objects.create_user("bob", password="test-pass-123")
        self.topic = Topic.objects.create(
            owner=self.user, title="Django models", status=Topic.Status.DONE
        )
        self.other_topic = Topic.objects.create(owner=self.other_user, title="Bob's topic")
        # The test client acts like a browser; log it in as alice
        self.client.login(username="alice", password="test-pass-123")


class ModelTests(TopicTestCase):
    def test_str_is_title(self):
        self.assertEqual(str(self.topic), "Django models")

    def test_default_status_is_not_started(self):
        self.assertEqual(self.other_topic.status, Topic.Status.NOT_STARTED)


class ListViewTests(TopicTestCase):
    def test_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("topics:list"))
        # 302 = redirect, here to the login page
        self.assertRedirects(response, reverse("login") + "?next=/")

    def test_shows_only_my_topics(self):
        response = self.client.get(reverse("topics:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django models")
        self.assertNotContains(response, "Bob&#x27;s topic")

    def test_filter_by_status(self):
        Topic.objects.create(owner=self.user, title="Forms", status=Topic.Status.IN_PROGRESS)
        response = self.client.get(reverse("topics:list"), {"status": "in_progress"})
        self.assertContains(response, "Forms")
        self.assertNotContains(response, "Django models")

    def test_unknown_status_shows_everything(self):
        response = self.client.get(reverse("topics:list"), {"status": "nonsense"})
        self.assertContains(response, "Django models")

    def test_progress_numbers(self):
        Topic.objects.create(owner=self.user, title="Forms")
        response = self.client.get(reverse("topics:list"))
        self.assertEqual(response.context["total"], 2)
        self.assertEqual(response.context["done"], 1)
        self.assertEqual(response.context["percent_done"], 50)


class DetailViewTests(TopicTestCase):
    def test_shows_topic(self):
        response = self.client.get(reverse("topics:detail", args=[self.topic.id]))
        self.assertContains(response, "Django models")

    def test_missing_topic_is_404(self):
        response = self.client.get(reverse("topics:detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_other_users_topic_is_404(self):
        response = self.client.get(reverse("topics:detail", args=[self.other_topic.id]))
        self.assertEqual(response.status_code, 404)


class CreateEditDeleteTests(TopicTestCase):
    def test_create_topic(self):
        response = self.client.post(reverse("topics:create"), {
            "title": "Class-based views",
            "description": "",
            "status": "not_started",
        })
        new_topic = Topic.objects.get(title="Class-based views")
        self.assertEqual(new_topic.owner, self.user)  # owner set by the view
        self.assertRedirects(response, reverse("topics:detail", args=[new_topic.id]))

    def test_create_without_title_shows_error(self):
        response = self.client.post(reverse("topics:create"), {"title": "", "status": "done"})
        self.assertEqual(response.status_code, 200)  # form shown again
        self.assertContains(response, "This field is required.")

    def test_edit_topic(self):
        self.client.post(reverse("topics:edit", args=[self.topic.id]), {
            "title": "Django models (updated)",
            "description": "More notes",
            "status": "in_progress",
        })
        self.topic.refresh_from_db()  # reload from the database
        self.assertEqual(self.topic.title, "Django models (updated)")
        self.assertEqual(self.topic.status, Topic.Status.IN_PROGRESS)

    def test_cannot_edit_other_users_topic(self):
        response = self.client.post(
            reverse("topics:edit", args=[self.other_topic.id]),
            {"title": "Hacked", "status": "done"},
        )
        self.assertEqual(response.status_code, 404)
        self.other_topic.refresh_from_db()
        self.assertEqual(self.other_topic.title, "Bob's topic")

    def test_delete_asks_first_then_deletes(self):
        url = reverse("topics:delete", args=[self.topic.id])
        # GET only shows the confirmation page...
        self.client.get(url)
        self.assertTrue(Topic.objects.filter(pk=self.topic.id).exists())
        # ...POST actually deletes
        response = self.client.post(url)
        self.assertRedirects(response, reverse("topics:list"))
        self.assertFalse(Topic.objects.filter(pk=self.topic.id).exists())


class ResourceTests(TopicTestCase):
    def test_add_resource(self):
        self.client.post(reverse("topics:resource_add", args=[self.topic.id]), {
            "title": "Django docs",
            "url": "https://docs.djangoproject.com/",
        })
        self.assertEqual(self.topic.resources.count(), 1)

    def test_invalid_url_is_rejected(self):
        response = self.client.post(reverse("topics:resource_add", args=[self.topic.id]), {
            "title": "Bad link",
            "url": "not a url",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.topic.resources.count(), 0)

    def test_add_resource_needs_post(self):
        response = self.client.get(reverse("topics:resource_add", args=[self.topic.id]))
        self.assertEqual(response.status_code, 405)  # 405 = method not allowed

    def test_delete_resource(self):
        resource = Resource.objects.create(topic=self.topic, title="Docs", url="https://example.com")
        self.client.post(reverse("topics:resource_delete", args=[resource.id]))
        self.assertEqual(self.topic.resources.count(), 0)

    def test_cannot_delete_other_users_resource(self):
        resource = Resource.objects.create(
            topic=self.other_topic, title="Bob's link", url="https://example.com"
        )
        response = self.client.post(reverse("topics:resource_delete", args=[resource.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Resource.objects.filter(pk=resource.id).exists())
