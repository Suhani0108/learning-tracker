from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ResourceForm, TopicForm
from .models import Resource, Topic


# @login_required sends logged-out visitors to the login page first.
@login_required
def topic_list(request):
    """Home page: the user's topics, with progress stats and a status filter."""
    # Only this user's topics. Every view filters by owner like this.
    my_topics = request.user.topics.all()

    # Build one "tab" per status, with how many topics have that status.
    status_tabs = []
    for value, label in Topic.Status.choices:
        status_tabs.append({
            "value": value,
            "label": label,
            "count": my_topics.filter(status=value).count(),
        })

    total = my_topics.count()
    done = my_topics.filter(status=Topic.Status.DONE).count()
    # Avoid dividing by zero when there are no topics yet
    percent_done = round(done / total * 100) if total else 0

    # ?status=done in the URL shows only done topics. request.GET holds
    # everything after the "?". We ignore values that aren't real statuses.
    selected_status = request.GET.get("status", "")
    topics = my_topics
    if selected_status in Topic.Status.values:
        topics = my_topics.filter(status=selected_status)
    else:
        selected_status = ""

    context = {
        "topics": topics,
        "status_tabs": status_tabs,
        "selected_status": selected_status,
        "total": total,
        "done": done,
        "percent_done": percent_done,
    }
    return render(request, "topics/topic_list.html", context)


@login_required
def topic_detail(request, topic_id):
    """Detail page: one topic, its resources, and a form to add a resource."""
    # owner=request.user means other people's topics give a 404, not a peek
    topic = get_object_or_404(Topic, pk=topic_id, owner=request.user)
    context = {
        "topic": topic,
        "resources": topic.resources.all(),
        "resource_form": ResourceForm(),
    }
    return render(request, "topics/topic_detail.html", context)


@login_required
def topic_create(request):
    """Show an empty form (GET), or save a new topic (POST)."""
    if request.method == "POST":
        # Fill the form with what the user submitted
        form = TopicForm(request.POST)
        if form.is_valid():
            # commit=False gives us the object without saving it yet,
            # so we can set the owner first.
            topic = form.save(commit=False)
            topic.owner = request.user
            topic.save()
            messages.success(request, f"Added “{topic.title}”.")
            return redirect("topics:detail", topic_id=topic.id)
        # If it's not valid, fall through and show the form with errors
    else:
        form = TopicForm()

    return render(request, "topics/topic_form.html", {"form": form, "is_new": True})


@login_required
def topic_edit(request, topic_id):
    """Like topic_create, but the form starts filled in with the topic."""
    topic = get_object_or_404(Topic, pk=topic_id, owner=request.user)
    if request.method == "POST":
        # instance=topic means "update this topic" instead of creating one
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes saved.")
            return redirect("topics:detail", topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)

    return render(request, "topics/topic_form.html", {"form": form, "topic": topic, "is_new": False})


@login_required
def topic_delete(request, topic_id):
    """Ask "are you sure?" (GET), then delete (POST)."""
    topic = get_object_or_404(Topic, pk=topic_id, owner=request.user)
    if request.method == "POST":
        title = topic.title
        topic.delete()
        messages.success(request, f"Deleted “{title}”.")
        return redirect("topics:list")

    return render(request, "topics/topic_confirm_delete.html", {"topic": topic})


# @require_POST: these views only change data, so they refuse plain GET visits.
@login_required
@require_POST
def resource_add(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id, owner=request.user)
    form = ResourceForm(request.POST)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.topic = topic
        resource.save()
        messages.success(request, "Resource added.")
        return redirect("topics:detail", topic_id=topic.id)

    # Show the detail page again, with the form's error messages
    context = {
        "topic": topic,
        "resources": topic.resources.all(),
        "resource_form": form,
    }
    return render(request, "topics/topic_detail.html", context, status=400)


@login_required
@require_POST
def resource_delete(request, resource_id):
    # topic__owner follows the ForeignKey: "the resource's topic's owner"
    resource = get_object_or_404(Resource, pk=resource_id, topic__owner=request.user)
    topic_id = resource.topic_id
    resource.delete()
    messages.success(request, "Resource removed.")
    return redirect("topics:detail", topic_id=topic_id)
