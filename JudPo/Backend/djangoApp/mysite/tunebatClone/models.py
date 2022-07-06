from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class song_Mixing(models.Model):
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,blank=True)
    artist = models.CharField(max_length=50,blank=True)
    genre = models.CharField(max_length=25,blank=True)
    released_year = models.IntegerField(blank=False, default=0, validators=[MaxValueValidator(9999)])
    song_key = models.CharField(max_length=25, blank=True)
    bpm = models.IntegerField(blank=False, default=0, validators=[MaxValueValidator(999)])
    camelot = models.CharField(max_length=3,blank=True)
    Instrumental_type = models.CharField(max_length=4)

    def _str_(self):
        return self.songMixing