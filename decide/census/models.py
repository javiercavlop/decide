from django.db import models

class CensusGroup(models.Model):
    name = models.CharField(max_length=256,unique=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    group = models.ForeignKey(CensusGroup,
                                blank=True, null=True,
                                related_name='censuss',
                                on_delete=models.SET_NULL)

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)
    
    def __str__(self):
        selfstr = "({},{})".format(self.voting_id,self.voter_id)
        if self.group:
            selfstr = "({},{},{})".format(self.voting_id,self.voter_id,self.group)
        return selfstr
