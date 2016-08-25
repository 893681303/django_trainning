from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone

# Create your models here.
# MVC MODEL VIEW CONTROLLER


#Post.objects.all()
#Post.objects.create(user=user, title="Some time")
class PostManager(models.Manager):
    def all(self, *args, kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish_lte=timezone.now())

def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Posts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location , blank=True,
                              width_field="width_field",
                              height_field='height_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    objects = PostManager()

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug:
        slug = new_slug
    qs = Posts.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        slug = "%s-%s" % (slug, instance.id)
        return create_slug(instance, slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Posts)


