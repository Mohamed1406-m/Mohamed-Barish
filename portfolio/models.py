from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=120, default="M Mohamed Barish")
    title = models.CharField(max_length=200, default="Python AI Developer")
    location = models.CharField(max_length=100, default="Chennai, Tamil Nadu")
    email = models.EmailField(default="mdbarish1502@gmail.com")
    linkedin = models.URLField(default="https://linkedin.com/in/mohamed-barish-0191aa27a")
    hero_headline = models.CharField(max_length=200, default="I build the AI that answers when a city calls.")
    hero_sub = models.TextField(default="Python and Django engineer in Chennai. Voice agents, WhatsApp bots and vision checks now running for three municipal corporations.")
    photo = models.ImageField(upload_to="profile/", blank=True, null=True)
    years_exp = models.CharField(max_length=10, default="1+")
    corps_count = models.CharField(max_length=10, default="3")
    apps_count = models.CharField(max_length=10, default="6")
    ai_label = models.CharField(max_length=60, default="Voice · Chat · Vision")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Profile"


class Project(models.Model):
    order = models.PositiveSmallIntegerField(default=0)
    client = models.CharField(max_length=120)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.CharField(max_length=300, help_text="Comma-separated tech tags")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    highlight = models.BooleanField(default=False, help_text="Green highlight card")
    is_active = models.BooleanField(default=True)

    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    def __str__(self):
        return f"{self.client} — {self.title}"

    class Meta:
        ordering = ["order"]


class StackItem(models.Model):
    name = models.CharField(max_length=60)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
