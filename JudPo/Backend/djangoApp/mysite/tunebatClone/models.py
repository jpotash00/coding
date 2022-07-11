from django.db import models
class Songs(models.Model):
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    genre = models.CharField(max_length=25)
    released_year = models.IntegerField()
    song_key = models.CharField(max_length=25)
    bpm = models.IntegerField()
    camelot = models.CharField(max_length=3)
    Instrumental_type = models.CharField(max_length=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'songs'

    def __str__(self):
        return self.title