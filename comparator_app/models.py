from django.db import models


class ComparisonResult(models.Model):
    left_file_name = models.CharField(max_length=255)
    right_file_name = models.CharField(max_length=255)
    similarity_percent = models.FloatField()
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.left_file_name} vs {self.right_file_name} ({self.similarity_percent:.2f}%)"
